from typing import Generator, Optional, Tuple
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.repositories.user import user_repository
from app.schemas.auth import TokenPayload
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def decode_token(token: str = Depends(oauth2_scheme)) -> TokenPayload:
    """
    Decode and validate the JWT token, returning the token payload
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
        return token_data
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


def get_current_user(
    db: Session = Depends(get_db), token_data: TokenPayload = Depends(decode_token)
) -> User:
    """
    Get the current user from the database using the user ID from the token
    """
    user = user_repository.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_admin(
    db: Session = Depends(get_db), token_data: TokenPayload = Depends(decode_token)
) -> User:
    """
    Get the current admin user. First checks if the user has admin role from token,
    then fetches the user from the database.
    """
    # Check role from token data
    print(token_data.role)
    if not token_data.role or token_data.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="The user doesn't have enough privileges",
        )
    
    # After role validation, fetch the user from database
    user = user_repository.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # # Double-check admin status in the database (optional additional security)
    # if not user_repository.is_admin(user):
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="The user doesn't have admin privileges in the database",
    #     )
    
    return user