from fastapi import FastAPI, Depends

from . import models, utils
from .database import SessionLocal, engine, get_db
from .config import Settings
from .routers import users


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)

