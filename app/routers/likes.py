from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import database, models, oauth, schemas, utils
from ..database import get_db

router = APIRouter()


@router.post("")
def like_post(like: schemas.LikeCreate, db: Session = Depends(get_db), username = Depends(oauth.get_current_user)):

    user_db = utils.get_user_by_id(id=like.user_id, db=db)
    post_db = utils.get_post_by_id(id=like.post_id, db=db)
    like_db = (
        db.query(models.Like).filter_by(user_id=user_db.id, post_id=post_db.id).first()
    )

    if user_db.username != username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    if like.direction == 1 and like_db:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You can not like the same post twice",
        )

    if like.direction == 0 and like_db is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You can not unlike a post wich you did not like",
        )

    if like.direction == 1:
        new_like = models.Like(user_id=like.user_id, post_id=like.post_id)
        db.add(new_like)
        db.commit()
        return {"message": "Post liked successfully"}

    db.delete(like_db)
    db.commit()
    return {"message": "Like removed successfully"}
