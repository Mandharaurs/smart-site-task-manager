from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_to: Optional[str]
    due_date: Optional[datetime]
    created_by: Optional[str]

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    category: Optional[str]
    priority: Optional[str]
    status: Optional[str]
    assigned_to: Optional[str]
    due_date: Optional[datetime]
    changed_by: Optional[str]
