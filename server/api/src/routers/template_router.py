from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_pagination import Params

from src.utils.template_pagination import get_pagination_params
import src.repository.SportsRepository as SportsRepository

templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/api/templates",
    tags=["Tamplates route"],
)

@router.get("/sports", response_class=HTMLResponse)
async def get_sports(request: Request, params: Params = Depends(get_pagination_params)):
    page_data = SportsRepository.getAllSports(params)
    return templates.TemplateResponse("sports.html", {"request": request, "page": page_data})