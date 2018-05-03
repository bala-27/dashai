#from __main__ import app
from common import *
from config import *

def deplpoy_dashboard(id,grafana):
    creds=grafanacreds(grafana)
    if "FAILED" in creds or "NOSVC" in creds:
        error=creds
        return render_template('grafanahealth.html', error=error) 
    elif "LOST" in creds:
        error="LOST"
        return render_template('grafanahealth.html', error=error) 
    else:    
        headers = {'Content-type': 'application/json', 'charset':'UTF-8'}
        if id == '1':
            url = 'https://raw.githubusercontent.com/alyarctiq/dashboards/master/gsheets.json'
            response = urllib.urlopen(url)
            data = response.read()
            r = requests.post("http://"+creds+"@"+grafana+"/api/dashboards/db", data, headers=headers)
            return("Status:" + str(r.status_code))
        if id == '2':
            url = 'https://raw.githubusercontent.com/alyarctiq/dashboards/master/ocp36.json'
            response = urllib.urlopen(url)
            data = response.read()
            r = requests.post("http://"+creds+"@"+grafana+"/api/dashboards/db", data, headers=headers)
            return("Status:" + str(r.status_code))
        if id == '3':
            url = 'https://raw.githubusercontent.com/alyarctiq/dashboards/master/dashai-nagios-linux.json'
            response = urllib.urlopen(url)
            data = response.read()
            r = requests.post("http://"+creds+"@"+grafana+"/api/dashboards/db", data, headers=headers)
            return("Status:" + str(r.status_code))
        if id == '4':
            url = 'https://raw.githubusercontent.com/alyarctiq/dashboards/master/ocp37.json'
            response = urllib.urlopen(url)
            data = response.read()
            r = requests.post("http://"+creds+"@"+grafana+"/api/dashboards/db", data, headers=headers)
            return("Status:" + str(r.status_code))
        if id == '5':
            url = 'https://raw.githubusercontent.com/alyarctiq/dashboards/master/dashai-apache.json'
            response = urllib.urlopen(url)
            data = response.read()
            r = requests.post("http://"+creds+"@"+grafana+"/api/dashboards/db", data, headers=headers)
            return("Status:" + str(r.status_code))
        if id == '6':
            url = 'https://raw.githubusercontent.com/alyarctiq/dashboards/master/dashai-host-metrics.json'
            response = urllib.urlopen(url)
            data = response.read()
            r = requests.post("http://"+creds+"@"+grafana+"/api/dashboards/db", data, headers=headers)
            return("Status:" + str(r.status_code))
        if id == '7':
            url = 'https://raw.githubusercontent.com/alyarctiq/dashboards/master/dashai-github.json'
            response = urllib.urlopen(url)
            data = response.read()
            r = requests.post("http://"+creds+"@"+grafana+"/api/dashboards/db", data, headers=headers)
            return("Status:" + str(r.status_code))

@app.route('/getdashboards')
def get_dashboards():
    if not session.get('logged_in'):
        error = "Log In First..."
        return render_template('auth.html', error=error)
    else:
        dashboards=[]
        command="oc get route grafana -o template --template {{.spec.host}} --config="+session['kubeconfig']
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        grafana = cmd.strip()
        if grafana == "":    
            return render_template('dashboards.html',dashboards=dashboards)
        else:
            creds=grafanacreds(grafana)    
            if "FAILED" in creds or "NOSVC" in creds:
                error=creds
                return render_template('grafanahealth.html', error=error) 
            elif "LOST" in creds:
                error="LOST"
                return render_template('grafanahealth.html', error=error) 
            else: 
                headers = {'Content-type': 'application/json', 'charset':'UTF-8'}
                url = "http://"+creds+"@"+grafana+"/api/search"
                resp = requests.get(url=url)
                data = json.loads(resp.text)
                if len(data) == 0:                
                    dashboards.append('None')
                else:
                    for i in xrange(len(data)):
                        dashboards.append([])
                        dashboards[i].append(data[i]["title"])
                        uri="http://"+grafana+"/dashboard/"+data[i]["uri"]+"?refresh=10s&orgId=1"
                        dashboards[i].append(uri)
                print(dashboards)
                return render_template('dashboards.html',dashboards=dashboards)

@app.route('/launchdashboard',methods = ['POST'])
def launchdashboard():
    if request.method == 'POST':
      result = request.form
      dburi = request.form.get('dburi')
    return render_template('dashboards-vr-ldr.html',dburi=dburi)


@app.route('/dashboards-ldr')
def dashboards():
    if not session.get('logged_in'):
        error = "Log In First..."
        return render_template('auth.html', error=error)
    else:
        return render_template('dashboards-ldr.html')

def grafanacreds(grafana):
    urlbase="http://"+grafana
    headers = {'Content-type': 'application/json', 'charset':'UTF-8'}
    if not session.get('logged_in'):
        error = "Log In First..."
        return render_template('auth.html', error=error)
    else:        
        r = requests.get(urlbase,auth=('dashaisvc','K25SNJ6HURUrpHet'),headers=headers )
        print(r.status_code)
        if str(r.status_code) == "200":
            creds="dashaisvc:K25SNJ6HURUrpHet"
            print ("final creds returned stg1")
            return(creds) #success
        r = requests.get(urlbase,auth=('admin','dashai'),headers=headers )
        if str(r.status_code) == "401":
            return("BASE LOST")
        elif str(r.status_code) == "200":
            r = requests.get(urlbase,auth=('dashaisvc','K25SNJ6HURUrpHet'),headers=headers )
            if str(r.status_code) == "401":
                print("attempting to create service account...")
                data='{"name":"DO NOT DELETE","email":"info@arctiq.ca","login":"dashaisvc","password":"K25SNJ6HURUrpHet","role":"Admin"}'
                url=urlbase+"/api/admin/users"
                r = requests.post(url, data=data, headers=headers, auth=('admin','dashai'))
                if str(r.status_code) != "200":
                    return("SVC CREATE FAILED")
                else:
                    print("Getting User List")
                    url=urlbase+"/api/users?perpage=500"
                    r = requests.get(url,headers=headers, auth=('admin','dashai'))
                    json_data = json.loads(r.text)
                    for r in (row for row in json_data if 'id' in row): 
                        if r['login'] == "dashaisvc":
                            id=str(r['id'])
                            print("Attempting Elevation")
                            data='{"isGrafanaAdmin": true}'
                            url=urlbase+"/api/admin/users/"+id+"/permissions"
                            r = requests.put(url, data=data, headers=headers, auth=('admin','dashai'))
                    if str(r.status_code) != "200":
                        return("ELEVATION FAILED")                        
                    else:
                         print("Evelation Success, Attempting Org User Update")
                         url=urlbase+"/api/org/users/"+id
                         print(url)
                         data='{"role": "Admin"}'
                         r = requests.patch(url, data=data, headers=headers, auth=('admin','dashai'))
                         if str(r.status_code) != "200":
                            return("PATCH FAILED")  
                            #return("Patch Failed: "+ str(r.status_code))  
                         else:
                            creds="dashaisvc:K25SNJ6HURUrpHet"
                            print ("final creds returned stg2")
                            return(creds)#success
        elif r.status_code == 503:
            return("NOSVC")
            

def grafanahealthcheck(grafana):
    fixattempt="0"
    urlbase="http://"+grafana
    headers = {'Content-type': 'application/json', 'charset':'UTF-8'}
    if not session.get('logged_in'):
        error = "Log In First..."
        return render_template('auth.html', error=error)
    else:
        while True:                  
            r = requests.get(urlbase,auth=('dashaisvc','K25SNJ6HURUrpHet'),headers=headers )
            print(r.status_code)
            if str(r.status_code) == "200":
                print ("stg1 health check passed")
                status="0" #success
                break
            r = requests.get(urlbase,auth=('admin','dashai'),headers=headers )
            if str(r.status_code) == "200":
                print ("stg2 health check passed")
                status="1" 
            else: 
                status="2"
            fix="1"
            if fix == "0":
                if status == "1":
                    output=grafanacreds(grafana)
                    if "FAILED" in output:
                        return(output)                    
                elif status =="2":
                    return("BASE ACCOUNT LOST")
            else:
                break
        return("HEALTH CHECK FAILED")    
            
  
