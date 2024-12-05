from src.database.database import session_maker
from src.models.models import User, Competition, UserCompetition, UserCompetitionCreateModel


def createUserCompetition(data: UserCompetitionCreateModel):
    with session_maker() as db:
        
        user = db.query(User).filter(User.id == data.user_id).first()
        
        if not user:
            raise ValueError(f"User with id {data.user_id} does not exist.")

        competition = db.query(Competition).filter(Competition.id == data.competition_id).first()
        
        if not competition:
            raise ValueError(f"Competition with id {data.sport_id} does not exist.")
        
        db_user_competition = UserCompetition(**data.model_dump())
        
        db.add(db_user_competition)
        db.commit()
        
        return db_user_competition
    

def updateUserCompetition(id: int, data: UserCompetitionCreateModel):
    with session_maker() as db:
        user_competition = db.query(UserCompetition).filter(UserCompetition.id == id).first()

        if not user_competition:
            raise ValueError(f"Row with id {id} not found.")

        user_competition.user_id = data.user_id
        user_competition.competition_id = data.competition_id
        user_competition.start_group = data.start_group
        user_competition.description = data.description
        user_competition.results = data.results
        user_competition.position = data.position
        
        db.commit()

        return {"message": "User competition updated success"}


def removeUserCompetition(id: int):
    with session_maker() as db:
        user_competition = db.query(UserCompetition).filter(UserCompetition.id == id).first()

        if not user_competition:
            raise ValueError(f"User competition with id {id} not found.")

        db.delete(user_competition)
        db.commit()

        return {"message": "User competition deleted success"}