from fastapi import FastAPI

from . import models
from .database import SessionLocal, engine
from .config import Settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

