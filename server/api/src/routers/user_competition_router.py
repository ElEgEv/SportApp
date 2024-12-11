import datetime
from fastapi import APIRouter, HTTPException, Form
from src.repository.UserCompetitionRepository import createUserCompetition, updateUserCompetition, removeUserCompetition
from src.models.models import UserCompetitionCreateModel

from dotenv import load_dotenv
from typing import Annotated

load_dotenv('.env')

router = APIRouter(
    prefix="/api/user_competition",
    tags=["User Competition CRUD"],
)

@router.post("/")
async def create_user_competition(user_id: Annotated[int, Form()],
                                    competition_id: Annotated[int, Form()],
                                    start_group: Annotated[str, Form()],
                                    description: Annotated[str, Form()],
                                    results: Annotated[str, Form()],
                                    position: Annotated[int, Form()]
                                ):
    
    userCompetition = UserCompetitionCreateModel(
        user_id=user_id,
        competition_id=competition_id,
        start_group=start_group,
        description=description,
        results=results,
        position=position
    )
    
    return createUserCompetition(userCompetition)

@router.put("/update")
async def update_user_competition(id: Annotated[int, Form()],
                                    user_id: Annotated[int, Form()],
                                    competition_id: Annotated[int, Form()],
                                    start_group: Annotated[str, Form()],
                                    description: Annotated[str, Form()],
                                    results: Annotated[str, Form()],
                                    position: Annotated[int, Form()]):
    
    userCompetition = UserCompetitionCreateModel(
        user_id=user_id,
        competition_id=competition_id,
        start_group=start_group,
        description=description,
        results=results,
        position=position
    )
    
    return updateUserCompetition(id, userCompetition)

@router.delete("/{id}")
async def remove_user_competition(id: int):
    if id == None:
        raise HTTPException(status_code=404, detail="User Competition not found")
    
    return removeUserCompetition(id)