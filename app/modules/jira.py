#from __main__ import app
from common import *
from config import *
from gvar import *
from datasources import *
from dashboards import *

@app.route('/jirainfo')
def jirainfo():
    return render_template('jira/jira-info.html')

@app.route('/jiraqueryexample')
def jiraqueryexample():
    return render_template('jira/jiraqueryexample.html')

@app.route('/deployjira_stg1',methods = ['POST', 'GET'])
def deployjira_stg1():
    global jiraURL
    global jiraUID
    global jiraPID
    global jiraQRY
    if request.method == 'POST':
      result = request.form
      jiraURL = request.form.get('jiraURL')
      jiraUID = request.form.get('jiraUID')
      jiraPID = request.form.get('jiraPID')
      jiraQRY = request.form.get('jiraQRY')
    return render_template('jira/jira-loader.html')

@app.route('/deployjira_stg2')
def deployjira_stg2():
      global jiraURL
      global jiraUID
      global jiraPID
      global jiraQRY
      influxDB = "dashai-jira"
      command="oc get routes dashai-influxdb -o template --template {{.spec.host}} --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      influxURL = cmd
      jiraBlock="""
    {
      "jiraUrl": "https://%s",
      "jiraUsername": "%s",
      "jiraPassword": "%s",
      "jiraPauseMilliseconds": 500,
      "influxUrl": "http://%s",
      "influxDB": "%s",
      "influxUsername": "",
      "influxPassword": "",
      %s
    }
      """
      output=(jiraBlock % (jiraURL, jiraUID, jiraPID, influxURL, influxDB, jiraQRY ))
      text_file = open("/tmp/config.json", "w")
      text_file.write(output)
      text_file.close()
      command="oc new-app https://github.com/alyarctiq/dashai-jira --name=dashai-jira --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out1=prettyprint(cmd)
      command = "oc delete secret jira-tokens --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out2 = cmd
      command = "oc create secret generic jira-tokens --from-file=/tmp/config.json --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out3 = cmd
      command = "oc volume dc/dashai-jira --add --type=secret --secret-name=jira-tokens -m /go/src/app/ --config="+session['kubeconfig']
      call(command, shell=True)
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out4 = cmd
      eventgen("JIRA Deployed")
      return render_template('jira/jira.html',
                             out1=out1,
                             out2=out2,
                             out3=out3,
                             out4=out4
                             )

@app.route('/jira-deploy')
def jiradeploy():
    return render_template('jira/jira-deploy.html')
