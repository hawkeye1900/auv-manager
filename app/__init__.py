from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from dotenv import load_dotenv

import os
import logging


login_manager = LoginManager()
login_manager.login_view = 'main.login'
bcrypt = Bcrypt()
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    # create a Flask application instance
    app = Flask(__name__)

    logging.basicConfig(level=logging.DEBUG)

    login_manager.init_app(app)
    bcrypt.init_app(app)

    # connect db extension to app
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        'postgresql://user:password@db:5432/auv_db'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # suppress warning

    db.init_app(app)
    migrate.init_app(app, db)

    # import routes as blueprint
    from .routes import main

    # register the blueprint called main
    app.register_blueprint(main)

    register_error_handlers(app)

    # return the flask application
    return app


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

