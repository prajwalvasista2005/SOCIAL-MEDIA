from pydantic import BaseModel, ConfigDict, conint
from datetime import datetime
from pydantic import EmailStr
from typing import Optional, Annotated

class PostBase(BaseModel):
    title:str
    content:str
    published:bool=True

class UpdatePost(PostBase):
    pass
class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: "UserOut"

    model_config = ConfigDict(from_attributes=True)

class PostOut(BaseModel):
    post:Post
    votes:int
    model_config=ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    model_config=ConfigDict(from_attributes=True)
class UserUpdate(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str
class TokenData(BaseModel):
    id:Optional[int]=None

class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, conint(le=1)]


