import datetime
import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi_pagination import Page, Params
from typing import Annotated, Optional
from src.repository import CompetitionRepository
from src.utils.FileOperator import get_file_format
from src.models.models import Competition, CompetitionCreateModel, CompetitionOut

from dotenv import load_dotenv

load_dotenv('.env')

router = APIRouter(
    prefix="/api/competitions",
    tags=["Competitions CRUD"],
)


@router.get("/", response_model=Page[CompetitionOut])
async def get_competitions(params: Params = Depends()):
    page = CompetitionRepository.getAllCompetition(params)
    
    for competition in page.items:
        if competition.image:
            competition.image = os.environ.get("SERVER_URL") + competition.image
        else:
            competition.image = os.environ.get("SERVER_URL") + "public/competitions/images/default.jpg"
    
    return page

@router.get("/{id}")
async def get_competition(id: int):
    return CompetitionRepository.getCompetitionById(id)

@router.post("/")
async def create_competition(sport_id: Annotated[int, Form()],
                            name: Annotated[str, Form()],
                            description: Annotated[str, Form()],
                            chief_judge: Annotated[str, Form()],
                            date: Annotated[datetime.date, Form()],
                            image: UploadFile = File(...)):
    if image:
        file_format = get_file_format(image)
        
        if file_format not in ['png', 'jpg', 'jpeg']:
            raise HTTPException(status_code=405, detail="Incorrect image format")
        
    competition = CompetitionCreateModel(
        sport_id=sport_id,
        name=name,
        description=description,
        chief_judge=chief_judge,
        date=date
    )
    
    return CompetitionRepository.createCompetition(competition, image)

@router.put("/update/")
async def update_competition(id: Annotated[int, Form()], 
                            sport_id: Annotated[int, Form()],
                            name: Annotated[str, Form()],
                            description: Annotated[str, Form()],
                            chief_judge: Annotated[str, Form()],
                            date: Annotated[datetime.date, Form()],
                            image: UploadFile = File(...)):
    if image:
        file_format = get_file_format(image)
        
        if file_format not in ['png', 'jpg', 'jpeg']:
            raise HTTPException(status_code=405, detail="Incorrect image format")
        
    competition = CompetitionCreateModel(
        sport_id=sport_id,
        name=name,
        description=description,
        chief_judge=chief_judge,
        date=date
    )
    
    return CompetitionRepository.updateCompetition(id, competition, image)

@router.delete("/{id}")
async def delete_competition(id: int):
    result = CompetitionRepository.deleteCompetitionById(id)
    
    if not result:
        raise HTTPException(status_code=404, detail="Competition not found")

    return {"message" : "Competition delete success"}