#from __main__ import app
from gvar import events
from gvar import status
from gvar import project
from common import *
from config import *
from headerloader import *

@app.route('/endpoints')
def endpoints():
    global project
    print(project)
    if session.get('logged_in'):
        route=""
        routeslist=[]
        index=0
        command = "oc get routes -o name --config="+session['kubeconfig']
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        text_file = open("/tmp/dashai-routes", "w")
        text_file.write(cmd)
        text_file.close()
        with open("/tmp/dashai-routes") as f:
            while True:
                line = f.readline()
                if not line: break
                command = "oc get -o template --template {{.spec.host}} "+line + " --config="+session['kubeconfig']
                p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                (cmd, err) = p.communicate()
                route+=cmd+";"
                index += 1
        routes=route.split(";")
        for i in range(0,index):
            #print(routes[i])
            routeslist.append(routes[i])
        os.remove("/tmp/dashai-routes")
        return(routeslist)
    else:
        routeslist=[]
        routeslist.append("NA")
        return(routeslist)

@app.route('/services')
def services():
    global project
    if session.get('logged_in'):
        index=0
        command = "oc get services -o name --config="+session['kubeconfig']
        svc=[]
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        text_file = open("/tmp/dashai-services", "w")
        text_file.write(cmd)
        text_file.close()
        with open("/tmp/dashai-services") as f:
            while True:
                line = f.readline()
                if not line: break
                svc.append(line)
        os.remove("/tmp/dashai-services")
        return (svc)
    else:
        svc=[]
        svc.append("NA")
        return (svc)

@app.route('/configmap')
def configmap():
    global project
    if session.get('logged_in'):
        index=0
        command = "oc get configmap -o name --config="+session['kubeconfig']
        cm=[]
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        text_file = open("/tmp/dashai-configmap", "w")
        text_file.write(cmd)
        text_file.close()
        with open("/tmp/dashai-configmap") as f:
            while True:
                line = f.readline()
                if not line: break
                cm.append(line)
        os.remove("/tmp/dashai-configmap")
        return (cm)
    else:
        cm=[]
        cm.append("NA")
        return (cm)

@app.route('/deployments')
def deployments():
    global project
    if session.get('logged_in'):
        index=0
        dc=[]
        command = "oc get dc -o name --config="+session['kubeconfig']
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        text_file = open("/tmp/dashai-deployments", "w")
        text_file.write(cmd)
        text_file.close()
        with open("/tmp/dashai-deployments") as f:
            while True:
                line = f.readline()
                if not line: break
                dc.append(line)
        os.remove("/tmp/dashai-deployments")
        return (dc)
    else:
        dc=[]
        dc.append("NA")
        return (dc)

@app.route('/pods')
def pods():
    global project
    if session.get('logged_in'):
        index=0
        pods = []
        command = "oc get pods -o name --config="+session['kubeconfig']
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        text_file = open("/tmp/dashai-pods", "w")
        text_file.write(cmd)
        text_file.close()
        with open("/tmp/dashai-pods") as f:
            while True:
                line = f.readline()
                if not line: break
                pods.append(line)
        text_file.close()
        os.remove("/tmp/dashai-pods")
        return (pods)
    else:
        pods = []
        pods.append("NA")
        return (pods)

def getdcs():
    global project
    dc = []
    if session.get('logged_in'):
        index=0
        command = "oc get dc -o name --config="+session['kubeconfig']
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        text_file = open("/tmp/dashai-dc", "w")
        text_file.write(cmd)
        text_file.close()
        with open("/tmp/dashai-dc") as f:
            while True:
                line = f.readline()
                if not line: break
                dc.append(line)
                print(line)
        os.remove("/tmp/dashai-dc")
        print(dc)
        return (dc)
    else:
        dc = []
        dc.append("NA")
        return (dc)
