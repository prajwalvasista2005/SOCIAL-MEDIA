from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix="/saved",
    tags=["Saved Posts"],
)


@router.post(
    "/{post_id}",
    status_code=status.HTTP_201_CREATED,
)
def save_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

    existing_save = (
        db.query(models.SavedPost)
        .filter(
            models.SavedPost.user_id == current_user.id,
            models.SavedPost.post_id == post_id,
        )
        .first()
    )

    if existing_save:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Post already saved",
        )

    new_save = models.SavedPost(
        user_id=current_user.id,
        post_id=post_id,
    )

    db.add(new_save)
    db.commit()

    return {"message": "Post saved successfully"}


@router.delete(
    "/{post_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def unsave_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    saved_post = (
        db.query(models.SavedPost)
        .filter(
            models.SavedPost.user_id == current_user.id,
            models.SavedPost.post_id == post_id,
        )
        .first()
    )

    if not saved_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post is not saved",
        )

    db.delete(saved_post)
    db.commit()

    return None


@router.get(
    "",
    response_model=list[schemas.PostDetail],
)
@router.get(
    "",
    response_model=list[schemas.PostDetail],
)
def get_saved_posts(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
):
    results = (
        db.query(
            models.Post,
            func.count(models.Votes.post_id.distinct()).label("votes"),
            func.count(models.Comment.id.distinct()).label("comments_count"),
        )
        .join(
            models.SavedPost,
            models.SavedPost.post_id == models.Post.id,
        )
        .outerjoin(
            models.Votes,
            models.Votes.post_id == models.Post.id,
        )
        .outerjoin(
            models.Comment,
            models.Comment.post_id == models.Post.id,
        )
        .filter(models.SavedPost.user_id == current_user.id)
        .group_by(models.Post.id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    response = []

    for row in results:
        comments = (
            db.query(models.Comment).filter(models.Comment.post_id == row.Post.id).all()
        )

        response.append(
            {
                "post": row.Post,
                "votes": row.votes,
                "comments": comments,
                "comments_count": row.comments_count,
            }
        )

    return response
