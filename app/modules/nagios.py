#from __main__ import app
from common import *
from config import *
from gvar import *
from datasources import *
from dashboards import *

@app.route('/nagios-deploy')
def nagiosdeploy():
    return render_template('nagios/nagios-deploy.html')

@app.route('/nagiosloader')
def nagiosload():
    return render_template('nagios/nagios-loader.html')


def nagios_grafana():
      url="dashai-influxdb:8086"
      db="dashainagflux"
      command="oc get route grafana -o template --template {{.spec.host}} --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      grafana=cmd
      o1=deploy_DS_influx("dashai-nagflux",url,db,grafana)
      eventgen(o1)
      o2=deplpoy_dashboard("3",grafana)
      eventgen(o2)
      return;


@app.route('/nagios')
def nagios():
      command="oc new-app https://github.com/alyarctiq/dashai-mariadb --name dashai-mariadb --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out1=prettyprint(cmd)

      command="oc new-app https://github.com/alyarctiq/dashai-gearman --name dashai-gearman --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out2=prettyprint(cmd)

      command="oc new-app https://github.com/alyarctiq/dashai-modworker --name dashai-modworker --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out3=prettyprint(cmd)

      command="oc new-app https://github.com/alyarctiq/dashai-nagflux --name dashai-nagflux --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out4=prettyprint(cmd)

      command="oc new-app https://github.com/alyarctiq/dashai-nagios --name dashai-nagios --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out5=prettyprint(cmd)

      command="oc expose svc dashai-nagios --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out7 =prettyprint(cmd)

      nagios_grafana()

      out6 = 'INFO: This deployment will take a bit of time to build, please be patient :) '
      eventgen("Nagios Deployed")
      eventgen("INFO: Nagios deployment will take a bit of time to build, please be patient")
      return render_template('nagios/nagios.html',
                             out1=out1,
                             out2=out2,
                             out3=out3,
                             out4=out4,
                             out5=out5,
                             out6=out6
                             )
