import os

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.github import GitHub

from config import basedir

app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object('config')

db = SQLAlchemy(app)
github = GitHub(app)

# login module
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

oid = OpenID(app, os.path.join(basedir, 'tmp'))

# views refer app, so call this after defining app
from app_server import views





