from typing import List, Optional
from pydantic import BaseModel

from app.models.user_project import UserProject

class User(BaseModel):
    id: int
    username: str
    hashed_password: str
    email: str
    role: str
    # Reference to UserProject model (defined in another file)
    user_projects: Optional[List[UserProject]] = []

    class Config:
        orm_mode = True
