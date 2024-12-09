from pathlib import Path
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi_pagination import add_pagination

from src.routers.sports_router import router as sports_router
from src.routers.user_router import router as user_router
from src.routers.user_sport_router import router as user_sport_router
from src.routers.competition_router import router as competition_router
from src.routers.user_competition_router import router as user_competition_router
from src.routers.template_router import router as template_router
from src.models.models import UserOut

app = FastAPI(
    title="Учёт результатов спортивных соревнований", 
    description="Данная API предназначена для курсовой работы в рамках предмета ТПО", 
    version="1.0.2"
)

add_pagination(app)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.mount("/public", StaticFiles(directory=Path("./public")), name="public")

@app.get("/")
def redirect_to_swagger():
    return RedirectResponse(url="/docs")

# @app.middleware("http")
# async def session_middleware(request: Request, call_next):
#     # Исключаем страницу `/auth` из проверки сессии
#     if request.url.path not in ["/api/templates/auth", "/api/templates/registration"] and "session_id" not in request.cookies:
#         return RedirectResponse(url="/api/templates/auth", status_code=302)
#     response = await call_next(request)
#     return response

app.include_router(sports_router)

app.include_router(user_router)

app.include_router(user_sport_router)

app.include_router(competition_router)

app.include_router(user_competition_router)

app.include_router(template_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)