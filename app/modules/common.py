#from __main__ import app
from common import *
from config import *
from gvar import *
from datasources import *
from dashboards import *

def timenow():
    timenowis=datetime.datetime.now()
    return(timenowis)

def statusgen(st):
     global status
     status.append(st)
     return(status)

def eventgen(event):
     global events
     events.insert(0,event)
     return(events)

def prettyprint(cmd):
    data = []
    text_file = open("/tmp/dashai-printer", "w")
    text_file.write(cmd)
    text_file.close()
    with open("/tmp/dashai-printer") as f:
        while True:
            line = f.readline()
            if not line: break
            data.append(line)
    text_file.close()
    #os.remove("/tmp/dashai-printer")
    return (data)

def errorcollector(pods):
    if session.get('logged_in'):
        index=0
        while True:
            try:
                podstatus=[]
                for pod in pods():
                    podstatus.append([])
                    print("pod>>>>"+pod)
                    line = pod.replace("\n", " ")
                    command = "oc get "+line+" -o json --config="+session['kubeconfig']
                    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                    (cmd, err) = p.communicate()
                    return_code = p.returncode
                    print 'RETURN CODE', return_code                 
                    if return_code == 0:
                        text_file = open("/tmp/dashai-podstatus", "w")
                        text_file.write(cmd)
                        text_file.close()
                        data = json.load(open('/tmp/dashai-podstatus'))

                        if "containerStatuses" not in data["status"]:
                            name=(data["metadata"]["name"])
                            podstatus[index].append(name)
                            print("hit")
                            state=(data["status"]["conditions"][0]["reason"])
                        else:
                            name=(data["status"]["containerStatuses"][0]["name"])
                            state=(data["status"]["containerStatuses"][0]["state"])
                            if "build" not in name:
                                if "deployment" in name:
                                    name=(data["metadata"]["name"])
                                    podstatus[index].append(name)
                                else:
                                    podstatus[index].append(data["status"]["containerStatuses"][0]["name"])
                            else:
                                podstatus[index].append(line)

                        if "waiting" in state:
                            if data["status"]["containerStatuses"][0]["state"]["waiting"]["reason"]:
                                podstatus[index].append(data["status"]["containerStatuses"][0]["state"]["waiting"]["reason"])
                            else:
                                podstatus[index].append("Waiting")
                        elif "terminated" in state:
                            if "reason" in data["status"]["containerStatuses"][0]["state"]["terminated"]:
                                podstatus[index].append(data["status"]["containerStatuses"][0]["state"]["terminated"]["reason"])
                            else:
                                podstatus[index].append("Terminated")
                        elif "Unschedulable" in state:
                            if data["status"]["conditions"][0]["reason"]:
                                podstatus[index].append(data["status"]["conditions"][0]["reason"])
                            else:
                                podstatus[index].append("Unschedulable")
                        elif "running" in state:
                            podstatus[index].append("Running")
                        else:
                            podstatus[index].append("NA")
                        index=index+1
                    else:
                        print("Bad Pod")
            except:
                continue
            break                
        return podstatus;
    else:
        return

@app.route("/getstatusinfo")
def getstatusinfo():
    if session.get('logged_in'):
        command = "oc config current-context --config="+session['kubeconfig']+"| cut -d '/' -f 3"
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        whoami=cmd
        command = "oc config current-context --config="+session['kubeconfig']+"| cut -d '/' -f 1"
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        project=cmd
        command = "oc config current-context --config="+session['kubeconfig']+"| cut -d '/' -f 2"
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        endpoint=cmd
        command = "oc version --config="+session['kubeconfig']+"| grep openshift"
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        version=cmd
        return render_template('status.html',whoami=whoami,project=project,endpoint=endpoint,version=version)
    else:
        return

def getprojects():
    if session.get('logged_in'):
        return
