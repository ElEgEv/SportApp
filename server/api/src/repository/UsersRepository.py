import os
from sqlalchemy import select
from fastapi import UploadFile
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from src.database.database import session_maker
from src.models.models import User, UserCreateModel, UserLogin
from src.utils.FileOperator import upload_file
from src.utils.hashing import Hasher


def getAllUsers() -> Page[User]:
    with session_maker() as db:
        query = db.query(User)
        return paginate(query)
    
def checkUser(user: UserLogin):
    with session_maker() as db:
        user_db = db.query(User).filter(User.email == user.email).first()
        
        is_user = Hasher.verify_password(user.password, user_db.password)
        
        if is_user:
            return user
        
        return False
    
def getUserById(id: int):
    with session_maker() as db:
        user = db.query(User).get(id)
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
        return {"message": "User create success"}
    
def deleteUserById(id: int):
    with session_maker() as db:
        user = db.query(User).get(id)
        db.delete(user)
        db.commit()
        return True