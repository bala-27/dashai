#from __main__ import app
from common import *
from config import *
from endpoints import *
from flask import send_file

def importer_output(endpoint,db):
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
          hostname = ""
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
    output=(outputblock % (endpoint, db))
    return output;


def telegrafhostconfig():
    inputblock="""
            [[inputs.cpu]]
              percpu = true
              totalcpu = true
              collect_cpu_time = false
              report_active = false

            [[inputs.disk]]
              ignore_fs = ["tmpfs", "devtmpfs", "devfs"]
            [[inputs.diskio]]
            [[inputs.kernel]]
            [[inputs.mem]]
            [[inputs.processes]]
            [[inputs.swap]]
            [[inputs.system]]
            [[inputs.cgroup]]
            [[inputs.net]]
            [[inputs.net_response]]
            [[inputs.netstat]]
            [[inputs.conntrack]]
            """
    return inputblock;

def hostpoller(outblock,inblock):
    script="""
#!/bin/bash
rpm -ivh https://dl.influxdata.com/telegraf/releases/telegraf-1.5.2-1.x86_64.rpm
cat << EOF > /etc/telegraf/telegraf.conf
%s

%s
EOF
chkconfig telegraf on
service telegraf start
            """
    script=(script % (outblock, inblock))
    return script;

@app.route('/telegraf-ldr')
def telegrafldr():
    return render_template('telegraf/telegraf-loader.html')

def telegrafds():
      out=[]
      url="dashai-influxdb:8086"
      db="telegraf-agent"
      command="oc get route grafana -o template --template {{.spec.host}} --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      grafana = cmd.strip()
      out.append(deploy_DS_influx("telegraf-agent",url,db,grafana))
      out.append(deplpoy_dashboard("6",grafana))
      return out;

@app.route('/telegraf-build')
def telegrafconfig():
    input_telegraf=telegrafhostconfig()
    endpoint=influx_endpoint()
    output_block=importer_output(endpoint,"telegraf-agent")
    script=hostpoller(output_block,input_telegraf)
    text_file = open("/tmp/telegraf.conf", "w")
    text_file.write(script)
    text_file.close()
    rule = request.host
    rule = rule +"/telegrafget"
    out=telegrafds()
    return render_template('telegraf/telegraf.html', rule=rule, out=out)


@app.route('/telegrafget')
def telegrafget():
    path="/tmp/telegraf.conf"
    print(path)
    return send_file(path, as_attachment='True', mimetype='application/octet-stream')

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/telegraf-deploy')
def telegrafdeploy():
    return render_template('telegraf/telegraf-deploy.html')
