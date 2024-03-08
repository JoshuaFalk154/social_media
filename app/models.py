from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base

"""
CREATE TABLE User (
	id SERIAL PRIMARY KEY,
	email VARCHAR(255) NOT NULL,
	username VARCHAR(40) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
	created_at TIMESTAMP NOT NULL
);

CREATE TABLE Post (
	id SERIAL PRIMARY KEY,
	owner_id INTEGER NOT NULL,
	title VARCHAR(40) NOT NULL,
	content TEXT NOT NULL,  
	public BOOLEAN NOT NULL DEFAULT TRUE,
	created_at TIMESTAMP NOT NULL,
	FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE
);

CREATE TABLE Like (
	user_id INTEGER NOT NULL,
	post_id INTEGER NOT NULL,
	PRIMARY KEY (user_id, post_id),
	FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
FOREIGN KEY (post_
"""


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    posts = relationship("Post", back_populates="owner")
    likes = relationship("Like", back_populates="liker")


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    public = Column(Boolean, default=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    # owner_id = Column(Integer, ForeignKey("users.id"))
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    owner = relationship("User", back_populates="posts")
    likes = relationship("Like", back_populates="post")


class Like(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)

    liker = relationship("User", back_populates="likes")
    post = relationship("Post", back_populates="likes")
