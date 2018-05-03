#from __main__ import app
from common import *
from config import *
from dashboards import grafanacreds

def deploy_DS_influx(name,url,db,grafana):
        creds=grafanacreds(grafana)
        if "FAILED" in creds or "NOSVC" in creds:
                return render_template('grafanahealth.html', error=error) 
        elif "LOST" in creds:
                error="LOST"
                return render_template('grafanahealth.html', error=error) 
        else:      
                src="""
                {
                "name":"%s",
                "type":"influxdb",
                "typeLogoUrl":"public/app/plugins/datasource/influxdb/img/influxdb_logo.svg",
                "access":"proxy",
                "url":"http://%s",
                "password": "",
                "user": "",
                "database": "%s",
                "basicAuth": "false"
                }
                """
                form=(src % (name,url,db))
                data=json.loads(form)
                r = requests.post("http://"+creds+"@"+grafana+"/api/datasources", data)
                return(r.status_code)


def deploy_DS_prom(url,grafana):
        creds=grafanacreds(grafana)
        if "FAILED" in creds or "NOSVC" in creds:
              return render_template('grafanahealth.html', error=error) 
        elif "LOST" in creds:
              error="LOST"      
              return render_template('grafanahealth.html', error=error) 
        else:   
                print("Creating datasource")
                src="""
                {
                "name":"DasahiPromK8S",
                "type":"prometheus",
                "typeLogoUrl":"public/app/plugins/datasource/prometheus/img/prometheus_logo.svg",
                "access":"proxy",
                "url":"http://%s",
                "password":"",
                "user":"",
                "database":"",
                "basicAuth":false,
                "isDefault":false
                }
                """
                form=(src % (url))
                data=json.loads(form)
                r = requests.post("http://"+creds+"@"+grafana+"/api/datasources", data)
                return r.status_code
