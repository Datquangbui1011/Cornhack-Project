from typing import Optional
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    role: str

    class Config:
        from_attributes = True


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    id: int
    email: str
    hashed_password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True
