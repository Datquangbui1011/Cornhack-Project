from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from app.models.user_project import UserProject

class Project(BaseModel):
    id: int
    project_name: str
    description: Optional[str] = None
    dificulty: int
    categoryId: int
    created_at: datetime
    updated_at: datetime
    # Reference to UserProject model (defined in another file)
    user_projects: Optional[List[UserProject]] = []

    class Config:
        orm_mode = True
