from .database import Base
from sqlalchemy import TIMESTAMP, Column,Integer,String,Boolean, text, ForeignKey
from sqlalchemy.orm import relationship
class Post(Base):
    __tablename__="posts"
    id:int=Column(Integer,primary_key=True,nullable=False)
    title:str=Column(String,nullable=False)
    content:str=Column(String,nullable=False)
    published:bool=Column(Boolean,server_default='TRUE',nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id:int=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner=relationship("User")
class User(Base):
    __tablename__="users"
    id:int=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    posts=relationship("Post",back_populates="owner")

class Votes(Base):
    __tablename__="votes"
    user_id:int=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id:int=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
