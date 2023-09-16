from flask import Flask
from conf.database import Config
from conf.base import Session
from flask_sqlalchemy_session import flask_scoped_session
"""
BLUEPRINT IMPORTS :
"""
from api.rest.login import LOGIN_BLUEPRINT


def create_app():
    """
    Construct the main application
    """
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_object(Config)
    flask_scoped_session(Session)
    app.register_blueprint(LOGIN_BLUEPRINT)
    return app