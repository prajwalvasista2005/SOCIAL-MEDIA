from datetime import datetime
from typing import List, Optional, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, conint


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    image_url: Optional[str] = None
    image_public_id: Optional[str] = None


class PostCreate(PostBase):
    pass


class UpdatePost(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: "UserOut"

    model_config = ConfigDict(from_attributes=True)


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    post_id: int
    user_id: int
    created_at: datetime
    owner: "UserOut"

    model_config = ConfigDict(from_attributes=True)


class PostDetail(BaseModel):
    post: Post
    votes: int
    comments_count: int
    comments: List[CommentResponse]

    model_config = ConfigDict(from_attributes=True)


class PostFeed(BaseModel):
    post: Post
    votes: int
    comments_count: int

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    username: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    profile_picture_url: str | None = None
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserProfile(BaseModel):
    id: int
    email: EmailStr
    username: str
    profile_picture_url: str | None = None
    followers_count: int
    following_count: int


class Token(BaseModel):
    access_token: str
    refresh_token:str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Literal[0, 1]


class Follow(BaseModel):
    following_id: int

class RefreshtokenRequest(BaseModel):
    refresh_token:str

class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str
  