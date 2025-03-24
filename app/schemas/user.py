from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime


# Shared properties
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


# Properties to receive on user creation
class UserCreate(UserBase):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "customer"

    @validator('role')
    def validate_role(cls, v):
        allowed_roles = ["admin", "customer"]
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of {allowed_roles}")
        return v


# Properties to receive on user update
class UserUpdate(UserBase):
    password: Optional[str] = None


# Properties to return to client
class UserResponse(UserBase):
    id: int
    role: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Additional properties stored in DB
class UserInDB(UserResponse):
    hashed_password: str

    class Config:
        from_attributes = True