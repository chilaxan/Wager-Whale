from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    balance = Column(Float)

class Wager(Base):
    __tablename__ = 'wagers'
    id = Column(Integer, primary_key=True, index=True)
    owner = Column(Integer)
    startX = Column(Float)
    startY = Column(Float)
    endX = Column(Float)
    endY = Column(Float)
    bet = Column(Float)
    duration = Column(Float)
    stream = Column(String)