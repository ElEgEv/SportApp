from pydantic import BaseModel
from sqlalchemy.orm import declarative_base
from sqlalchemy import  Column, Date, Integer, String
import datetime
from typing import Optional
  
Base = declarative_base()
  
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
    
class UserLogin(BaseModel):
    email: str
    password: str
    
# model for pagination
class UserOut(BaseModel):
    id: int
    name: str
    email: str
    date_birthday: Optional[datetime.date] = None
    sports_category: Optional[str] = None
    avatars: Optional[str] = None

    # for work pydantic with sqlalchemy model
    class Config:
        orm_mode = True
        
class UserCreateModel(BaseModel):  
    name: str
    email: str
    password: str
    date_birthday: datetime.date
    sports_category: str
        
class SportOut(BaseModel):
    id: int
    name: str
    trainer: str
    
    class Config:
        orm_mode = True
    