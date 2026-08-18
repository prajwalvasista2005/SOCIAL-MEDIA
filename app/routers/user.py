from fastapi import APIRouter, Depends, File, HTTPException, Query, status, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .. import models, schemas, utils, oauth2,cloudinary_utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut,
)
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    hashed_password = utils.hash(user.password)

    user_data = user.model_dump()
    user_data["password"] = hashed_password

    new_user = models.User(**user_data)

    db.add(new_user)

    try:
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    return new_user


@router.get(
    "/",
    response_model=list[schemas.UserOut],
)
def get_all_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
    search: str | None = Query(default=None, max_length=50),
):
    query = db.query(models.User).filter(
        models.User.id != current_user.id
    )

    if search:
        query = query.filter(
            models.User.username.ilike(f"%{search}%")
        )

    return query.limit(20).all()
@router.get(
    "/me",
    response_model=schemas.UserProfile,
)
def get_me(
    current_user: models.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    followers_count = (
        db.query(models.Follow)
        .filter(models.Follow.following_id == current_user.id)
        .count()
    )

    following_count = (
        db.query(models.Follow)
        .filter(models.Follow.follower_id == current_user.id)
        .count()
    )

    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "profile_picture_url": current_user.profile_picture_url,
        "followers_count": followers_count,
        "following_count": following_count,
    }

@router.get(
    "/{id}",
    response_model=schemas.UserProfile,
)
def find_user(
    id: int,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist",
        )

    followers_count = (
        db.query(models.Follow).filter(models.Follow.following_id == id).count()
    )

    following_count = (
        db.query(models.Follow).filter(models.Follow.follower_id == id).count()
    )

    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "followers_count": followers_count,
        "following_count": following_count,
    }


@router.put(
    "/{id}",
    response_model=schemas.UserOut,
)
def update_user(
    id: int,
    updated_user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist",
        )

    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    updated_data = updated_user.model_dump(exclude_unset=True)

    if "password" in updated_data:
        updated_data["password"] = utils.hash(updated_data["password"])

    for field, value in updated_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(oauth2.get_current_user),
):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The user with id {id} was not found",
        )

    if user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform requested action",
        )

    db.delete(user)
    db.commit()

    return None


@router.get(
    "/{id}/followers",
    response_model=list[schemas.UserOut],
)
def get_followers(
    id: int,
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    followers = (
        db.query(models.User)
        .join(
            models.Follow,
            models.Follow.follower_id == models.User.id,
        )
        .filter(models.Follow.following_id == id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    return followers


@router.get(
    "/{id}/following",
    response_model=list[schemas.UserOut],
)
def get_following(
    id: int,
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    skip: int = Query(0, ge=0),
):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    following = (
        db.query(models.User)
        .join(
            models.Follow,
            models.Follow.following_id == models.User.id,
        )
        .filter(models.Follow.follower_id == id)
        .limit(limit)
        .offset(skip)
        .all()
    )

    return following

@router.post("/me/profile-picture")
def upload_profile_picture(
    file: UploadFile = File(...),
    current_user: models.User = Depends(oauth2.get_current_user),
    db: Session = Depends(get_db),
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must be an image"
        )

    if current_user.profile_picture_public_id:
        cloudinary_utils.delete_image(
        current_user.profile_picture_public_id
    )

    upload_result = cloudinary_utils.upload_image(file.file)
    print(upload_result)

    current_user.profile_picture_url = upload_result["url"]
    current_user.profile_picture_public_id = upload_result["public_id"]

    db.commit()
    db.refresh(current_user)

    return {
        "profile_picture_url": current_user.profile_picture_url
    }
