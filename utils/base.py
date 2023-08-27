from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from conf.database import Config

Session = sessionmaker(bind=Config.engine, autoflush=False)
base = declarative_base()