from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from .db import Base

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key = True, index = True)
    title = Column(String, index = True, nullable = False)
    description = Column(String, nullable = True)
    completed = Column(Boolean, default = False)
    created_at = Column(DateTime, default = func.now())
