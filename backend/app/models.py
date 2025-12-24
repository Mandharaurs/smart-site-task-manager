import uuid
from sqlalchemy import Column, String, DateTime, JSON, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)

    category = Column(String, nullable=True)
    priority = Column(String, nullable=True)
    status = Column(String, default="pending")

    assigned_to = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)

    extracted_entities = Column(JSON, nullable=True)
    suggested_actions = Column(JSON, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class TaskHistory(Base):
    __tablename__ = "task_history"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, ForeignKey("tasks.id", ondelete="CASCADE"))

    action = Column(String, nullable=False)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    changed_by = Column(String, nullable=True)

    changed_at = Column(DateTime(timezone=True), server_default=func.now())
