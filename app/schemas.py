from pydantic import BaseModel
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str = None

class TaskUpdate(BaseModel):
    title: str = None
    description: str = None
    completed: bool = None

class Task(BaseModel):
    id: int
    title: str
    description: str = None
    completed: bool
    created_at: datetime

    class Config:
        orm_mode = True
