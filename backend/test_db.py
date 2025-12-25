from sqlalchemy import text
from app.database import engine

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT NOW()"))
        print("Database connection successful:", result.fetchone())
except Exception as e:
    print("Database connection failed:", e)
