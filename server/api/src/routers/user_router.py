import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi_pagination import Page
from typing import Annotated
from src.utils.FileOperator import get_file_format
from src.repository import UsersRepository
from src.models.models import User, UserCreateModel, UserLogin, UserOut

from dotenv import load_dotenv
import os

from authlib.integrations.starlette_client import OAuthError
from src.utils.auth_handler import sign_jwt
from src.utils.auth_bearer import JWTBearer

load_dotenv('.env')

router = APIRouter(
    prefix="/api/users",
    tags=["Users CRUD"],
)

@router.get("/", response_model=Page[UserOut])
async def get_users():
    page = UsersRepository.getAllUsers()
    return page

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def get_user_by_id(id: int):
    user = UsersRepository.getUserById(id)
    
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user

@router.post("/sign_in")
async def sign_in_user(user: UserLogin):
    user_data = UsersRepository.checkUser(user)
    
    if not user_data:
        return HTTPException(status_code=410, detail="Incorrect email or password")
    
    return {"token": sign_jwt(user.email), "user_data" : user_data}
    

@router.post("/create")
async def create_user(name: Annotated[str, Form()],
                      email: Annotated[str, Form()],
                      password: Annotated[str, Form()],
                      date_birthday: Annotated[datetime.date, Form()],
                      sports_category: Annotated[str, Form()],
                      avatar: UploadFile = File(None)
                    ):

    if avatar:
        file_format = get_file_format(avatar)
        
        if file_format not in ['png', 'jpg', 'jpeg']:
            raise HTTPException(status_code=405, detail="Incorrect image format")
        
    user = UserCreateModel( name=name, 
                            email=email, 
                            password=password, 
                            date_birthday=date_birthday, 
                            sports_category=sports_category
                        )
    
    return UsersRepository.createUser(user, avatar)

@router.delete("/{id}")
async def delete_user_by_id(id: int):
    result = UsersRepository.deleteUserById(id)
    
    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message" : "User delete success"}
