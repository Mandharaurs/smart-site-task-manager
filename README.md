# Smart Site Task Manager

A backend-driven task management system that automatically classifies,
prioritizes, and organizes tasks using intelligent keyword-based analysis.
Built as part of the Backend + Flutter Hybrid Developer Assessment.

---

## Project Overview

This project is a Smart Task Manager that:
- Automatically classifies tasks by category
- Assigns priority based on urgency
- Extracts entities such as people, dates, and actions
- Suggests next actions based on task type
- Stores tasks and audit history in PostgreSQL (Supabase)

---

## Tech Stack

### Backend
- FastAPI (Python)
- SQLAlchemy
- PostgreSQL (Supabase)
- Pydantic
- Pytest

### Deployment
- Render (Backend API)

---

## Features Implemented

- Create, update, delete tasks
- Automatic classification on task creation
- Task history (audit logs)
- Filtering, sorting, pagination
- Task summary analytics
- Full-text search
- API documentation via Swagger
- Unit tests and API tests

---

## API Endpoints

### Create Task
```http
POST /api/tasks
