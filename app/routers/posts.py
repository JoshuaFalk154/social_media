from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from .. import models, oauth, schemas, utils
from ..database import SessionLocal, engine, get_db

router = APIRouter()


@router.post("", response_model=schemas.Post)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    username: str = Depends(oauth.get_current_user),
):

    user_db = utils.get_user_by_username(username=username, db=db)
    if user_db.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    post_db_model = models.Post(**post.model_dump())
    db.add(post_db_model)
    db.commit()
    db.refresh

    return post_db_model


@router.get("/{post_id}", response_model=schemas.Post)
def get_post(
    post_id: int,
    db: Session = Depends(get_db),
    username: str = Depends(oauth.get_current_user),
):
    db_post = db.query(models.Post).filter_by(id=post_id).first()

    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Post does not exist"
        )
    return db_post


@router.get("", response_model=list[schemas.Post])
def get_posts(
    username: str = Depends(oauth.get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(ge=0, le=100, default=10),
    skip: int | None = Query(ge=0, default=0),
    search: str | None = "",
):
    post_list = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return post_list


@router.delete("/{post_id}")
def delete_post(
    post_id: int,
    username: str = Depends(oauth.get_current_user),
    db: Session = Depends(get_db),
):
    db_user = utils.get_user_by_username(username=username, db=db)
    db_post = utils.get_post_by_id(id=post_id, db=db)

    if db_post.owner_id != db_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    db.query(models.Post).filter_by(id=post_id).delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(
    post: schemas.PostCreate,
    post_id: int,
    username: str = Depends(oauth.get_current_user),
    db: Session = Depends(get_db),
):
    db_user = utils.get_user_by_username(username=username, db=db)
    db_post = utils.get_post_by_id(id=post_id, db=db)

    if db_post.owner_id != db_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not author of post"
        )

    post_data = post.model_dump()
    for key, value in post_data.items():
        setattr(db_post, key, value)

    db.commit()
    db.refresh(db_post)

    return db_post
