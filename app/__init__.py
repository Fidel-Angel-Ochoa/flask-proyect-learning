from flask import Flask
from flask_bs4 import Bootstrap
from flask_login import LoginManager

from app.models import UserModel

from .config import Config
from .auth import auth


login_manger= LoginManager()
login_manger.login_view='auth.login'


# @login_manger.user_loader
# def load_user(user_id=''):
#     return None

@login_manger.user_loader
def load_user(username):
    return UserModel.query(username)

def create_app():
    app= Flask(__name__)
    bootstrap = Bootstrap(app)

    app.config.from_object(Config)
    
    login_manger.init_app(app)

    app.register_blueprint(auth)

    return app
