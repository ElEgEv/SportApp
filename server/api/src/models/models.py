from pydantic import BaseModel
from sqlalchemy.orm import declarative_base
from sqlalchemy import  Column, Date, Integer, String
import datetime
from typing import List, Optional
  
Base = declarative_base()
  
# class Sport(Base):
#     __tablename__ = "sports"
  
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     trainer = Column(String)
    
# class User(Base):
#     __tablename__ = "users"
  
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)
#     email = Column(String)
#     password = Column(String)
#     date_birthday = Column(Date)
#     sports_category = Column(String)
#     avatars = Column(String)

# ORM MODELS
from sqlalchemy import (
    Column, Integer, String, Date, ForeignKey, BigInteger, Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(500), nullable=False)
    date_birthday = Column(Date, nullable=False)
    sports_category = Column(String(255), nullable=False)
    avatars = Column(String(255), nullable=True)

    # Связи
    sports = relationship('UserSport', back_populates='user')
    competitions = relationship('UserCompetition', back_populates='user')
    
    @property
    def processed_avatars(self):
        base_url = "http://localhost:8000/"
        return f"{base_url}{self.avatars}" if self.avatars else None


class Sport(Base):
    __tablename__ = 'sports'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    trainer = Column(String(300), nullable=False)

    # Связи
    competitions = relationship('Competition', back_populates='sport')
    users = relationship('UserSport', back_populates='sport')


class UserSport(Base):
    __tablename__ = 'users_sports'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    sport_id = Column(BigInteger, ForeignKey('sports.id'), nullable=False)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=True)

    # Связи
    user = relationship('User', back_populates='sports')
    sport = relationship('Sport', back_populates='users')


class Competition(Base):
    __tablename__ = 'competitions'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    sport_id = Column(BigInteger, ForeignKey('sports.id'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    chief_judge = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    image = Column(String(255), nullable=True)

    # Связи
    sport = relationship('Sport', back_populates='competitions')
    participants = relationship('UserCompetition', back_populates='competitions')
    
    @property
    def processed_image(self):
        base_url = "http://localhost:8000/"
        return f"{base_url}{self.image}" if self.image else None


class UserCompetition(Base):
    __tablename__ = 'users_competitions'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    competition_id = Column(BigInteger, ForeignKey('competitions.id'), nullable=False)
    start_group = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    results = Column(String(255), nullable=False)
    position = Column(Integer, nullable=False)

    # Связи
    user = relationship('User', back_populates='competitions')
    competitions = relationship('Competition', back_populates='participants')

# /ORM MODELS
    
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

class SportCreateModel(BaseModel):
    name: str
    trainer: str
    
class UserSportORM(BaseModel):
    user_id: int
    sport_id: int
    date_start: datetime.date
    date_end: Optional[datetime.date] = None
    
class CompetitionCreateModel(BaseModel):
    sport_id: int
    name: str
    description: str
    chief_judge: str
    date: datetime.date
    
class CompetitionOut(BaseModel):
    id: int
    sport_id: int
    name: str
    description: Optional[str] = None
    chief_judge: str
    date: datetime.date
    image: Optional[str] = None

    class Config:
        orm_mode = True
        

class UserCompetitionCreateModel(BaseModel):
    user_id: int
    competition_id: int
    start_group: str
    description: str
    results: str
    position: int