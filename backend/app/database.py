import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", "local")

# --------------------------------------------------
# Database Engine
# --------------------------------------------------
if ENV == "production":
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise RuntimeError("DATABASE_URL not set")

    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=5,          # ✅ REQUIRED
        max_overflow=10,      # ✅ REQUIRED
        pool_timeout=30,      # ✅ REQUIRED
    )

else:
    DATABASE_URL = "sqlite:///./tasks.db"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

# --------------------------------------------------
# Base + Session
# --------------------------------------------------
Base = declarative_base()

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# --------------------------------------------------
# Dependency
# --------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
