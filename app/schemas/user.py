from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: Optional[str] = None
    can_add_users: Optional[bool] = False

class UserLogin(BaseModel):
    email: EmailStr
    password: Optional[str] = None

class User(UserBase):
    id: int
    can_add_users: bool

    class Config:
        from_attributes = True
