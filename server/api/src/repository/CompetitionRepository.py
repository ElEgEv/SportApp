import datetime

from fastapi import HTTPException, UploadFile
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import joinedload
from sqlalchemy import func
from src.repository import SportsRepository
from src.utils.FileOperator import upload_file
from src.models.models import Competition, CompetitionCreateModel, Sport
from src.database.database import session_maker

def getAllCompetition(params: Params, sport_id: int = 0) -> Page[Competition]:
    with session_maker() as db:
        if sport_id == 0:
            query = (
                db.query(Competition)
                .options(
                    joinedload(Competition.sport)
                )
                .order_by(Competition.id)
            )
        else:
            query = (
                db.query(Competition)
                .options(
                    joinedload(Competition.sport)
                )
                .filter(Competition.sport_id == sport_id)
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
    

def getBestResultByPeriod(date_start: datetime, date_end:datetime, sport_id: int):
    with session_maker() as db:
        competitions = (db.query(Competition.id)
                .filter(Competition.date >= date_start, Competition.date <= date_end, Competition.sport_id == sport_id)
                .order_by(Competition.date)
                .all()
            )
        
        sport = SportsRepository.getSportById(sport_id)
        
        # сюда название вида спорта
        headers = ["#", sport.name]
        # сюда данные в виде день / сарева + по саревам
        data_arr = []
        
        for competition_id in competitions:
            competition: Competition = getCompetitionById(competition_id[0])
            
            print(competition.__dict__)
            
            if len(competition.participants) > 0:
                support_arr = []
                
                support_arr.append(competition.name)
                support_arr.append(int(max(competition.participants, key=lambda x: int(x.results)).results))
                
                data_arr.append(support_arr)
            
        data_for_template = {
            "header": headers,
            "rows": data_arr
        }
        
        return data_for_template

def getMiddleResultByPeriod(date_start, date_end, sport_id):
    with session_maker() as db:
        competitions = (db.query(Competition.id)
                .filter(Competition.date >= date_start, Competition.date <= date_end, Competition.sport_id == sport_id)
                .order_by(Competition.date)
                .all()
            )
        
        sport = SportsRepository.getSportById(sport_id)
        
        headers = ["#", sport.name]
        data_arr = []
        
        for competition_id in competitions:
            competition: Competition = getCompetitionById(competition_id[0])
            
            print(competition.__dict__)
            
            if len(competition.participants) > 0:
                support_arr = []
                
                support_arr.append(competition.name)
                support_arr.append(sum(int(p.results) for p in competition.participants) / len(competition.participants))
                
                data_arr.append(support_arr)
            
        data_for_template = {
            "header": headers,
            "rows": data_arr
        }
        
        return data_for_template
    

def getCompetitionsBySportId(sport_id: int):
    with session_maker() as db:
        return db.query(Competition).filter(Competition.sport_id == sport_id).all()


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