from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2
from datetime import datetime, timedelta, timezone

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid Credentials"
        )
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})
    refresh_token = oauth2.create_refresh_token()
    hashed_refresh_token = utils.hash_refresh_token(refresh_token)
    db_refresh_token = models.RefreshToken(
        user_id=user.id,
        token_hash=hashed_refresh_token,
        expires_at=datetime.now() + timedelta(days=30),
    )
    db.add(db_refresh_token)
    db.commit()
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=schemas.AccessTokenResponse)
def refresh_token(
    refresh_token_data: schemas.RefreshtokenRequest,
    db: Session = Depends(database.get_db),
):
    hashed_refresh_token = utils.hash_refresh_token(refresh_token_data.refresh_token)
    db_refresh_token = (
        db.query(models.RefreshToken)
        .filter(models.RefreshToken.token_hash == hashed_refresh_token)
        .first()
    )

    if not db_refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    if db_refresh_token.revoked:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )

    if db_refresh_token.expires_at < datetime.now(timezone.utc):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
        )
    access_token = oauth2.create_access_token(
        data={"user_id": db_refresh_token.user_id}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout(refresh_token_data: schemas.RefreshtokenRequest,db: Session = Depends(database.get_db),):
    hashed_refresh_token = utils.hash_refresh_token(refresh_token_data.refresh_token)


    db_refresh_token = (  
    db.query(models.RefreshToken)
    .filter(models.RefreshToken.token_hash == hashed_refresh_token)
    .first()
)

    if not db_refresh_token:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
    )

    db_refresh_token.revoked = True

    db.commit()
    return {"message": "Successfully logged out"}
