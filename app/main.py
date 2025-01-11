# from random import randrange
# from typing import Optional
# from urllib import response
from fastapi import Body, FastAPI, HTTPException, Query, Response,status
from pydantic import BaseModel
from typing import List
from psycopg2.extras  import RealDictCursor
import psycopg2
import time
from . import model,schemas,utils
from .model import SQLModel
from .database import create_db_and_tables,SessionDep
from .routers import posts,users,auth,vote
from fastapi.middleware.cors import CORSMiddleware


origins=['https://www.google.com/']

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# We can define the schema in different file, it would be better way to structure a file

# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool = True
    # body:bool=True
    # rating:Optional[int]=None
    # id:int


# def create_post(post: schemas.PostCreate):
#     db = SessionDep()
#     db_post = schemas.Post(**post.dict())  
#     db.add(db_post)
#     db.commit()
#     db.refresh(db_post)
#     return db_post



# @app.get("/check_table")
# def check_table():
#     try:
#         # Query to check if the Posts table exists
#         result = connection.execute("""
#             SELECT *
#             FROM information_schema.tables 
#             WHERE table_name = 'Posts';
#         """)
#         table = result.fetchall()
        
#         if table:
#             return {"Table exists": True}
#         else:
#             return {"Table exists": False}
    
#     except Exception as e:
#         return {"error": str(e)}

@app.get("/sqlalchemy")
def test_post(session: SessionDep):
    post=session.query(model.Post).all() #importing the model Post from model.py file
    # return{"posts":post} here instead of returning a json we can return the post ,fastapi will automatically serialize it and convert it to json, DO IT IN ALL THE RETURN STATEMENT
    return post

while True:   
    try:
        conn = psycopg2.connect(host='localhost',database='FastAPI',user='postgres',password='SQLpost',cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("connection successful")
        # print(type(connection))
        break
    except Exception as e:
        print("Connection failed!!")
        print("Error:",e)
        time.sleep(5)
        
# @app.get("/")
# def get_post():
#     return {"hello"}

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)
app.include_router(vote.router)