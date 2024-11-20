from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from src.database.database import session_maker
from src.models.models import Sport

# # создаем сессию подключения к бд
# with session_maker as db:
#     # создаем объект Person для добавления в бд
#     tom = Person(name="Tom", age=38)
#     db.add(tom)     # добавляем в бд
#     db.commit()     # сохраняем изменения
#     print(tom.id)   # можно получить установленный id

def getAllSports() -> Page[Sport]:
    with session_maker() as db:
        query = db.query(Sport)
        return paginate(query)