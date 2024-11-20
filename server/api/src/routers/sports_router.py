from fastapi import APIRouter
from fastapi_pagination import Page
from src.repository import SportsRepository
from src.models.models import Sport, SportOut

router = APIRouter(
    prefix="/api/sports",
    tags=["Sports CRUD"],
)

@router.get("/", response_model=Page[SportOut])
async def get_sports():
    page = SportsRepository.getAllSports()
    return page
