from typing import List, Optional
from pydantic import BaseModel


class Category(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# Note: Forward references (e.g., "Project") should be updated
# after importing all models in a central place.
