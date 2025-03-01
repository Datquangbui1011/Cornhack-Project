from typing import Optional
from pydantic import BaseModel


# Base model that contains common fields
class CategoryBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


# Model used for creating a new category
class CategoryCreate(CategoryBase):
    pass


# Model used for updating a category; all fields are optional
class CategoryUpdate(BaseModel):
    name: Optional[str] = None

    class Config:
        from_attributes = True


# Model for reading a category (includes the auto-generated id)
class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True
