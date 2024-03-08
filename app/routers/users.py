from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import SessionLocal, engine, get_db

router = APIRouter()


@router.post("/users")
def get_users(user: schemas.UserCreate, db: Session = Depends(get_db)):
    fake_password = utils.get_password_hash(user.password)
    user.password = fake_password

    
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
