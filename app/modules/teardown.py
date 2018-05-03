#from __main__ import app
from common import *
from config import *
from gvar import *
from datasources import *
from dashboards import *
from headerloader import *

@app.route('/teardownlist')
def teardown():
    if session.get('logged_in'):
        return render_template('teardownlist.html')
    else:
        error = "Log In First..."
        return render_template('auth.html', error=error)

@app.route('/listdc')
def listdc():
    if session.get('logged_in'):
        dc=deployments()
        return render_template('teardowntable.html', dc=dc)

@app.route('/teardownconfirm',methods = ['POST'])
def teardownconfirm():
        if request.method == 'POST':
            deletethese=[]
            result = request.form
            d1ID = request.form.get('dc')
            temp=d1ID.split("/")
            ID=temp[1]
            ID=ID.strip()
            dc=deployments()
            for d1 in dc:
                d1=d1.strip()
                if ID in d1:
                    deletethese.append(d1)
            pod=pods()
            for p1 in pod:
                p1=p1.strip()
                if ID in p1:
                    deletethese.append(p1)
            svc=services()
            for s1 in svc:
                s1=s1.strip()
                if ID in s1:
                    deletethese.append(s1)
            routes=endpoints()
            for r1 in routes:
                r1=r1.strip()
                if ID in r1:
                    r1="routes/"+r1
                    deletethese.append(r1)
        return render_template('teardownconfirm.html', d1ID=d1ID, ID=ID, deletethese=deletethese)


@app.route('/teardowndelete',methods = ['POST'])
def teardowndelete():
        if request.method == 'POST':
            deletethese=[]
            deleted=[]
            result = request.form
            d1ID = request.form.get('dc')
            temp=d1ID.split("/")
            ID=temp[1]
            ID=ID.strip()
            dc=deployments()
            i=0
            for d1 in dc:
                d1=d1.strip()
                if ID in d1:
                    deletethese.append(d1)
            pod=pods()
            for p1 in pod:
                p1=p1.strip()
                if ID in p1:
                    deletethese.append(p1)
            svc=services()
            for s1 in svc:
                s1=s1.strip()
                if ID in s1:
                    deletethese.append(s1)
            routes=endpoints()
            for r1 in routes:
                r1=r1.strip()
                if ID in r1:
                    r1="routes/"+r1
                    deletethese.append(r1)
            for delete in deletethese:
                  command="oc delete " + delete + " --config="+session['kubeconfig']
                  p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
                  (cmd, err) = p.communicate()
                  cmd=cmd.strip()
                  if cmd != "":
                      deleted.append(prettyprint(cmd))
        return render_template('teardowndeleted.html',deleted=deleted)

@app.route('/teardowncollector',methods = ['POST'])
def teardowncollector():
        if request.method == 'POST':
            result = request.form
            d1ID = request.form.get('dc')
        return d1ID;
