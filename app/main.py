from fastapi import Depends, FastAPI

from . import models, utils
from .config import Settings
from .database import SessionLocal, engine, get_db
from .routers import auth, posts, users, likes

# models.Base.metadata.create_all(bind=engine)



# user444@example.com
app = FastAPI()

app.include_router(users.router, prefix="/users", tags=["users"])

app.include_router(auth.router, tags=["login"])

app.include_router(posts.router, prefix="/posts", tags=["posts"])

app.include_router(likes.router, prefix="/likes", tags=["likes"])
