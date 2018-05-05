package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"regexp"
	"strconv"
	"time"

	"github.com/influxdata/influxdb/client/v2"
	"github.com/namsral/flag"
	"golang.org/x/net/context"
	"golang.org/x/oauth2"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/sheets/v4"
)

// tokenFromFile retrieves a Token from a given file path.
// It returns the retrieved Token and any read error encountered.
func tokenFromFile(file string) (*oauth2.Token, error) {
	f, err := os.Open(file)
	if err != nil {
		return nil, err
	}
	t := &oauth2.Token{}
	err = json.NewDecoder(f).Decode(t)
	defer f.Close()
	return t, err
}

// getClient uses a Context and Config to retrieve a Token
// then generate a Client. It returns the generated Client.
func getClient(ctx context.Context, config *oauth2.Config, tokenFile string) (*http.Client, error) {
	loadedTok, err := tokenFromFile(tokenFile)
	if err != nil {
		log.Printf("Could not load token from '%s'\n", tokenFile)
		return nil, err
	}
	// force refresh
	tokenSource := config.TokenSource(ctx, loadedTok)
	tok, err := tokenSource.Token()
	if err != nil {
		log.Printf("Could not refresh token from '%s'\n", tokenFile)
		return nil, err
	}
	return config.Client(ctx, tok), nil
}

func main() {
	var host, database, user, password, docId, sheetName, clientSecretFile, tokenFile string
	flag.StringVar(&host, "host", "http://dashai-influxdb:8086", "InfluxDB Host")
	flag.StringVar(&database, "database", "DashAiSheets", "InfluxDB Database")
	flag.StringVar(&user, "user", "", "InfluxDB User")
	flag.StringVar(&password, "password", "", "InfluxDB Password")
	flag.StringVar(&docId, "doc-id", "1NnmdNxhBKQe9veBoWjptDCG2ZOOrOXkNV6yqMYP4meI", "Google Sheet Documen ID")
	flag.StringVar(&sheetName, "sheet", "dashai", "Google Sheet Name")
	flag.StringVar(&clientSecretFile, "client-secret-file", "client_secret.json", "JSON file containing the Client Secret")
	flag.StringVar(&tokenFile, "token-file", "token.json", "JSON file to read/write the token")
	flag.Parse()

	// queryDB convenience function to query the database
	queryDB := func(clnt client.Client, cmd string) (res []client.Result, err error) {
		q := client.Query{
			Command:  cmd,
			Database: database,
		}
		if response, err := clnt.Query(q); err == nil {
			if response.Error() != nil {
				return res, response.Error()
			}
			res = response.Results
		} else {
			return res, err
		}
		return res, nil
	}

	first := true
	for {
		if !first {
			<-time.After(5 * time.Second)
		} else {
			first = false
		}

		// Setup OAuth2
		ctx := context.Background()
		b, err := ioutil.ReadFile(clientSecretFile)
		if err != nil {
			log.Printf("Unable to read client secret file: %v", err)
			continue
		}
		config, err := google.ConfigFromJSON(b,
			"https://www.googleapis.com/auth/spreadsheets.readonly")
		if err != nil {
			log.Printf("Unable to parse client secret file to config: %v", err)
			continue
		}
		sheetsClient, err := getClient(ctx, config, tokenFile)
		if err != nil {
			log.Printf("Unable to get fresh token: %v", err)
			continue
		}

		c, err := client.NewHTTPClient(client.HTTPConfig{
			Addr:     host,
			Username: user,
			Password: password,
		})
		if err != nil {
			log.Println(err)
			continue
		}

		_, err = queryDB(c, fmt.Sprintf("CREATE DATABASE %s", database))
		if err != nil {
			log.Println(err)
		}

		// Create a new point batch
		bp, err := client.NewBatchPoints(client.BatchPointsConfig{
			Database:  database,
			Precision: "s",
		})
		if err != nil {
			log.Println(err)
			continue
		}

		// Fetch Sheets
		srv, err := sheets.New(sheetsClient)
		if err != nil {
			log.Printf("Unable to retrieve Sheets Client %v", err)
			continue
		}

		readRange := fmt.Sprintf("%s!A2:D", sheetName)
		resp, err := srv.Spreadsheets.Values.Get(docId, readRange).Do()
		if err != nil {
			log.Printf("Unable to retrieve data from sheet. %v", err)
			continue
		}

		currentSection := ""
		for _, row := range resp.Values {
			// Fix row length
			for len(row) < 4 {
				row = append(row, "")
			}

			rowSection := row[0].(string)
			if rowSection != "" && rowSection != currentSection {
				currentSection = rowSection
			}

			rowField := row[1].(string)
			if rowField == "" {
				continue
			}
			rowUnit := row[3].(string)

			re := regexp.MustCompile("[^0-9.]")
			cleanedValue := re.ReplaceAllString(row[2].(string), "")
			value := float64(0)
			if len(cleanedValue) > 0 {
				value, err = strconv.ParseFloat(cleanedValue, 64)
				if err != nil {
					log.Println("ERR:", err)
					value = 0
				}
			}

			// Create a point and add to batch
			tags := map[string]string{"section": currentSection, "field": rowField}
			fields := map[string]interface{}{
				"value": value,
				"unit":  rowUnit,
			}
			pt, err := client.NewPoint("rows", tags, fields, time.Now())
			if err != nil {
				log.Println(err)
			}
			bp.AddPoint(pt)
		}

		// Write the batch
		if err := c.Write(bp); err != nil {
			log.Printf("Writing to influxdb: %v", err)
			continue
		}

		log.Println("Wrote", len(bp.Points()), "points to", host, ">", database)
	}
}
