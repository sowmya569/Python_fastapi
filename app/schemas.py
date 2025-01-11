from pydantic.types import conint
import datetime
from typing import Optional
from pydantic import BaseModel,EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    class Config:
        from_attributes = True 

# Extending from Post class, by passing "pass" keyword is  it the same as Post class 
class PostCreate(PostBase):
    pass
# Defining a different class for each function/operation would be a correct method because sometimes while updating we might require the user to explicitly update some fields, but while creating the field we might give a default value and create. 
# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# Removing the default from published cause we want the user to explicitly define the value for published,
# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool
                                    #  or
# Here by defining the class in this way, here we are tleling that they can update only published field, if they try to update any other field it will throw an error                                   
# class UpdatePost(BaseModel):
    # published:bool                        
 

#when the user creates a post when calling the api, user must not get back the password again so to overcome this we are creating a new schema 
class UserOut(BaseModel):
    email:EmailStr
    id:int
    created_at:datetime.datetime

class Post(PostBase):
    id: int
    created_at: datetime.datetime
    user_id:int
    user:UserOut
    class Config:
        from_attributes = True  
    
class UserCreate(BaseModel):
    email:EmailStr
    password:str

    
class UserLogin(BaseModel): 
    email:EmailStr
    password:str
    
class Token(BaseModel):
    access_token:str
    token_type:str
    
class TokenData(BaseModel):
    id:str
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) # type: ignore
    
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True