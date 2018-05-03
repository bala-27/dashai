#from __main__ import app
from common import *
from config import *
from gvar import *
from datasources import *
from dashboards import *

def get_docID(rawurl):
    url=rawurl.split("/")
    docId=url[5]
    return docId;

def get_client_token():
    credential_path = ('/dashai/token/client_secret.json')
    return credential_path

def get_private_token():
    credential_path = ('/dashai/token/token.json')
    return credential_path

@app.route('/getauthcode')
def getauthcode_stg1():
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    REDIRECT_URI='urn:ietf:wg:oauth:2.0:oob'
    REFRESH_TOKEN = "refresh_token"
    credential_path = '/dashai/token/client_secret.json'
    flow = client.flow_from_clientsecrets(credential_path, SCOPES, REDIRECT_URI)
    flow.params['access_type'] = 'offline'
    flow.params['state'] = 'state-token'
    auth_uri = flow.step1_get_authorize_url()
    return redirect(auth_uri)

def getauthcode_stg2(auth_code):
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
    REDIRECT_URI='urn:ietf:wg:oauth:2.0:oob'
    REFRESH_TOKEN = "refresh_token"
    credential_path = ('/dashai/token/client_secret.json')
    flow = client.flow_from_clientsecrets(credential_path, SCOPES, REDIRECT_URI)
    flow.params['access_type'] = 'offline'
    flow.params['state'] = 'state-token'
    credentials = flow.step2_exchange(auth_code)
    http_auth = credentials.authorize(httplib2.Http())
    storage = Storage('/dashai/token/token-primary.json')

    storage.put(credentials)
    credentials = storage.get()
    with open('/dashai/token/token-primary.json') as data_file:
        data = json.load(data_file)
    token=(data['token_response'])
    now=datetime.now(tzlocal())+timedelta(hours=1)
    now_1hr=(now.isoformat())
    token['expiry'] = now_1hr
    token_path = ('/dashai/token/token.json')
    with open(token_path,'w') as outfile:
        json.dump(token,outfile)

@app.route('/sheets-deploy')
def sheetsdeploy():
    return render_template('sheets/sheets-deploy.html')

@app.route('/sheetsloader')
def sheetsloader():
    if request.method == 'POST':
       return render_template('sheets/sheets-loader.html')

@app.route('/sheetsinfo')
def sheetsinfo():
    return render_template('sheets/sheets-info.html')


@app.route('/deploysheets_stg1',methods = ['POST', 'GET'])
def deploysheets_stg1():
    global docId
    global authcode
    if request.method == 'POST':
      result = request.form
      docID = request.form.get('docID')
      authcode = request.form.get('authcode')
      docId=get_docID(docID)
      getauthcode_stg2(authcode)
    return render_template('sheets/sheets-loader.html')

@app.route('/deploysheets_stg2')
def deploysheets_stg2():
      global docId
      global authcode
      client_token_path=get_client_token()
      private_token_path=get_private_token()
      command = "oc new-app https://github.com/alyarctiq/dashai-sheet-importer --name dashai-sheets -e DOC_ID='"+docId+"' --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out1 = prettyprint(cmd)
      command = "oc delete secret sheets-tokens --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out2 = cmd
      command = "oc create secret generic sheets-tokens --from-file=" + client_token_path +" --from-file=" + private_token_path + " --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out3 = cmd
      command = "oc volume dc/dashai-sheets --add --type=secret --secret-name=sheets-tokens -m /go/src/app/ --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      out4 = cmd
      url="dashai-influxdb:8086"
      db="DashAiSheets"
      command="oc get route grafana -o template --template {{.spec.host}} --config="+session['kubeconfig']
      p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
      (cmd, err) = p.communicate()
      grafana = cmd.strip()
      out5=deploy_DS_influx("sheets",url,db,grafana)
      out6=deplpoy_dashboard("1",grafana)
      eventgen("Sheets Deployed")
      return render_template('sheets/sheets.html',
                             out1=out1,
                             out2=out2,
                             out3=out3,
                             out4=out4,
                             out5=out5,
                             out6=out6
                             )
