from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime



class PostCreate(BaseModel):
    title: str
    content: str
    

class PostUpdate(BaseModel):
    title:str
    content : str

    



class Post(BaseModel):
    title: str
    content: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class PostList(BaseModel):
    posts: List[Post]


class User(BaseModel):
    username : str
    email : Optional[str] = None
    full_name : Optional[str] = None
    disabled : Optional[bool] = None

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username : str
    password : str


class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    username: Optional[str] = None
