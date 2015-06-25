import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
# from flask.ext.openid import OpenID
from flask_oauth import OAuth
from config import basedir, location

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# oid = OpenID(app, os.path.join(basedir, 'tmp'), safe_roots=[])
oauth = OAuth()

app.config['LOCATION'] = location;

from app import views, models
