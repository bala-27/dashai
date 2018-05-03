#from __main__ import app
from common import *
from config import *
from headerloader import *
from main import *

@app.route("/projects")
def projects():
    if session.get('logged_in'):
        projects=[]
        command="oc get project -o name --config="+session['kubeconfig']
        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (cmd, err) = p.communicate()
        text_file = open("/tmp/dashai-projects", "w")
        text_file.write(cmd)
        text_file.close()
        with open("/tmp/dashai-projects") as f:
            while True:
                line = f.readline()
                if not line: break
                projects.append(line)
        os.remove("/tmp/dashai-projects")
        return render_template('projecttable.html', projects=projects)
    else:
        error = "Log In First..."
        return render_template('auth.html', error=error)

@app.route('/projectchg',methods = ['POST'])
def projectchg():
    if request.method == 'POST':
        result = request.form
        project = request.form.get('project')
        projectschg=[]
        if project != "new":
            temp=project.split("/")
            project=temp[1]
            project=project.strip()            
            command="oc project " + project + " --config="+session['kubeconfig']
            print(command)
            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (cmd, err) = p.communicate()
            projectschg.append(cmd)
            return render_template('projectchanged.html', projectschg=projectschg)
        else:
            result = request.form
            project = request.form.get('newproject')
            project=project.strip()
            project=project.lower()
            command="oc new-project " + project + " --config="+session['kubeconfig']
            print(command)
            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
            (cmd, err) = p.communicate()
            text_file = open("/tmp/dashai-projects", "w")
            text_file.write(cmd)
            text_file.close()
            with open("/tmp/dashai-projects") as f:
                while True:
                    line = f.readline()
                    if not line: break
                    projectschg.append(line)
                os.remove("/tmp/dashai-projects")
            return render_template('projectchanged.html', projectschg=projectschg)
