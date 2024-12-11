import datetime

from fastapi import HTTPException, UploadFile
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import joinedload
from src.utils.FileOperator import upload_file
from src.models.models import Competition, CompetitionCreateModel, Sport
from src.database.database import session_maker

def getAllCompetition(params: Params) -> Page[Competition]:
    with session_maker() as db:
        query = (
            db.query(Competition)
            .options(
                joinedload(Competition.sport)
            )
            .order_by(Competition.id)
        )
    
        return paginate(query, params=params)
    
def getCompetitionById(id: int):
    with session_maker() as db:
        competition = (
            db.query(Competition)
            .options(
                joinedload(Competition.sport),
                joinedload(Competition.participants)
            )
            .get(id)
        )
        
        if competition:
            competition.image = competition.processed_image
        else:
            raise HTTPException(status_code=404, detail="Competition not found")
        
        return competition

def createCompetition(competition: CompetitionCreateModel, image: UploadFile):
    current_file_name = upload_file('competitions/images', image, image.filename)
        
    db_competition = Competition(**competition.model_dump())
    
    db_competition.image = current_file_name
        
    with session_maker() as db:
        db.add(db_competition)
        db.commit()
        return db_competition
    
def updateCompetition(id: int, competition: Competition, image: UploadFile):
    with session_maker() as db:
        competition_db = db.query(Competition).get(id)
        
        if not competition_db:
            raise HTTPException(status_code=404, detail="Competition not found")
        
        competition_db.name = competition.name
        competition_db.description = competition.description
        competition_db.chief_judge = competition.chief_judge
        competition_db.date = competition.date
        competition_db.sport_id = competition.sport_id
        
        current_file_name = upload_file('competitions/images', image, image.filename)
        
        competition_db.image = current_file_name
        
        db.commit()

        return competition_db
    
def deleteCompetitionById(id: int):
    with session_maker() as db:
        competition = db.query(Competition).get(id)
        db.delete(competition)
        db.commit()
        return True