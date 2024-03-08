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
    posts: list[Post]

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str = Field(..., max_length=10000)
    public: bool
    owner_id: int


class CreatePost(PostBase):
    pass


class Post(BaseModel):
    id: int
    owner: User
    likes: list[User] = []

    @property
    def amount_likes(self) -> int:
        return len(self.likes)

    class Config:
        orm_mode = True


class LikeBase(BaseModel):
    user_id: int
    post_id: int


class LikeCreate(LikeBase):
    pass


class Like(LikeBase):
    liker: User
    post: Post

    class Config:
        orm_mode = True
