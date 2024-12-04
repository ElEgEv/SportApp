from sqlalchemy.orm import joinedload
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from src.database.database import session_maker
from src.models.models import Sport

def getAllSports(params: Params) -> Page[Sport]:
    with session_maker() as db:
        query = db.query(Sport)
        return paginate(query, params=params)
    
def getSportById(id: int):
    with session_maker() as db:
        sport = (
            db
            .query(Sport)
            .options(
                joinedload(Sport.users),
                joinedload(Sport.competitions)
            )
            .get(id) 
        )
        
        return sport
    
def createSport(sport: Sport):
    with session_maker() as db:
        db.add(sport)
        db.commit()
        return sport
    
def updateSport(id: int, sport: Sport):
    with session_maker() as db:
        sport_db = db.query(Sport).get(id)
        sport_db.name = sport.name
        sport_db.trainer = sport.trainer
        db.commit()
        sport.id = id
        return sport
    
def deleteSportById(id: int):
    with session_maker() as db:
        sport = db.query(Sport).get(id)
        db.delete(sport)
        db.commit()
        return True