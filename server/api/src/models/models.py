from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import  Column, Date, Integer, String
  
class Base(DeclarativeBase): pass
  
class Sport(Base):
    __tablename__ = "sports"
  
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    trainer = Column(String)
    
class User(Base):
    __tablename__ = "users"
  
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    date_birthday = Column(Date)
    sports_category = Column(String)
    avatars = Column(String)