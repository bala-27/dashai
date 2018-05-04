#from __main__ import app
from common import *
from config import *
from gvar import *
from datasources import *
from endpoints import *

@app.route('/apache-info')
def apacheinfo():
    return render_template('apache/apache-info.html')

@app.route('/apache-deploy')
def apachedeploy():
    return render_template('apache/apache-deploy.html')


@app.route('/deployapache_stg1',methods = ['POST', 'GET'])
def deployapache():
    global apacheURL
    global apacheUID
    global apachePID
    global apacheID
    if request.method == 'POST':
      result = request.form
      apacheURL = request.form.get('apacheURL')
      apacheUID = request.form.get('apacheUID')
      apachePID = request.form.get('apachePID')
      apacheID = request.form.get('apacheID')
    return render_template('apache/apache-loader.html')

def apache_secrets():
    secrets=[]
    command = "oc delete secret apache-tokens --config="+session['kubeconfig']
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cmd, err) = p.communicate()
    out1=prettyprint(cmd)
    secrets.append(out1)
    command = "oc create secret generic apache-tokens --from-file=/tmp/telegraf.conf --config="+session['kubeconfig']
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cmd, err) = p.communicate()
    out1=prettyprint(cmd)
    secrets.append(out1)
    command = "oc volume dc/dashai-apache --add --type=secret --secret-name=apache-tokens -m /etc/telegraf/  --config="+session['kubeconfig']
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cmd, err) = p.communicate()
    out1=prettyprint(cmd)
    secrets.append(out1)
    os.remove("/tmp/telegraf.conf")
    return secrets;

def importer_output_apache(hostID,endpoint,db):
    outputblock="""
        [agent]
          interval = "10s"
          round_interval = true
          metric_batch_size = 1000
          metric_buffer_limit = 10000
          collection_jitter = "0s"
          flush_interval = "10s"
          flush_jitter = "0s"
          precision = ""
          logfile = ""
          hostname = \"%s\"
          omit_hostname = false

        [[outputs.influxdb]]
          urls = ["http://%s"] # required
          database = \"%s\"
          retention_policy = ""
          write_consistency = "any"
          timeout = "5s"
          # username = "telegraf"
          # password = "metricsmetricsmetricsmetrics"
          # user_agent = "telegraf"
          # udp_payload = 512
          ## Optional SSL Config
          # ssl_ca = "/etc/telegraf/ca.pem"
          # ssl_cert = "/etc/telegraf/cert.pem"
          # ssl_key = "/etc/telegraf/key.pem"
          ## Use SSL but skip chain & host verification
          # insecure_skip_verify = false
     """
    output=(outputblock % (hostID,endpoint, db))
    return output;

@app.route('/deployapache_stg2')
def deployapache_stg2():
    global apacheURL
    global apacheUID
    global apachePID
    global apacheID

    output=[]
    apache="""
        [[inputs.apache]]
          urls = ["%s"]

          ## Credentials for basic HTTP authentication.
          username = "%s"
          password = "%s"

          ## Maximum time to receive response.
          # response_timeout = "5s"

          ## Optional SSL Config
          # ssl_ca = "/etc/telegraf/ca.pem"
          # ssl_cert = "/etc/telegraf/cert.pem"
          # ssl_key = "/etc/telegraf/key.pem"
          ## Use SSL but skip chain & host verification
          # insecure_skip_verify = false
          """
    input_apache=(apache % (apacheURL, apacheUID, apachePID))
    endpoint=influx_endpoint()
    output_block=importer_output_apache(apacheID,endpoint,"dashai-apache")
    text_file = open("/tmp/telegraf.conf", "w")
    text_file.write(output_block)
    text_file.write(input_apache)
    text_file.close()
    command="oc new-app https://github.com/dashai/dashai/tree/master/collectors/dashai-importer --name=dashai-apache  --config="+session['kubeconfig']
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cmd, err) = p.communicate()
    out1=prettyprint(cmd)
    output.append(out1)
    out2=apache_secrets()
    output.append(out2)
    command="oc get route -o yaml  --config="+session['kubeconfig'] + "| grep host | grep -v openshift | grep grafana | cut -d':' -f 2|uniq"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cmd, err) = p.communicate()
    grafana = cmd.strip()
    url="dashai-influxdb:8086"
    db="dashai-apache"
    out3=deploy_DS_influx("dashai-apache",url,db,grafana)
    output.append(out3)
    out4=deplpoy_dashboard("5",grafana)
    output.append(out4)
    return render_template('apache/apache.html',output=output);
