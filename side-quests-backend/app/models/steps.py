from typing import List, Optional
from pydantic import BaseModel

from app.models.step_breakdown import StepBreakdown
from app.models.steps_completed import StepsCompleted
class Steps(BaseModel):
    id: int
    description: str
    # References to StepBreakdown and StepsCompleted models
    stepbreakdown: Optional[List[StepBreakdown]] = []
    steps_completed: Optional[List[StepsCompleted]] = []

    class Config:
        from_attributes = True
