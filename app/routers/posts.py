from typing import List, Optional
from .. import model,schemas,utils
from fastapi import APIRouter, Body, Depends, FastAPI, HTTPException, Query, Response,status
from sqlalchemy import func
from ..schemas import PostOut
from ..database import create_db_and_tables,SessionDep,Session, get_session
from .oauth2 import get_user_token


router=APIRouter(
    prefix="/createpost",
    tags=['Posts']
)
    
items_post=[{"title":"title of post1", "content":"content of post1","id":1},{"title":"title of post 2 " , "content":"content of post 2","id":2}]

@router.get("/items",response_model=List[schemas.PostOut])
def get_items(session:SessionDep):
    # cursor.execute("""SELECT * FROM "Posts" """)
    # post=cursor.fetchall()
    # print(post)
    # This is public means we get all the post in the database
    # post=session.query(model.Post).limit(limit).offset(skip).all()
    
    # post=session.query(model.Post).filter(model.Post.title.contains(search)).limit(limit).all()
    
    post_two = session.query(model.Post, func.count(model.Vote.post_id).label("votes")).join(
        model.Vote, model.Vote.post_id == model.Post.id, isouter=True).group_by(model.Post.id).all()
    
    print("This is post two:",post_two)

    # db_query=session.query()
    # print("This is the count",db_query)
    
    # This is private that is only those posts that are created by the particular user we will get.
    # post=session.query(model.Post).filter(model.Post.user_id==current_user.id).all()
    
    return post_two
    # return post_two

@router.post("/",response_model=schemas.Post)
def create_post(data:schemas.PostCreate,response:Response,session:SessionDep,current_user:int=Depends(get_user_token)):
    # print(data.dict())
    # print(data.json())
    # post_dict=data.dict()
    # post_dict['id']=randrange(1,100000)
    # items_post.append(post_dict)
    # cursor.execute("""INSERT INTO "Posts" ("content","title","published") VALUES (%s,%s,%s) RETURNING * """,(data.content,data.title,data.published))
    # new_post=cursor.fetchone()
    # print(new_post)
    # conn.commit()
    # print(**data.dict())
    print("This is the current user id ",current_user.id)
    response.status_code=status.HTTP_201_CREATED
    # # new_post=model.Post(title=data.title,content=data.content,published=data.published)
    print("This is the current user ",current_user)
    new_post = model.Post(user_id=current_user.id,**data.dict())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)
    return new_post

@router.get("/latest")
def latest_post():
    print(len(items_post))
    latest=items_post[len(items_post)-1]
    return latest

def find_post(id):  
    for p in items_post:
        if p['id'] == id:
            return p
         
def find_index_post(id:int):
    for i, p in enumerate(items_post):
        if p['id']==id:
            return i
        
# retreiving single post
@router.get("/{id}",response_model=schemas.Post)
def get_post(id:int,response:Response,session:SessionDep,current_user:int=Depends(get_user_token)):
    # cursor.execute("""SELECT * FROM "Posts" where "id"=%s """,(str(id)))
    # data=cursor.fetchone()
    # post=session.query(model.Post).get(id)
    post=session.query(model.Post).filter(model.Post.id==id).first()
    print("This is the current user",current_user)
    print("This is the post",post)
    if not post:
        # response.status_code=404  this can be used if we know the status code 
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with id {id} not found"
    )
    # print(data)
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def del_post(id:int,session:SessionDep,current_user:int=Depends(get_user_token)):
    # index=find_index_post(id)
    # response.status_code=status.
    # cursor.execute("""DELETE FROM "Posts" where "id"=%s returning *""",(str(id),))
    # data=cursor.fetchone()
    # conn.commit()
    # print(data)
    data=session.query(model.Post).filter(model.Post.id==id).first()
    
    print("Data using filter()------->",data)
    
    data1=session.query(model.Post).get(id)
    print("Data using get()------->",data1)
    
    if data==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The post with {id} does not exist')
    print("This is the current user",current_user)
    print("Data user_id",data.user_id)
    if data.user_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform this operation")
    session.delete(data)
    session.commit()
    # session.refresh(data)
    # items_post.pop(data)
    # return Response()

# Updation 
@router.put("/{id}")
def update_post(id:int,post:schemas.PostCreate,session:SessionDep,current_user:int=Depends(get_user_token)):
    # index=find_index_post(id)
    # cursor.execute("""UPDATE "Posts" set title=%s,content=%s where id=%s RETURNING *""",(post.title,post.content,str(id)))
    # data=cursor.fetchone()
    data=session.query(model.Post).filter(model.Post.id==id)
    data_first=data.first()
    # data.update(post.dict(),synchronize_session=False)
    # print(data)
    # conn.commit()
    if data_first==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'The post with {id} does not exist')
    if data_first.user_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform this operation")
    data.update(post.dict(),synchronize_session=False)
    session.commit()
    # session.refresh(post)
    # my_post=post.dict()
    # my_post['id']=id
    # items_post[index]=my_post
    return data.first()
    