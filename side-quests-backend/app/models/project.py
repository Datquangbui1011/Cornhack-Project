from typing import List, Optional
from pydantic import BaseModel

from app.models.category import Category


class ProjectBase(BaseModel):
    project_name: str
    description: Optional[str] = None
    dificulty: int


class Project(ProjectBase):
    id: int
    category: Category

    class Config:
        from_attributes = True


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    description: Optional[str] = None
    dificulty: Optional[int] = None

    class Config:
        from_attributes = True


class ProjectCreate(ProjectBase):
    category_id: int

    class Config:
        from_attributes = True


from typing import List, Optional
from pydantic import BaseModel
from app.models.category import Category

# Ensure the import for UserProject is correct if needed


class ProjectBase(BaseModel):
    project_name: str
    description: Optional[str] = None
    dificulty: int


class Project(ProjectBase):
    id: int
    category: Category

    class Config:
        model_config = {"from_attributes": True}


class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    description: Optional[str] = None
    dificulty: Optional[int] = None

    class Config:
        model_config = {"from_attributes": True}


class ProjectCreate(ProjectBase):
    category_id: int

    class Config:
        model_config = {"from_attributes": True}


class ProjectFromUser(Project):
    completed: bool

    class Config:
        model_config = {"from_attributes": True}
