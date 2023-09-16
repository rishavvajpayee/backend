from conf.base import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), default=func.uuid_generate_v4())
    email = Column(String(100), default=None)
    phone_number = Column(String(100), default=None)
    password = Column(String(100), default=None)


class Otp(Base):
    __tablename__ = "otp"
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), default=None)
    otp = Column(Integer, default=None)


class Test(Base):
    __tablename__ = "test"
    id = Column(Integer, primary_key=True)
    test = Column(String(10), default="")
