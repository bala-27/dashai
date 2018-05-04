#from __main__ import app
from common import *
from config import *

@app.route('/coreload')
def coreload():
    if not session.get('logged_in'):
        error = "Log In First..."
        return render_template('auth.html', error=error)
    else:
        return render_template('core-loader.html')


@app.route('/deploycore')
def deploycore():
      command="oc whoami --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      if err:
          statusgen("Error Caputred: "+err )
      out1=prettyprint(cmd)
      command="oc project --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out2=prettyprint(cmd)
      if err:
          eventgen("Error Caputred: "+err )
      command="oc adm policy add-scc-to-user anyuid -z default --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out3=prettyprint(cmd)
      if err:
          eventgen("Error Caputred: "+err )
      command="oc adm policy add-cluster-role-to-user cluster-reader -z default --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out4=prettyprint(cmd)
      if err:
          eventgen("Error Caputred: "+err )
      command="oc new-app https://github.com/dashai/dashai/tree/master/collectors/dashai-grafana-ocp--name grafana --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out5=prettyprint(cmd)
      
      command="oc create -f https://raw.githubusercontent.com/dashai/dashai/master/configmaps/grafana-config.yml --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out6=prettyprint(cmd)

      command="oc volume dc/grafana --add --name=grafana-config -m /etc/grafana -t configmap --configmap-name=grafana-config --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out7=prettyprint(cmd)
      
      command="oc expose service grafana --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out8=prettyprint(cmd)
      if err:
          eventgen("Error Caputred: "+err )
      command="oc new-app https://github.com/dashai/dashai/tree/master/collectors/dashai-influxdb --name dashai-influxdb --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out9=prettyprint(cmd)
      command="oc expose svc dashai-influxdb --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()

      if err:
          eventgen("Error Caputred: "+err )
      call(command, shell=True)
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out10=prettyprint(cmd)
      if err:
          eventgen("Error Caputred: "+err )
      eventgen("Core Componets Deployed")
      return render_template('core.html',
                             out1=out1,
                             out2=out2,
                             out3=out3,
                             out4=out4,
                             out5=out5,
                             out6=out6,
                             out7=out7,
                             out8=out8,
                             out9=out9,
                             out10=out10
                             )

@app.route('/core')
def core():
    if not session.get('logged_in'):
        error = "Log In First..."
        return render_template('auth.html', error=error)
    return render_template('core-deploy.html')
