from fastapi import APIRouter
from src.repository import UsersRepository

router = APIRouter(
    prefix="/api/users",
    tags=["Users CRUD"],
)

@router.get("/")
async def get_users():
    return UsersRepository.getAllUsers()
