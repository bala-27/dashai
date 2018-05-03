# Jira-Influx

`jira-influx` is an integration tool that pulls from JIRA and pushes into InfluxDB. It is configured through `config.json`, which specifies hosts, credentials, and databases for Jenkins and InfluxDB databases.

## Configuration

1. Ensure an internet-accessible Jenkins instance is properly running, with test data.
2. With InfluxDB running (see `../influxdb`), create a database for JIRA.
```bash
$ docker run --rm --link=influxdb -it influxdb influx -host influxdb
> CREATE DATABASE jira
```

3. Edit `config.json`
4. Add the internet-accessible Jenkins URL, username, and password. Adjust the queries as per the [project page](https://github.com/cbonitz/jira-influx).
5. Add the InfluxDB URL, database, username, and password (leave the last two blank if you did not configure auth/authz).
6. Build the image and run it with the correct mounts.
```bash
$ WD=$(pwd)
$ docker build -t jira-influx .
$ docker run --link influxdb \
             --name jira-influx \
             -v ${WD}/config.json:/go/src/app/config.json \
             jira-influx
```

Alternatively, the JSON contents may be specified in the environmental variable
`JIRA_INFLUX_CONFIG_JSON`. For example,

```
$ docker run --link influxdb \
             --name jira-influx \
             -e JIRA_INFLUX_CONFIG_JSON="$(cat config.json)" \
             jira-influx
```
