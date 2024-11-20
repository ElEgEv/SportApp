from src.database.database import session_maker
from src.models.models import User

# # создаем сессию подключения к бд
# with session_maker as db:
#     # создаем объект Person для добавления в бд
#     tom = Person(name="Tom", age=38)
#     db.add(tom)     # добавляем в бд
#     db.commit()     # сохраняем изменения
#     print(tom.id)   # можно получить установленный id

def getAllUsers():
    with session_maker() as db:
        return db.query(User).all()