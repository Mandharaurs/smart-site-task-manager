# Smart Site Task Manager

A full-stack task management application that automatically classifies
and prioritizes tasks based on content analysis.

---

## 1. Project Overview

Smart Site Task Manager allows users to create tasks while the system
automatically determines:
- Task category
- Task priority
- Suggested actions
- Extracted entities


## 2. Features

- Create, update, delete, and view tasks
- Automatic task classification
- Priority detection
- Task history tracking
- REST API with Swagger docs
- Flutter-based dashboard UI
- Backend unit tests
- Production-ready structure



## 3. Tech Stack

### Backend
- FastAPI
- PostgreSQL (Supabase)
- SQLAlchemy
- Pydantic
- Pytest

### Frontend
- Flutter
- Material UI



## 4. Project Structure

smart-site-task-manager/
├── backend/
│ ├── app/
│ ├── tests/
│ ├── requirements.txt
│ └── main.py
├── frontend/
│ └── lib/
└── README.md



## 5. Backend Setup

### Step 1: Create virtual environment
cd backend
python -m venv venv
venv\Scripts\activate

Step 2: Install dependencies
pip install -r requirements.txt

Step 3: Environment variables 
Create a .env file inside the backend/ directory:
DATABASE_URL=postgresql://postgres:<PASSWORD>@<HOST>:5432/postgres
⚠️ Environment variables are required. Secrets are not committed.

Step 4: Run backend server
uvicorn app.main:app --reload
Open Swagger UI:
👉 http://127.0.0.1:8000/docs


## 6. API Endpoints
Method	Endpoint	Description
POST	/api/tasks	Create task
GET	/api/tasks	List tasks
GET	/api/tasks/{id}	Get task
PUT	/api/tasks/{id}	Update task
DELETE	/api/tasks/{id}	Delete task


## 7. Classification Logic
Category Rules
scheduling → meeting, schedule, call
finance → invoice, payment
technical → bug, error, fix
safety → hazard, inspection
general → default

Priority Rules
high → urgent, today, emergency
medium → important, soon
low → default


## 8. Testing
Run backend tests:
pytest


## 9. Frontend Setup (Flutter)
cd frontend
flutter pub get
flutter run

## 10. Future Improvements
AI/LLM-based task classification
Authentication and role management
Real-time updates
Mobile notifications












