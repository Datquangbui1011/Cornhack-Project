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


class StepUpdate(BaseModel):
    description: Optional[str] = None
    stepbreakdown: Optional[List[StepBreakdownUpdate]] = None


class Steps(StepsBase):
    id: int
    stepbreakdown: Optional[List[StepBreakdown]] = []

    class Config:
        from_attribute = True
