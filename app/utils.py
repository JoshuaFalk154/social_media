from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status

from . import models, schemas
from .database import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_username(username: str, db: Session):
    db_user = db.query(models.User).filter_by(username=username).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User not found"
        )
    return db_user


def get_post_by_id(id: int, db: Session):
    db_user = db.query(models.Post).filter_by(id=id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Post not found"
        )
    return db_user



