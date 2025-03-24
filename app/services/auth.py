from datetime import timedelta
from typing import Optional

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.repositories.user import user_repository
from app.schemas.auth import Token
from jose import jwt, JWTError
from sqlalchemy.orm import Session


class AuthService:
    @staticmethod
    def login(db: Session, email: str, password: str) -> Optional[Token]:

        #Authenticate user and return tokens
        user = user_repository.authenticate(db=db, email=email, password=password) 
        if not user:
            return None
        
        access_token = create_access_token(
            subject=user.id,
            role=user.role,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_refresh_token(subject=user.id, role=user.role)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token
        )

    @staticmethod
    def refresh_token(db: Session, refresh_token: str) -> Optional[Token]:
        
        #Create new access token from refresh token

        
        
        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id: int = int(payload.get("sub"))
            if user_id is None:
                return None
        except JWTError:
            return None
        
        user = user_repository.get(db=db, id=user_id)
        if not user:
            return None
        
        access_token = create_access_token(
            subject=user.id,
            role=user.role,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        new_refresh_token = create_refresh_token(subject=user.id, role=user.role)
        
        return Token(
            access_token=access_token,
            refresh_token=new_refresh_token
        )


auth_service = AuthService()