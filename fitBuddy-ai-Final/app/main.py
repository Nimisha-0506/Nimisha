from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import init_db
from .routes import router

app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

init_db()
app.include_router(router)
