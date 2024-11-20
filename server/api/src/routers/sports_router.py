from fastapi import APIRouter
from src.repository import SportsRepository

router = APIRouter(
    prefix="/api/sports",
    tags=["Sports CRUD"],
)

@router.get("/")
async def get_sports():
    return SportsRepository.getAllSports()
