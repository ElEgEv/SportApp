import datetime
from fastapi import APIRouter, HTTPException, Form
from src.repository.UserSportRepository import addEndDateToUserSport, addSportToUser, removeSportFromUser
from src.models.models import UserSport, UserSportORM

from dotenv import load_dotenv
from typing import Annotated

load_dotenv('.env')

router = APIRouter(
    prefix="/api/user_sport",
    tags=["User Sport CRUD"],
)


@router.post("/create")
async def create_user_sport(
    user_id: Annotated[int, Form()],
    sport_id: Annotated[int, Form()],
    date_start: Annotated[datetime.date, Form()],
    date_end: Annotated[datetime.date, Form()] = None
):
    data = UserSportORM(
        user_id=user_id,
        sport_id=sport_id,
        date_start=date_start,
        date_end=None
    )
    
    return addSportToUser(UserSport(**data.model_dump()))


@router.put("/update")
def update_end_date_of_user_sport(user_sport_id: Annotated[int, Form()],
                                  date_end: Annotated[datetime.date, Form()]):
    result = addEndDateToUserSport(user_sport_id, date_end)
    
    if not result:
        raise HTTPException(status_code=404, detail="User Sport not found")

    return {"message" : "User Sport update success"}


@router.delete("/{id}")
async def delete_user_sport(user_sport_id: Annotated[int, Form()]):
    result = removeSportFromUser(user_sport_id)
    
    if not result:
        raise HTTPException(status_code=404, detail="User Sport not found")

    return {"message" : "User Sport delete success"}
    
