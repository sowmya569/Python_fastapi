import time
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
import psycopg2
from sqlmodel import Session, SQLModel, create_engine
from .config import settings

        
# from .config import 

# SQLALCHEMY_DATABASE_URL='postgresql://postgres:SQLpost@localhost/FastAPI'
# engine=create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal=Session(autocommit=False,autoflush=False,bind=engine)


# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session


# SessionDep = Annotated[Session, Depends(get_session)]
 
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

Base=declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]