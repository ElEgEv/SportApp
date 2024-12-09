from fastapi import APIRouter, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_pagination import Params

from dotenv import load_dotenv
import os

from src.models.models import UserOut
import src.repository.UsersRepository as UsersRepository
import src.repository.SportsRepository as SportsRepository

from src.routers.user_router import cookie, verifier

from src.utils.template_pagination import get_pagination_params
load_dotenv('.env')

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/api/templates",
    tags=["Tamplates route"],
)

@router.get("/sports", response_class=HTMLResponse)
async def get_sports(request: Request, params: Params = Depends(get_pagination_params)):
    page_data = SportsRepository.getAllSports(params)
    return templates.TemplateResponse("sports.html", {"request": request, "page": page_data})


@router.get("/athletes", response_class=HTMLResponse)
async def get_users(request: Request, params: Params = Depends(get_pagination_params)):
    page_data = UsersRepository.getAllUsers(params)
    
    for user in page_data.items:
        user.avatars = os.environ.get("SERVER_URL") + user.avatars
        
    return templates.TemplateResponse("athletes.html", {"request": request, "page": page_data})


@router.get("/main", response_class=HTMLResponse)
async def get_main(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@router.get("/about", response_class=HTMLResponse)
async def get_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@router.get("/registration", response_class=HTMLResponse)
async def get_registration(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.get("/auth", response_class=HTMLResponse)
async def get_login():
    return templates.TemplateResponse("auth.html", {"request": {}})

@router.get("/profile", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def get_profile(request: Request, session_data: UserOut = Depends(verifier)):
    try:       
        user = UsersRepository.getUserById(session_data.id)
        
        user.avatars = os.environ.get("SERVER_URL") + user.avatars
        
        return templates.TemplateResponse("profile.html", {"request": request, "user": user})
    except Exception as e:
        return RedirectResponse(url="/auth", status_code=302)