#from __main__ import app
from common import *
from config import *
from dashboards import *
from datasources import *

@app.route('/ocp')
def deployocp():
      global ocpver
      command="oc new-app prom/prometheus --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out1=prettyprint(cmd)
      #out1 = cmd
      if session['ocpversion'] == "3.7" :
          command="oc create -f https://raw.githubusercontent.com/dashai/dashai/master/configmaps/ocp37.yml --config="+session['kubeconfig']
          p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
          (cmd, err) = p.communicate()
          out2=prettyprint(cmd)
          session['ocpid']="4"
      elif session['ocpversion'] == "3.9" :
          command="oc create -f https://raw.githubusercontent.com/dashai/dashai/master/configmaps/ocp37.yml --config="+session['kubeconfig']
          p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
          (cmd, err) = p.communicate()
          out2=prettyprint(cmd)
          session['ocpid']="4"          
      elif session['ocpversion'] == "3.6" :
          command="oc create -f https://raw.githubusercontent.com/dashai/dashai/master/configmaps/ocp36.yml --config="+session['kubeconfig']
          p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
          (cmd, err) = p.communicate()
          out2=prettyprint(cmd)
          session['ocpid']="2"
      print ("ID:"+session['ocpid'])    
      command="oc volume dc/prometheus --add --overwrite --name=prom-k8s -m /etc/prometheus -t configmap --configmap-name=prom-k8s --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out3=prettyprint(cmd)
      #out3 = cmd
      command="oc expose service prometheus --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out4=prettyprint(cmd)
      #out4 = cmd
      command="oc get route grafana -o template --template {{.spec.host}} --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      grafana = cmd.strip()
      url=("prometheus:9090")
      out5=deploy_DS_prom(url,grafana)
      out6=deplpoy_dashboard(session['ocpid'],grafana)
      eventgen("OCP Deployed")
      return render_template('ocp/ocp.html',
                             out1=out1,
                             out2=out2,
                             out3=out3,
                             out4=out4,
                             out5=out5,
                             out6=out6
                             )

@app.route('/ocploader',methods = ['POST'])
def ocploader():
    global ocpver
    if request.method == 'POST':
      result = request.form
      ocpver = request.form.get('ocpver')
    return render_template('ocp/ocp-loader.html')

@app.route('/ocpdeploy')
def ocpdeploy():
    command = "oc version --config="+session['kubeconfig'] + " | grep openshift"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cmd, err) = p.communicate()
    version=cmd
    if "3.7" in version:
        session['ocpversion']="3.7" 
        version="3.7" 
    elif "3.6" in version:
        session['ocpversion']="3.6"
        version="3.6"                
    else:
        session['ocpversion']="3.7"
        version="3.7"
    #print (version)
    return render_template('ocp/ocp-deploy.html',version=version)
