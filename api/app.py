import os

from flask import Flask, g
from flask_cors import CORS
from flask_login import LoginManager

from db import DATABASE, initialize
from models.record import Record
from models.favorite import Favorite
from models.user import User
from models.marketplace import Marketplace
from models.message import Message
from resources.records import recordBP
from resources.users import userBP
from resources.marketplace import marketplace
from resources.messages import messageBP

DEBUG = True
PORT = 8000

login_manager = LoginManager()

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET') or 'recordslongconfusingkey'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(userid):
    try:
        return User.get(User.id == userid)
    except BaseException:
        return None


@app.before_request
def before_request():
    g.db = DATABASE
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


@app.route('/')
def index():
    return 'Welcome to Record App!'


app.register_blueprint(recordBP)
app.register_blueprint(userBP)
app.register_blueprint(marketplace)
app.register_blueprint(messageBP)

origins = ['http://localhost:3000', "*"]


if 'DATABASE_URL' in os.environ:
    initialize([Record, User, Favorite, Marketplace, Message])
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = False
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    origins.append(os.environ.get('CLIENT_URL'))

CORS(app, origins=origins, supports_credentials=True)


if __name__ == '__main__':
    initialize([Record, User, Favorite, Marketplace, Message])
    app.run(debug=DEBUG, port=PORT)
