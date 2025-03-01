from pydantic import BaseModel

class StepBreakdown(BaseModel):
    id: int
    stepsId: int

    class Config:
        orm_mode = True
