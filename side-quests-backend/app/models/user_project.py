from typing import List, Optional
from pydantic import BaseModel

from app.models.steps_completed import StepsCompleted


class UserProject(BaseModel):
    id: int
    userId: int
    projectId: int
    completed: bool
    # Reference to StepsCompleted model (defined in another file)
    steps_completed: Optional[List[StepsCompleted]] = []

    class Config:
        from_attributes = True
