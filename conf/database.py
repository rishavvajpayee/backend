import os
from os.path import join, dirname
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = join(dirname(__file__), ".env")  # path for .env file
load_dotenv()


class Config:
    DEBUG = True if os.getenv("DEBUG") == "True" else False
    DEVELOPMENT = True
    CSRF_ENABLED = True
    SECRET_KEY = "secret"
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
    CORS_METHODS = os.getenv("CORS_METHODS", "GET,POST,PUT,DELETE").split(",")
    PORT = 5000

    SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(
        os.getenv("POSTGRES_USER"),
        os.getenv("POSTGRES_PASS"),
        os.getenv("POSTGRES_HOST"),
        os.getenv("POSTGRES_PORT"),
        os.getenv("POSTGRES_DB"),
    )
    engine = create_engine(SQLALCHEMY_DATABASE_URI, poolclass=NullPool)
