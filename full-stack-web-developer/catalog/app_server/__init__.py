import os

from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from flask.ext.sqlalchemy import SQLAlchemy

from config import basedir

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# login module
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

oid = OpenID(app, os.path.join(basedir, 'tmp'))

# views refer app, so call this after defining app
from app_server import views





