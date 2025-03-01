from typing import List, Optional
from pydantic import BaseModel

from app.models.project import Project
class Category(BaseModel):
    id: int
    name: str
    # Reference to Project model (defined in another file)
    projects: Optional[List[Project]] = []

    class Config:
        orm_mode = True

# Note: Forward references (e.g., "Project") should be updated
# after importing all models in a central place.
