from .. import models,schemas,utils
from fastapi import status,HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db


router=APIRouter(
    prefix="/users",tags=["Users"]
)
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/",response_model=list[schemas.UserOut])
def get_all_users(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    return users

@router.get("/{id}",response_model=schemas.UserOut)
def find_user(id:int,db:Session=Depends(get_db)):
    user=db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"user with id {id} does not exist")
    return user

@router.put("/{id}",response_model=schemas.UserOut)
def update_user(id:int,updated_user:schemas.UserUpdate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id==id)
    if user_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with id {id} does not exist")
    updated_data = updated_user.model_dump(exclude_unset=True)
    if "password" in updated_data:
        updated_data["password"] = utils.hash(updated_data["password"])
    user_query.update(updated_data)
    db.commit()
    updated = user_query.first()
    return updated
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id:int,db:Session=Depends(get_db)):
    user_delete=db.query(models.User).filter(models.User.id==id)
    if user_delete.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the user with id {id} not found")
    user_delete.delete(synchronize_session=False)
    db.commit()
    return {"message":"User deleted successfully"}
