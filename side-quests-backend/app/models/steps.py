from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from app.models.step_breakdown import (
    StepBreakdown,
    StepBreakdownCreate,
    StepBreakdownUpdate,
)


class StepsBase(BaseModel):
    description: str


class StepCreate(StepsBase):
    stepbreakdown: List[StepBreakdownCreate] = None
    
class StepsCreateRequest(BaseModel):
    project_id: int
    step_ids: List[int]

class StepUpdate(BaseModel):
    completed: bool


class Step(StepsBase):
    id: int
    stepbreakdown: Optional[List[StepBreakdown]] = []

    class Config:
        from_attribute = True


class StepsCompleted(Step):
    completed: bool

    class Config:
        from_attributes = True
class StepCompletedTable(BaseModel):
    id: int
    userProjectId: int
    stepsId: int
    completed: bool
