from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.models.category import Category
from app.models.user_project import UserProject


class Project(BaseModel):
    id: int
    project_name: str
    description: Optional[str] = None
    dificulty: int
    category: Category
    created_at: datetime
    updated_at: datetime
    # Reference to UserProject model (defined in another file)

    class Config:
        from_attributes = True


class ProjectCreate(BaseModel):
    project_name: str
    description: Optional[str] = None
    dificulty: int
    categoryId: int

    class Config:
        from_atributes = True

class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    description: Optional[str] = None
    dificulty: Optional[int] = None
    categoryId: Optional[int] = None
    
    class Config:
        from_attributes = True