from .database import Base
from sqlalchemy import TIMESTAMP, Column, Integer, String, Boolean, text, ForeignKey
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = "posts"
    id: int = Column(Integer, primary_key=True, nullable=False)
    title: str = Column(String, nullable=False)
    content: str = Column(String, nullable=False)
    published: bool = Column(Boolean, server_default="TRUE", nullable=False)
    image_url:str=Column(String,nullable=True)
    image_public_id:str=Column(String,nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner_id: int = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    owner = relationship("User", back_populates="posts")


class User(Base):
    __tablename__ = "users"
    id: int = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    profile_picture_url=Column(String,nullable=True)
    profile_picture_public_id = Column(String, nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    posts = relationship("Post", back_populates="owner")


class Votes(Base):
    __tablename__ = "votes"
    user_id: int = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id: int = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )


class Comment(Base):
    __tablename__ = "comments"
    id: int = Column(Integer, primary_key=True, nullable=False)
    content: str = Column(String, nullable=False)
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    owner = relationship("User")
    post = relationship("Post")


class Follow(Base):
    __tablename__ = "followers"
    follower_id: int = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    following_id: int = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        index=True,
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class SavedPost(Base):
    __tablename__ = "saved_posts"
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    )
    post_id = Column(
        Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True
    )
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

class RefreshToken(Base):
    __tablename__="refresh_tokens"
    id=Column(Integer,primary_key=True,nullable=False)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    token_hash=Column(String,nullable=False,index=True)
    created_at = Column(
            TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
        )
    expires_at = Column(
    TIMESTAMP(timezone=True),
    nullable=False
    )
    revoked=Column(Boolean,default=False,nullable=False)

    