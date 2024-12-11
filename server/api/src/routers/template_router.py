import datetime
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi_pagination import Params

from dotenv import load_dotenv
import os

from src.repository import CompetitionRepository
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

@router.get("/sports", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def get_sports(request: Request, 
                    params: Params = Depends(get_pagination_params),
                    session_data: UserOut = Depends(verifier)
                ):
    try:
        if not session_data:
            return RedirectResponse(url="/api/templates/auth", status_code=302)
        page_data = SportsRepository.getAllSports(params)
        return templates.TemplateResponse("sports.html", {"request": request, "page": page_data})
    except HTTPException as e:
        return RedirectResponse(url="/api/templates/auth", status_code=302)


@router.get("/athletes", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def get_users(request: Request, 
                    params: Params = Depends(get_pagination_params),
                    session_data: UserOut = Depends(verifier)
                ):
    try:
        if not session_data:
            return RedirectResponse(url="/api/templates/auth", status_code=302)
        page_data = UsersRepository.getAllUsers(params)
        
        for user in page_data.items:
            user.avatars = os.environ.get("SERVER_URL") + user.avatars
            
        return templates.TemplateResponse("athletes.html", {"request": request, "page": page_data})
    except HTTPException as e:
        return RedirectResponse(url="/api/templates/auth", status_code=302)
    

@router.get("/competitions", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def get_competitions(request: Request, 
                            getBetter: str = 'N', 
                            getMiddle: str = 'N',
                            date_start: datetime.date = datetime.date.today(),
                            date_end: datetime.date = datetime.date.today(), 
                            sport_id: int = 0,
                            params: Params = Depends(get_pagination_params),
                            session_data: UserOut = Depends(verifier)
                        ):
    try:
        if not session_data:
            return RedirectResponse(url="/api/templates/auth", status_code=302)
        if date_end < date_start:
            return templates.TemplateResponse("competitions.html", {"request": request, "error": "Дата окончания не может быть раньше даты начала"})
        
        if sport_id != 0:
            page_data = CompetitionRepository.getAllCompetition(params, sport_id)
        else:
            page_data = CompetitionRepository.getAllCompetition(params)
        
        sports = SportsRepository.getAllSportsWithoutPagination()
        
        for competition in page_data.items:
            if competition.image:
                competition.image = os.environ.get("SERVER_URL") + competition.image
            else:
                competition.image = os.environ.get("SERVER_URL") + "public/competitions/images/default.jpg"
        
        data_for_template = {
            "request": request, 
            "page": page_data, 
            "sports": sports,
            "getBetter": getBetter,
            "getMiddle": getMiddle,
            "date_start": date_start,
            "date_end": date_end,
            "sport_id": sport_id,
            "dataBestForGraph": False,
            "dateMiddleForGraph": False
        }
        
        if getBetter == 'Y' and sport_id != 0:
            dataBestForGraph = CompetitionRepository.getBestResultByPeriod(date_start, date_end, sport_id)
            
            data_for_template['dataBestForGraph'] = dataBestForGraph
            
        if getMiddle == 'Y' and sport_id != 0:
            dateMiddleForGraph = CompetitionRepository.getMiddleResultByPeriod(date_start, date_end, sport_id)

            data_for_template['dateMiddleForGraph'] = dateMiddleForGraph
        
        return templates.TemplateResponse("competitions.html", data_for_template)
    except HTTPException as e:
        return RedirectResponse(url="/api/templates/auth", status_code=302)

@router.get("/competition_result/", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def get_competition_result(request: Request, 
                                sport_id: int = 0, 
                                competition_id: int = 0,
                                session_data: UserOut = Depends(verifier)
                            ):
    try:
        if not session_data:
            return RedirectResponse(url="/api/templates/auth", status_code=302)
        
        if sport_id != 0:
            competitions = CompetitionRepository.getCompetitionsBySportId(sport_id)
        else:
            competitions = None
            
        if competition_id != 0:
            competition = CompetitionRepository.getCompetitionById(competition_id)
        else:
            competition = None
            
        users = UsersRepository.getAllUsersWithoutPagination()
        sports = SportsRepository.getAllSportsWithoutPagination()
        
        if competition:
            if competition.image:
                competition.image = os.environ.get("SERVER_URL") + competition.image
            else:
                competition.image = os.environ.get("SERVER_URL") + "public/competitions/images/default.jpg"
                
            for participant in competition.participants:
                participant = participant.__dict__
                participant['user_name'] = UsersRepository.getUserById(participant['user_id']).name
        
        data_for_template = {
            "request": request, 
            "id": 1, 
            "competition": competition, 
            "competitions": competitions,
            "users": users,
            "sports": sports,
            "sport_id": sport_id,
            "competition_id": competition_id
        }
        
        return templates.TemplateResponse("competition_result.html", data_for_template)
    except HTTPException as e:
        return RedirectResponse(url="/api/templates/auth", status_code=302)


@router.get("/main", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def get_main(request: Request, session_data: UserOut = Depends(verifier)):
    try:
        if not session_data:
            return RedirectResponse(url="/api/templates/auth", status_code=302)
        
        return templates.TemplateResponse("main.html", {"request": request})
    except HTTPException as e:
        return RedirectResponse(url="/api/templates/auth", status_code=302)


@router.get("/registration", response_class=HTMLResponse)
async def get_registration(request: Request):
    return templates.TemplateResponse("registration.html", {"request": request})


@router.get("/auth", response_class=HTMLResponse)
async def get_login():
    return templates.TemplateResponse("auth.html", {"request": {}})


@router.get("/profile", response_class=HTMLResponse, dependencies=[Depends(cookie)])
async def get_profile(request: Request, session_data: UserOut = Depends(verifier)):
    try:
        if not session_data:
            return RedirectResponse(url="/api/templates/auth", status_code=302)
        
        user = UsersRepository.getUserById(session_data.id)
        user.password = session_data.password
        
        return templates.TemplateResponse("profile.html", {"request": request, "user": user})
    except HTTPException as e:
        return RedirectResponse(url="/api/templates/auth", status_code=302)