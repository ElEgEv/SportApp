import datetime
from src.database.database import session_maker
from src.models.models import Sport, User, UserSport
from src.models.models import UserSport


def addSportToUser(data: UserSport):
    with session_maker() as db:
        
        user = db.query(User).filter(User.id == data.user_id).first()
        
        if not user:
            raise ValueError(f"User with id {data.user_id} does not exist.")

        sport = db.query(Sport).filter(Sport.id == data.sport_id).first()
        
        if not sport:
            raise ValueError(f"Sport with id {data.sport_id} does not exist.")

        # if all right
        db.add(data)
        db.commit()

        return data
    

def addEndDateToUserSport(user_sport_id: int, date_end: datetime.date):
    with session_maker() as db:
        user_sport = db.query(UserSport).filter(UserSport.id == user_sport_id).first()

        if not user_sport:
            raise ValueError(f"Row with id {user_sport_id} not found.")

        user_sport.date_end = date_end
        db.commit()

        return True


def removeSportFromUser(id: int):
    with session_maker() as db:
        user_sport = db.query(UserSport).filter(UserSport.id == id).first()

        if not user_sport:
            raise ValueError(f"Row with id {id} not found.")

        db.delete(user_sport)
        db.commit()

        return True