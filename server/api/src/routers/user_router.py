import datetime
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, Request, Response, UploadFile, File, Form
from fastapi_pagination import Page, Params
from typing import Annotated, Optional
from fastapi.responses import RedirectResponse


from src.utils.FileOperator import get_file_format
from src.repository import UsersRepository
from src.models.models import User, UserCreateModel, UserLogin, UserOut

from dotenv import load_dotenv
import os

from authlib.integrations.starlette_client import OAuthError
from src.utils.auth_handler import sign_jwt
from src.utils.auth_bearer import JWTBearer
from src.repository.UsersRepository import updateUser

from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.session_verifier import SessionVerifier
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from fastapi.templating import Jinja2Templates
from uuid import UUID, uuid4

from src.utils.basic_verifier import BasicVerifier

load_dotenv('.env')

templates = Jinja2Templates(directory="templates")


router = APIRouter(
    prefix="/api/users",
    tags=["Users CRUD"],
)

cookie_params = CookieParameters(
    max_age=86400
)

cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="erondondon",
    cookie_params=cookie_params,
)

backend = InMemoryBackend()

verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=False,
    backend=backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)

@router.get("/", response_model=Page[UserOut])
async def get_users(params: Params = Depends()):
    page = UsersRepository.getAllUsers(params)
    
    for user in page.items:
        user.avatars = os.environ.get("SERVER_URL") + user.avatars
    
    return page

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def get_user_by_id(id: int):
    user = UsersRepository.getUserById(id)
    
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
        
    return user

@router.post("/sign_in")
async def sign_in_user(email: Annotated[str, Form()],
                       password: Annotated[str, Form()], 
                       response: Response,
                       request: Request):
    try:
        user = UserLogin(email=email, password=password)
        
        user_data = UsersRepository.checkUser(user)
        
        if not user_data:
            return templates.TemplateResponse(
                "auth.html", 
                {"request": request, "error": "Неверная почта или пароль"}
            )
        
        user_data.password = user.password
        
        user_data = user_data.__dict__
        
        user_data['avatars'] = os.environ.get("SERVER_URL") + user_data['avatars']
        user_data['token'] = sign_jwt(user.email)['access_token']
        
        user = UserOut(**user_data)
        
        session = uuid4()
        data = user
        
        await backend.create(session, data)

        response = RedirectResponse(url="/api/templates/main", status_code=302)
        cookie.attach_to_response(response, session)
        
        return response
        
    except OAuthError:
        return HTTPException(status_code=403, detail="Ошибка авторизации. Проверьте логин и пароль")
    
    except Exception as e:
        return HTTPException(status_code=403, detail=str(e))


@router.get("/check/user", dependencies=[Depends(cookie)])
async def check_user(session_data: UserOut = Depends(verifier)):
    return session_data

@router.post("/logout")
async def delete_session(response: Response, session_id: UUID = Depends(cookie)):
    if await backend.read(session_id):
        await backend.delete(session_id)
        cookie.delete_from_response(response)
        return RedirectResponse(url="/api/templates/auth", status_code=302)
    else:
        cookie.delete_from_response(response)
        return RedirectResponse(url="/api/templates/auth", status_code=302)


@router.post("/create", description="Upload a file with multipart/form-data")
async def create_user(request: Request,
                      name: Annotated[str, Form()],
                      email: Annotated[str, Form()],
                      password: Annotated[str, Form()],
                      date_birthday: Annotated[datetime.date, Form()],
                      sports_category: Annotated[str, Form()],
                      avatar: Optional[UploadFile] = File(...)
                    ):
    try:
        if avatar:
            file_format = get_file_format(avatar)
            
            if file_format not in ['png', 'jpg', 'jpeg']:
                raise HTTPException(status_code=405, detail="Incorrect image format")

        user = UserCreateModel(name=name, 
                                email=email, 
                                password=password, 
                                date_birthday=date_birthday, 
                                sports_category=sports_category
                            )
        user_data = UsersRepository.createUser(user, avatar)
        
        if not user_data:
            return templates.TemplateResponse(
                "registration.html", 
                {"request": request, "error": "Пользователь с такой почтой уже существует"}
            )
        
        user = user.__dict__
        user['id'] = user_data['user'].id
        user['token'] = user_data['token']['access_token']
        user['avatars'] = os.environ.get("SERVER_URL") + user_data['user'].avatars
        
        new_user = UserOut(**user)
        
        session = uuid4()
        data = new_user
        
        await backend.create(session, data)

        response = RedirectResponse(url="/api/templates/main", status_code=302)
        cookie.attach_to_response(response, session)
        
        return response
    except Exception as e:
        return HTTPException(status_code=400, detail=str(e))

@router.post("/update", dependencies=[Depends(cookie)])
async def update_user(id: int, 
                name: Annotated[str, Form()],
                email: Annotated[str, Form()],
                password: Annotated[str, Form()],
                date_birthday: Annotated[datetime.date, Form()],
                sports_category: Annotated[str, Form()],
                response: Response,
                session_id: UUID = Depends(cookie),
                avatar: Optional[UploadFile] = File(None)
            ):
    session_data = await backend.read(session_id)
    
    if session_data is None:
        return RedirectResponse(url="/api/templates/auth", status_code=302)
    
    if avatar:
        file_format = get_file_format(avatar)
        
        if file_format not in ['png', 'jpg', 'jpeg']:
            raise HTTPException(status_code=405, detail="Incorrect image format")
    
    user = UsersRepository.getUserById(id)
    
    if not user:    
        raise HTTPException(status_code=404, detail="User not found")
    
    data = UserCreateModel(
        name=name,
        email=email, 
        password=password, 
        date_birthday=date_birthday, 
        sports_category=sports_category
    )
    
    data_result = UsersRepository.updateUser(id, data, avatar)

    # Обновляем данные сессии
    updated_session_data = UserOut(
        id=data_result.id,
        name=data_result.name,
        email=data_result.email,
        password=data_result.password,
        date_birthday=data_result.date_birthday,
        sports_category=data_result.sports_category,
        avatars=data_result.avatars,
        token=session_data.token  # Оставляем токен без изменений
    )
    await backend.update(session_id, updated_session_data)

    # Обновляем куку
    response = RedirectResponse(url="/api/templates/profile", status_code=302)
    cookie.attach_to_response(response, session_id)
    
    return response


@router.delete("/{id}")
async def delete_user_by_id(id: int):
    result = UsersRepository.deleteUserById(id)
    
    if not result:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message" : "User delete success"}
