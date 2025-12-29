from fastapi import FastAPI, Depends, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from uuid import UUID

from app.database import get_db
from app.models import Task, TaskHistory
from app.classification import classify_task

# --------------------------------------------------
# FastAPI app
# --------------------------------------------------
app = FastAPI(
    title="Smart Site Task Manager",
    version="1.0.0",
    description="Backend API for smart task classification and management"
)

# --------------------------------------------------
# CORS (Required for Flutter / Frontend)
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Schemas
# --------------------------------------------------
class TaskText(BaseModel):
    text: str

class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskUpdate(BaseModel):
    description: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskResponse(BaseModel):
    id: UUID   
    title: str
    description: str
    category: Optional[str]
    priority: Optional[str]
    status: str
    assigned_to: Optional[str]
    due_date: Optional[datetime]
    extracted_entities: dict
    suggested_actions: list
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

# --------------------------------------------------
# Constants
# --------------------------------------------------
ALLOWED_STATUS = {"pending", "in_progress", "completed"}
ALLOWED_PRIORITY = {"high", "medium", "low"}

# --------------------------------------------------
# Health Endpoints
# --------------------------------------------------
@app.get("/", tags=["Health"])
def root():
    return {"message": "Smart Site Task Manager API"}

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}

# --------------------------------------------------
# Classification (No DB save)
# --------------------------------------------------
@app.post("/classify", tags=["Classification"])
def classify_only(task: TaskText):
    return {
        "analysis": classify_task(task.text)
    }

# --------------------------------------------------
# Create Task
# --------------------------------------------------
@app.post("/api/tasks", response_model=TaskResponse, tags=["Tasks"])
def create_task(task: TaskCreate, db: Session = Depends(get_db)):
    classification = classify_task(f"{task.title} {task.description}")

    db_task = Task(
        title=task.title,
        description=task.description,
        category=classification["category"],
        priority=classification["priority"],
        status="pending",
        assigned_to=task.assigned_to,
        due_date=task.due_date,
        extracted_entities=classification["extracted_entities"],
        suggested_actions=classification["suggested_actions"]
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    history = TaskHistory(
        task_id=db_task.id,
        action="created",
        old_value=None,
        new_value=classification,
        changed_by="system"
    )

    db.add(history)
    db.commit()

    return db_task

# --------------------------------------------------
# Get Tasks (Filter + Pagination)
# --------------------------------------------------
@app.get("/api/tasks", response_model=List[TaskResponse], tags=["Tasks"])
def get_tasks(
    category: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=50),
    offset: int = Query(0, ge=0),
    sort_by: str = Query("created_at"),
    order: str = Query("desc"),
    db: Session = Depends(get_db)
):
    query = db.query(Task)

    if category:
        query = query.filter(Task.category == category)
    if priority:
        query = query.filter(Task.priority == priority)
    if status:
        query = query.filter(Task.status == status)

    column = getattr(Task, sort_by, Task.created_at)
    query = query.order_by(column.desc() if order == "desc" else column.asc())

    return query.offset(offset).limit(limit).all()

# --------------------------------------------------
# Task Summary
# --------------------------------------------------
@app.get("/api/tasks/summary", tags=["Tasks"])
def task_summary(db: Session = Depends(get_db)):
    pending = db.query(Task).filter(Task.status == "pending").count()
    in_progress = db.query(Task).filter(Task.status == "in_progress").count()
    completed = db.query(Task).filter(Task.status == "completed").count()
    
    return {
        "pending": pending,
        "in_progress": in_progress,
        "completed": completed,
    }

# --------------------------------------------------
# Search Tasks
# --------------------------------------------------
@app.get("/api/tasks/search", response_model=List[TaskResponse], tags=["Tasks"])
def search_tasks(
    q: str = Query(..., min_length=2),
    db: Session = Depends(get_db)
):
    return (
        db.query(Task)
        .filter(
            (Task.title.ilike(f"%{q}%")) |
            (Task.description.ilike(f"%{q}%"))
        )
        .all()
    )

# --------------------------------------------------
# Get Task by ID
# --------------------------------------------------
@app.get("/api/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def get_task(task_id: UUID, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# --------------------------------------------------
# Update Task
# --------------------------------------------------
@app.patch("/api/tasks/{task_id}", response_model=TaskResponse, tags=["Tasks"])
def update_task(task_id: UUID, data: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Validation
    if data.status and data.status not in ALLOWED_STATUS:
        raise HTTPException(status_code=400, detail="Invalid status")

    # Prepare update data
    update_data = data.model_dump(exclude_unset=True)

    # Block manual override of NLP fields
    if "category" in update_data or "priority" in update_data:
        raise HTTPException(
            status_code=400,
            detail="Category and priority are auto-generated"
        )

    # Snapshot before update
    old_value = {
        "title": task.title,
        "description": task.description,
        "category": task.category,
        "priority": task.priority,
        "status": task.status,
        "assigned_to": task.assigned_to,
        "due_date": str(task.due_date) if task.due_date else None
    }

    # Apply updates
    for field, value in update_data.items():
        setattr(task, field, value)

    # NLP RE-CLASSIFICATION (ONLY IF DESCRIPTION CHANGED)
    if "description" in update_data:
        classification = classify_task(f"{task.title} {task.description}")

        task.category = classification["category"]
        task.priority = classification["priority"]
        task.extracted_entities = classification["extracted_entities"]
        task.suggested_actions = classification["suggested_actions"]

    # Save
    db.commit()
    db.refresh(task)

    # History
    history = TaskHistory(
        task_id=task.id,
        action="updated",
        old_value=old_value,
        new_value=update_data,
        changed_by="system"
    )

    db.add(history)
    db.commit()

    return task

# --------------------------------------------------
# Delete Task
# --------------------------------------------------
@app.delete("/api/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: UUID, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    history = TaskHistory(
        task_id=task.id,
        action="deleted",
        old_value={
            "text": f"{task.title} {task.description}",
            "category": task.category,
            "priority": task.priority,
            "status": task.status
        },
        new_value=None,
        changed_by="system"
    )

    db.add(history)
    db.commit()

    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully"}

# --------------------------------------------------
# Task History
# --------------------------------------------------
@app.get("/api/tasks/{task_id}/history", tags=["Tasks"])
def get_task_history(task_id: UUID, db: Session = Depends(get_db)):
    history = (
        db.query(TaskHistory)
        .filter(TaskHistory.task_id == task_id)
        .order_by(TaskHistory.changed_at.desc())
        .all()
    )

    if not history:
        raise HTTPException(status_code=404, detail="No history found")

    return history
