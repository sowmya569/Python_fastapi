# from typing import Annotated

# from fastapi import Depends, FastAPI, HTTPException, Query
from typing import List, Optional
from sqlalchemy import Column, ForeignKey, Integer
from sqlmodel import Field, Relationship, SQLModel
from datetime import datetime
from sqlalchemy.sql import func

# class Post(SQLModel, table=True):
#     __tablename__="Posts"
#     id: int= Field(primary_key=True)
#     content: str = Field(index=True)
#     title: str = Field(index=True)
#     published:bool|None =Field(default=True)
#     created_at: datetime|None = Field(default_factory=datetime.utcnow)
#     user_id: int = Field(foreign_key="user.id", nullable=False) 
#     user: "User" = Relationship(back_populates="posts")
    
class Post(SQLModel, table=True):
    __tablename__ = "posts"
    id: int = Field(primary_key=True)
    content: str = Field(index=True)
    title: str = Field(index=True)
    published: bool = Field(default=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="user.id", nullable=False) 
    user: "User" = Relationship(back_populates="posts")
    
class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int = Field(primary_key=True)
    email: str = Field(nullable=False, index=True)
    password: str = Field(nullable=False)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    posts: List["Post"] = Relationship(back_populates="user")
    phone_number:str = Field(nullable=False)
    
class Vote(SQLModel,table=True):
    __tablename__= "votes"
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    post_id: int = Field(foreign_key="posts.id", primary_key=True)
