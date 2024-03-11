# für zyklisches referenzieren
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


# Base
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., max_length=255)


# creating
class UserCreate(UserBase):
    password: str = Field(..., max_length=255)


# reading data
class User(UserBase):
    id: int
    created_at: datetime
    posts: list[PostMinimal]

    class Config:
        from_attributes = True


# das wird zum Post als Info über owner zurückgegeben
class UserMinimal(BaseModel):
    id: int
    username: str


class PostBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str = Field(..., max_length=10000)
    public: bool
    owner_id: int


class PostCreate(PostBase):
    pass


class Post(BaseModel):
    id: int
    owner: User
    likes: list[UserMinimal] = []

    @property
    def amount_likes(self) -> int:
        return len(self.likes)

    class Config:
        from_attributes = True


# wird zum User ausgegeben, also wenige Infos pro Post von ihm
class PostMinimal(BaseModel):
    id: int
    title: str


class LikeBase(BaseModel):
    user_id: int
    post_id: int


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    liker: User
    post: Post

    class Config:
        from_attributes = True
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
