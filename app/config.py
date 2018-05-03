from __future__ import print_function
from flask import Flask, render_template, request, redirect, flash, session, send_file, app
import random
import os
import time
import datetime
import httplib2
import json
import requests
import urllib
import dateutil.parser as parser
from dateutil.tz import tzlocal
from subprocess import call
import subprocess
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from datetime import datetime, date, time, timedelta
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from os.path import expanduser

app = Flask(__name__)
app.config["CACHE_TYPE"] = "null"
#app.secret_key = os.urandom(24)
app.secret_key = "sLiwAg4AX6L30vm"


import modules.core
import modules.apache
import modules.auth
import modules.projects
import modules.common
#import modules.config
import modules.dashboards
import modules.datasources
import modules.endpoints
import modules.gsheets
import modules.headerloader
import modules.jenkins
import modules.jira
import modules.nagios
import modules.ocp
import modules.teardown
import modules.telegraf
import modules.main
import modules.gvar
import modules.github
import modules.main
