#from __main__ import app
from gvar import events
from gvar import status
from gvar import project
from gvar import first
from common import *
from config import *
from headerloader import *


# @app.route("/")
# def main():
#         return render_template('index-ldr.html')

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=10)

@app.route("/")
def main():
    global project
    global events
    global first
    print(first)
    if session.get('logged_in') != True:
        session['logged_in'] = False
        login="0"
        return render_template('index.html',login=login)
    if session.get('logged_in'):
        project="1"
        print("logged in")
    if project == "1":
        #pod=pods()
        #dc=deployments()
        #cm=configmap()
        #svc=services()
        #routes=endpoints()
        login="1"
        #return render_template('index.html',allpods=pod,alldc=dc,allcm=cm,allsvc=svc,allroutes=routes,login=login,events=events,status=status)
        print(session['kubeconfig'])
        return render_template('index.html',login=login,events=events,status=status)
    else:
        login="0"
        return render_template('index.html',login=login)




@app.route('/collectors')
def collectors():
    if not session.get('logged_in'):
        error = "Log In First..."
        return render_template('auth.html', error=error)      
    else:
        command="oc get route grafana -o template --template {{.spec.host}} --config="+session['kubeconfig']
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        grafana = cmd.strip()
        if grafana == "":    
                error="Grafana Route Not Found During Health Check. Ensure You Are In The Right Project"
                return render_template('grafanahealth-hf.html', error=error) 
        else:
            creds=grafanacreds(grafana)    
            if "FAILED" in creds or "NOSVC" in creds:
                error=creds
                return render_template('grafanahealth-hf.html', error=error) 
            elif "LOST" in creds:
                error="LOST"
                return render_template('grafanahealth-hf.html', error=error) 
            else: 
                return render_template('collectors.html')

@app.route("/podtable")
def podtable():
        pod=pods()
        podstatus=errorcollector(pods)
        return render_template("podtable.html",podstatus=podstatus)
