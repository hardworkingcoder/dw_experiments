import urllib
import os
import uuid
import requests
import stripe
import json
import flask
from flask import Flask, render_template, request, redirect, session, url_for, g
from flask.ext.sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_failsafe import failsafe
import calendar
import time
import jinja2
app = Flask(__name__, static_url_path='/static')
app.config['PROPAGATE_EXCEPTIONS'] = True
app.jinja_loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates'))
socketio = SocketIO(app)
from threading import Thread
thread = None
from flask import send_from_directory
app.config.from_pyfile('_config.py')
db = SQLAlchemy(app)
import models
from sqlalchemy import and_
import calendar
import time
from flask_oauth import OAuth
import ast
oauth = OAuth()
from sqlalchemy.orm.attributes import flag_modified
import uuid
from flask import jsonify

@app.route('/login', strict_slashes=False)
def login():
    location = 'https://data.world/oauth/authorize?client_id=%s&redirect_uri=http://dw_experiments_dev.hardworkingcoder.com/dwoauth&response_type=code' % app.config['DATADOTWORLD_CLIENT_ID']
    return flask.redirect(location, code=302)

@app.route('/dwoauth', strict_slashes=False)
def dwoauth():
    print 'request args for dwoauth', request.args
    if 'access_token' in request.args:
        print 'Access token!', request.args
        return jsonify(request.args)
    code = request.args.get('code')
    
    url = 'https://data.world/oauth/authorize?code=%s&client_id=%s&client_secret=%s&redirect_uri=http://dw_experiments_dev.hardworkingcoder.com/dwoauth&grant_type=authorization_code' % (code, app.config['DATADOTWORLD_CLIENT_ID'], app.config['DATADOTWORLD_CLIENT_SECRET'].replace('#', '%23'))
    response = requests.get(url)
    print url
    try:
        print response.text
    except:
        print response.json()


@failsafe
def create_app():
    return app

import eventlet
eventlet.monkey_patch()
if __name__ == '__main__':
    socketio.run(create_app(), debug=True, port=5000)
