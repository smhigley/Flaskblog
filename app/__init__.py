import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.pagedown import PageDown
from flask_oauth import OAuth
from config import basedir, location

# init app with config
app = Flask(__name__)
app.config.from_object('config')

# database with sqlalchemy
db = SQLAlchemy(app)

#markdown editor
pagedown = PageDown(app)

# login manager and social oauth logins
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
oauth = OAuth()

# add location setting to global config object
app.config['LOCATION'] = location;

from app import views, models
