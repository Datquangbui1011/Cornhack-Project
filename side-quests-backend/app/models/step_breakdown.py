from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class StepBreakdownBase(BaseModel):
    description: str


class StepBreakdownCreate(StepBreakdownBase):
    pass


class StepBreakdownUpdate(BaseModel):
    description: Optional[str] = None


class StepBreakdown(StepBreakdownBase):
    id: int

    class Config:
        orm_mode = True
