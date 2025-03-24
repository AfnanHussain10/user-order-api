from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.auth import auth_service
from app.schemas.auth import Token, RefreshToken

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    
    #Get access and refresh tokens for a user
    token = auth_service.login(db, form_data.username, form_data.password)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.post("/refresh", response_model=Token)
def refresh_token(
    refresh_token_schema: RefreshToken,
    db: Session = Depends(get_db),
) -> Token:

    #Get new access token from refresh token
    token = auth_service.refresh_token(db, refresh_token_schema.refresh_token)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token