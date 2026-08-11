from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(
    prefix="/comments",
    tags=["Comments"],
)


@router.post(
    "/{post_id}",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.CommentResponse,
)
def create_comment(
    comment: schemas.CommentCreate,
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

    new_comment = models.Comment(
        content=comment.content,
        post_id=post_id,
        user_id=current_user.id,
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment


@router.get(
    "/{post_id}",
    response_model=list[schemas.CommentResponse],
)
def get_comments(
    post_id: int,
    db: Session = Depends(get_db),
):
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).all()

    return comments


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_comment(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    comment = db.query(models.Comment).filter(models.Comment.id == id).first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comment not found",
        )

    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    db.delete(comment)
    db.commit()

    return None
