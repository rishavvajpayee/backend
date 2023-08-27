from flask import Flask
from conf.database import Config
from utils.base import Session
from flask_sqlalchemy_session import flask_scoped_session

"""
BLUEPRINT IMPORTS :
"""
from api.rest.basic_api import BASIC_BLUEPRINT


def create_app():
    """
    Construct the main application
    """
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_object(Config)
    app.register_blueprint(BASIC_BLUEPRINT)
    return app