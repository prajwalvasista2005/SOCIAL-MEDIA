from .. import models,schemas,oauth2
from fastapi import  status,HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func


router=APIRouter(
    prefix="/sqlalchemy",tags=["Posts"]
)
@router.post("",response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):     
    new_post=models.Post(owner_id=current_user.id,**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post 

@router.get("/{id}", response_model=schemas.PostOut)
def find_post(id: int,db: Session = Depends(get_db),
current_user: models.User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")

    return {
        "post": post.Post,
        "votes": post.votes
    }

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post:schemas.UpdatePost,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post=post_query.first()

    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.owner_id !=current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")

    post_query.update(updated_post.model_dump())
    db.commit()
    return post_query.first()

@router.delete("/{id}")
def delete_post(id:int,db:Session=Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if  post== None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found")

    if post.owner_id !=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    return post
@router.get("", response_model=List[schemas.PostOut])
def get_all(db: Session = Depends(get_db),current_user: models.User = Depends(oauth2.get_current_user),limit: int = 10,skip: int = 0,search: Optional[str] = ""):
    results = db.query(models.Post,func.count(models.Votes.post_id).label("votes")).join(models.Votes,models.Votes.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return [
        {
            "post": row.Post,
            "votes": row.votes
        }
        for row in results
    ]