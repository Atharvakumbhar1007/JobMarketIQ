"""Database connection and session management using SQLAlchemy + SQLite."""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# Database URL
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
_DEFAULT_DB_URL = f"sqlite:///{PROJECT_ROOT / 'jobmarketiq.db'}"
DATABASE_URL = os.getenv("DATABASE_URL", _DEFAULT_DB_URL)

# ============================================================
# Engine & Session factory
# ============================================================

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# ============================================================
# Base class for ORM models
# ============================================================

class Base(DeclarativeBase):
    pass


# ============================================================
# Helpers
# ============================================================

def get_engine():
    return engine


def get_session():
    """Context-managed database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def create_all_tables():
    """Create all tables defined in models."""
    from src.database import models  # noqa: F401 — registers models
    Base.metadata.create_all(bind=engine)
    print("All tables created.")
