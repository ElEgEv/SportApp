from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi_pagination import add_pagination

from src.routers.sports_router import router as sports_router
from src.routers.user_router import router as user_router
from src.routers.user_sport_router import router as user_sport_router
from src.routers.competition_router import router as competition_router
from src.routers.user_competition_router import router as user_competition_router

app = FastAPI(
    title="Учёт результатов спортивных соревнований", 
    description="Данная API предназначена для курсовой работы в рамках предмета ТПО", 
    version="1.0.1"
)

add_pagination(app)
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/public", StaticFiles(directory=Path("./public")), name="public")

@app.get("/")
def redirect_to_swagger():
    return RedirectResponse(url="/docs")

app.include_router(sports_router)

app.include_router(user_router)

app.include_router(user_sport_router)

app.include_router(competition_router)

app.include_router(user_competition_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)