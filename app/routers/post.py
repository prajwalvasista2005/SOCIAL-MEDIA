from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Post,
)
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    new_post = models.Post(
        owner_id=current_user.id,
        **post.model_dump(),
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.get(
    "/{id}",
    response_model=schemas.PostDetail,
)
def find_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    result = (
        db.query(
            models.Post,
            func.count(models.Votes.post_id.distinct()).label("votes"),
        )
        .outerjoin(
            models.Votes,
            models.Votes.post_id == models.Post.id,
        )
        .filter(models.Post.id == id)
        .group_by(models.Post.id)
        .first()
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )

    comments = db.query(models.Comment).filter(models.Comment.post_id == id).all()

    return {
        "post": result.Post,
        "votes": result.votes,
        "comments_count": len(comments),
        "comments": comments,
    }


@router.put(
    "/{id}",
    response_model=schemas.Post,
)
def update_post(
    id: int,
    updated_post: schemas.UpdatePost,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    updated_data = updated_post.model_dump()

    for field, value in updated_data.items():
        setattr(post, field, value)

    db.commit()
    db.refresh(post)

    return post


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found",
        )

    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    db.delete(post)
    db.commit()

    return None


@router.get(
    "",
    response_model=list[schemas.PostFeed],
)
def get_all(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
    search: Optional[str] = Query(
        default=None,
        max_length=100,
    ),
):
    query = (
        db.query(
            models.Post,
            func.count(models.Votes.post_id.distinct()).label("votes"),
            func.count(models.Comment.id.distinct()).label("comments_count"),
        )
        .outerjoin(
            models.Votes,
            models.Votes.post_id == models.Post.id,
        )
        .outerjoin(
            models.Comment,
            models.Comment.post_id == models.Post.id,
        )
        .group_by(models.Post.id)
    )

    if search:
        query = query.filter(models.Post.title.contains(search))

    results = query.limit(limit).offset(skip).all()

    return [
        {
            "post": row.Post,
            "votes": row.votes,
            "comments_count": row.comments_count,
        }
        for row in results
    ]
