from flask import *
from PIL import Image  
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import psycopg2
from datetime import datetime
from random import *
from flask_socketio import SocketIO, join_room, send, emit, leave_room
from time import localtime, strftime
from matcha.orm.data_access import DataAccess
from matcha.model.Users import Users
from matcha.model.Connection import Connection
import logging
from pickle import NONE
from matcha.model.Room import Room
from matcha.model.Message import Message
from flask import render_template
# from routes import *
# from matcha.web import routes
# app.register_blueprint(routes)

# from flask import Blueprint
# routes = Blueprint('routes', __name__)


app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = 'd66HR8dç"f_-àgjYYic*dh'
app.debug = True  # a supprimer en production
socketio = SocketIO(app)
ROOMS = ["lounge", "news", "games", "coding"]

# # Lance les serveurs
# if __name__ == '__main__':
    # socketio.run(app)
