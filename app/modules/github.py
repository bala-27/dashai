#from __main__ import app
from common import *
from config import *
from gvar import *
from datasources import *
from dashboards import *

@app.route('/github-deploy')
def githubdeploy():
    return render_template('github/github-deploy.html')

@app.route('/githubloader')
def githubloader():
    if request.method == 'POST':
       return render_template('github/github-loader.html')

@app.route('/githubinfo')
def githubinfo():
    return render_template('github/github-info.html')


@app.route('/deploygithub_stg1',methods = ['POST', 'GET'])
def deploygithub_stg1():
    global repos
    global gittoken
    if request.method == 'POST':
      result = request.form
      repos = request.form.get('repos')
      gittoken = request.form.get('token')
      gitapi = request.form.get('api')
      if repos == '' :
           return render_template('github/github-info.html', error="Required Repo Missing")     
    return render_template('github/github-loader.html')

@app.route('/deploygithub_stg2')
def deploygithub_stg2():
    global repos
    global gittoken
    out1=""
    out2=""
    out3=""
    out4=""
    out5=""
    out6=""
    out7=""

    command="oc get routes prometheus -o template --template {{.spec.host}} --config="+session['kubeconfig']
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cmd, err) = p.communicate()
    out1=prettyprint(cmd)
    
    if out1:
        out1=prettyprint("Promethes TSBD Appears To Already Be Running..Not Overwriting ConfigMap")
    else :
        command="oc new-app prom/prometheus --config="+session['kubeconfig']
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        out1=prettyprint(cmd)
        
        command="oc create -f https://raw.githubusercontent.com/alyarctiq/configmaps/master/githubexp.yml --config="+session['kubeconfig']
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        out2=prettyprint(cmd)
        
        command="oc volume dc/prometheus --add --name=prom-k8s -m /etc/prometheus -t configmap --configmap-name=github-k8s --config="+session['kubeconfig']
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        out3=prettyprint(cmd)

        command="oc expose svc/prometheus  --config="+session['kubeconfig']
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
    
    if out2 == "":
        out2="Not Requried"
    if out3 == "":
        out2="Not Requried"

    command = "oc create -f https://raw.githubusercontent.com/alyarctiq/dashai-github/master/dashai-github.yml --config="+session['kubeconfig']
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cmd, err) = p.communicate()
    out4 = prettyprint(cmd)

    command = 'oc set env dc/dashai-github REPOS="'+repos+'" --config='+session['kubeconfig']
    print command
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cmd, err) = p.communicate()
    out5 = cmd
    
    if gittoken != "" :
        command = 'oc set env dc/dashai-github GITHUB_TOKEN="'+gittoken+'" --config='+session['kubeconfig']
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        out5 = cmd

    command="oc get route grafana -o template --template {{.spec.host}} --config="+session['kubeconfig']
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cmd, err) = p.communicate()
    grafana = cmd.strip()
    url=("prometheus:9090")
    out6=deploy_DS_prom(url,grafana)
    id="7"
    out7=deplpoy_dashboard(id,grafana)
    eventgen("GitHub Collector Deployed")
    return render_template('github/github.html',
                           out1=out1,
                           out2=out2,
                           out3=out3,
                           out4=out4,
                           out5=out5,
                           out6=out6,
                           out7=out7
                             )