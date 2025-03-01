from pydantic import BaseModel

class StepsCompleted(BaseModel):
    id: int
    userProjectId: int
    stepsId: int
    completed: bool

    class Config:
        orm_mode = True
