from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str
    role: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    username: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None  # If provided, this new password will be hashed.

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    id: int
    email: str
    username: str
    hashed_password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
