#from __main__ import app
from common import *
from config import *

def influx_endpoint():
    command = "oc get routes dashai-influxdb -o template --template {{.spec.host}} --config="+session['kubeconfig']
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cmd, err) = p.communicate()
    return cmd;
