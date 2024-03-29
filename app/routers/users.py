from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, oauth, schemas, utils
from ..database import SessionLocal, engine, get_db
from ..oauth import get_current_user

router = APIRouter()


@router.post("", response_model=schemas.User)
def create_users(user: schemas.UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(models.User).filter_by(email=user.email).first()

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists!"
        )

    hashed_password = utils.get_password_hash(user.password)
    user_data = user.model_dump()
    user_data.pop("password")

    db_user_create = models.User(**user_data, hashed_password=hashed_password)
    db.add(db_user_create)
    db.commit()
    db.refresh(db_user_create)

    return db_user_create


# @router.get("")
# def test(username: str = Depends(get_current_user), db: Session = Depends(get_db)):
#     print("richtige")
#     return oauth.get_user(username=username, db=db)


