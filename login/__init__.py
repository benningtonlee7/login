from flask import Flask
from login.config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from oauthlib.oauth2 import WebApplicationClient
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db, compare_type=True)
login = LoginManager(app)
login.login_view = "google.login"
client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)


from login.resources.ProfileResources import Profile
from login import routes, errors

