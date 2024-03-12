from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import config, database, models, schemas, utils
from .database import get_db

SECRET_KEY = f"{config.settings.secret_key}"
ALGORITHM = f"{config.settings.algorithm}"
ACCESS_TOKEN_EXPIRE_MINUTES = f"{config.settings.access_token_expire_minutes}"

oauth2_scheme = OAuth2PasswordBearer("/token")


def authenticate_user(username: str, password: str, db: Session):
    user_db = utils.get_user_by_username(username=username, db=db)
    if not utils.verify_password(password, user_db.hashed_password):
        return False
    return user_db


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = verify_access_token(token, credentials_exception=credentials_exception)
    user = utils.get_user_by_username(username=token.username, db=db)

    return user.username
