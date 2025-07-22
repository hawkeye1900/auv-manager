from flask import Flask  # import Flask class
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

import os

login_manager = LoginManager()
bcrypt = Bcrypt()
load_dotenv()

db = SQLAlchemy()


def create_app():
    # create a Flask application instance
    app = Flask(__name__)

    login_manager.init_app(app)
    bcrypt.init_app(app)

    # connect db extension to app
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://user:password@db:5432/auv_db'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # suppress warning

    db.init_app(app)

    # import routes as blueprint
    from .routes import main

    # register the blueprint called main
    app.register_blueprint(main)

    # return the flask application
    return app

