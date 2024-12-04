import os
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fastapi import UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from src.database.database import session_maker
from src.models.models import User, UserCreateModel, UserLogin
from src.utils.FileOperator import upload_file
from src.utils.hashing import Hasher
from src.utils.auth_handler import sign_jwt


def getAllUsers() -> Page[User]:
    with session_maker() as db:
        query = db.query(User)
        return paginate(query)
    
def checkUser(user: UserLogin):
    with session_maker() as db:
        user_db = db.query(User).filter(User.email == user.email).first()
        
        if not user_db:
            return False
        
        is_user = Hasher.verify_password(user.password, user_db.password)
        
        if is_user:
            return user
        
        return False
    
def getUserById(id: int):
    with session_maker() as db:
        user = (
            db.query(User)
            .options(
                joinedload(User.sports),  # Жадная загрузка видов спорта
                joinedload(User.competitions),  # Жадная загрузка соревнований
            )
            .filter(User.id == id)
            .first()
        )
        
        if user:
            user.avatars = user.processed_avatars
        
        return user
    
def createUser(user: UserCreateModel, avatar: UploadFile | None):
    if avatar:
        current_file_name = upload_file('users/avatars', avatar, avatar.filename)
    else:
        current_file_name = os.environ.get("DEFAULT_AVATARS")
    
    user_dict = {
        'name': user.name,
        'email': user.email,
        'password': Hasher.get_password_hash(user.password),
        'date_birthday': user.date_birthday,
        'sports_category': user.sports_category,
        'avatars': current_file_name
    }
   
    db_user = User(**user_dict)
    
    with session_maker() as db:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {
            "message": "User create success",
            "user": db_user,
            "token": sign_jwt(user.email)
        }
        
def updateUser(id: int, user: UserCreateModel, avatar: UploadFile | None):
    with session_maker() as db:
        user_db = db.query(User).get(id)
    
        user_db.name = user.name
        user_db.email = user.email
        user_db.password = Hasher.get_password_hash(user.password)
        user_db.date_birthday = user.date_birthday
        user_db.sports_category = user.sports_category

        current_file_name = upload_file('users/avatars', avatar, avatar.filename)
        
        user_db.avatars = current_file_name
            
        db.commit()
        return user
    
def deleteUserById(id: int):
    with session_maker() as db:
        user = db.query(User).get(id)
        db.delete(user)
        db.commit()
        return True