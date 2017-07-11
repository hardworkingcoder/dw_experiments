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
import requests
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(uuid):
    return User.query.get(uuid)

@app.route('/login', strict_slashes=False)
def login():
    location = 'https://data.world/oauth/authorize?client_id=%s&redirect_uri=https://dw_experiments_dev.hardworkingcoder.com/dwoauth&response_type=code' % app.config['DATADOTWORLD_CLIENT_ID']
    return flask.redirect(location, code=302)

def get_access_info(code):
    params = {
      'code': code,
      'client_id': app.config['DATADOTWORLD_CLIENT_ID'],
      'client_secret': app.config['DATADOTWORLD_CLIENT_SECRET'].replace('#', '%23'),
      'grant_type': 'authorization_code'
    }
    params_as_str = '&'.join(['='.join(pair) for pair in params.items()])
    url = 'https://data.world/oauth/access_token?%s' % (params_as_str)
    response = requests.post(url)
    return response.json()

def get_user_info(access_token):
    url = "https://api.data.world/v0/user"
    payload = "{}"
    headers = {'authorization': 'Bearer <<%s>>' % (access_token)}
    response = requests.request("GET", url, data=payload, headers=headers)
    return response.json()

def update_db_with_access_and_user_info(access_info, user_info):
    user_exists = db.session.query(models.User.social_id).filter_by(social_id=user_info['id']).scalar() is not None
    if user_exists:
        user = models.User.query.filter_by(social_id=user_info['id']).first()
        ddw_access_token = access_info['access_token']
        ddw_token_expires_in = access_info['expires_in']
        ddw_avatar_url = user_info['avatarUrl']
        nickname = user_info['displayName']
        ddw_user_updated = user_info['updated']
        db.session.commit()
    else:
        user = models.User(ddw_access_token=access_info['access_token'], ddw_token_expires_in=access_info['expires_in'], ddw_avatar_url=user_info['avatarUrl'], nickname=user_info['displayName'], social_id=user_info['id'], ddw_user_created=user_info['created'], ddw_user_updated=user_info['updated'])
        db.session.add(user)
        db.session.commit()
    return user

def update_db_session_for_user(user):
    session_row = models.Session(id = user.id)
    db.session.add(session_row)
    db.session.commit()
    return session_row

row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

@app.route('/dwoauth', strict_slashes=False)
def dwoauth():
    access_info = get_access_info(request.args.get('code'))
    user_info = get_user_info(access_info['access_token'])
    user = update_db_with_access_and_user_info(access_info, user_info)
    login_user(user, True)
    return flask.redirect('/', code=302)

@app.route('/logout', strict_slashes=False)
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/', strict_slashes=False)
def index():
    return send_from_directory('static', 'index.html')

@failsafe
def create_app():
    return app

import eventlet
eventlet.monkey_patch()
if __name__ == '__main__':
    socketio.run(create_app(), debug=True, port=5000)
