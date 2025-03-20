from typing import List, Optional

from app.repositories.user import user_repository
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.models.user import User
from sqlalchemy.orm import Session


class UserService:
    def get(self, db: Session, user_id: int) -> Optional[User]:
        #Get a user by ID
        return user_repository.get(db=db, id=user_id)
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        #Get a user by email
        return user_repository.get_by_email(db=db, email=email)
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        #Get a user by username
        return user_repository.get_by_username(db=db, username=username)
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        #Get all users with pagination
        return user_repository.get_multi(db=db, skip=skip, limit=limit)
    
    def create(self, db: Session, user_in: UserCreate) -> User:
    
        existing_user = self.get_by_email(db=db, email=user_in.email)
        if existing_user:
            raise ValueError("Email already registered")
        
        existing_username = self.get_by_username(db=db, username=user_in.username)
        if existing_username:
            raise ValueError("Username already taken")
        
        return user_repository.create(db=db, obj_in=user_in)
    
    def update(self, db: Session, user_id: int, user_in: UserUpdate) -> Optional[User]:

        db_obj = self.get(db=db, user_id=user_id)
        if not db_obj:
            return None
        
        # If email is being updated, check it's not already taken
        if user_in.email and user_in.email != db_obj.email:
            existing_user = self.get_by_email(db=db, email=user_in.email)
            if existing_user:
                raise ValueError("Email already registered")
        
        # If username is being updated, check it's not already taken
        if user_in.username and user_in.username != db_obj.username:
            existing_username = self.get_by_username(db=db, username=user_in.username)
            if existing_username:
                raise ValueError("Username already taken")
        
        return user_repository.update(db=db, db_obj=db_obj, obj_in=user_in)
    
    def delete(self, db: Session, user_id: int) -> Optional[User]:
        
        db_obj = self.get(db=db, user_id=user_id)
        if not db_obj:
            return None
        
        return user_repository.remove(db=db, id=user_id)
    
    def is_admin(self, user: User) -> bool:
        
        return user_repository.is_admin(user=user)


user_service = UserService()