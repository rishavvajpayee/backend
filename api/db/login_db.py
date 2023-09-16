import uuid
from conf.base import Base
from sqlalchemy import Column, String, DateTime, Integer

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), default=uuid.uuid4())
    email = Column(String(100), default=None)
    password = Column(String(100), default=None)


class OTP(Base):
    __tablename__ = 'otp'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), default=None)
    otp = Column(Integer, default=None)