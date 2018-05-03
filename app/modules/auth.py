#from __main__ import app
from common import *
from config import *
from headerloader import *
from main import *

@app.route("/logout")
def logout():
    global project
    session['logged_in'] = False
    command="oc logout"
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (cmd, err) = p.communicate()
    project="0"
    return main()

@app.route('/login')
def login():
    if session.get('logged_in'):
        flash('You Are Already Logged In')
        return render_template('auth.html')
    else:
        return render_template('login.html')

@app.route('/auth', methods=['GET', 'POST'])
def start():
    error=None
    global project
    global events
    global status
    if request.method == 'POST':
      ocpURL = request.form.get('ocpURL')
      ocpUID = request.form.get('ocpUID')
      ocpPID = request.form.get('ocpPID')
      ocpTKN = request.form.get('ocpTKN')
      if not ocpTKN:
          command="oc login https://"+ocpURL+" --insecure-skip-tls-verify=true -u '"+ocpUID+"' -p '"+ocpPID+"'"
          p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
          (cmd, err) = p.communicate()
          return_code = p.returncode
          print 'RETURN CODE', return_code
      else:
          if "oc login" and "token" not in ocpTKN:
            error = "Oh no! Something Went Wrong, Try Again..."
            return render_template('auth.html', error=error)
          else:
            if "insecure" in ocpTKN:  
                command=ocpTKN
                p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                (cmd, err) = p.communicate()
                return_code = p.returncode
                print 'RETURN CODE', return_code 
            else:
                command=ocpTKN+"  --insecure-skip-tls-verify=true"
                p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                (cmd, err) = p.communicate()
                return_code = p.returncode
                print 'RETURN CODE', return_code                 
      if return_code == 0:
          flash('You were successfully logged in. Deploy Base Components To Get Started If You Haven\'t Already!...')
          session['logged_in'] = True
          project="1"
          data = prettyprint(cmd)
          statusgen("Successful Login: "+ocpUID)
          command="oc project"
          p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
          (cmd, err) = p.communicate()
          eventgen(cmd)
          if "default" in cmd:
              defaultprojectwarn="1"
          else:
              defaultprojectwarn="0"
          x=random.randrange(0, 9999)
          session['kubeid'] = str(x)
          print(session['kubeid'])
          home = expanduser("~")
          os.rename(home+'/.kube/config', '/tmp/'+session['kubeid']+'.config')
          session['kubeconfig'] = '/tmp/'+session['kubeid']+'.config'
          return render_template('auth.html', error=error, cmd=cmd, data=data,defaultprojectwarn=defaultprojectwarn)
      else:
        error = "Oh no! Something Went Wrong, Try Again..."
        return render_template('auth.html', error=error)
    else:
        error = "Oh no! Something Went Wrong, Try Again..."
        return render_template('auth.html', error=error) 
