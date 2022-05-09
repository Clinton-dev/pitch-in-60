import os
from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "users.login"
login_manager.login_message_category = "warning"

mail = Mail(app)

from pitch.users.routes import users
from pitch.pitches.routes import pitches
from pitch.main.routes import main

app.register_blueprint(users)
app.register_blueprint(pitches)
app.register_blueprint(main)