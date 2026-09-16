from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create SQLAlchemy database engine
engine = create_engine(
    settings.sqlalchemy_database_uri,
    pool_pre_ping=True,  # Check connection health before using
)

# Session Local class for creating connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base model class
Base = declarative_base()

def get_db():
    """FastAPI Dependency for database session lifecycle management."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import contextvars
import uuid
from typing import Optional

# Context variables for request-scoped database sessions and user metadata
db_session_ctx: contextvars.ContextVar[Optional[SessionLocal]] = contextvars.ContextVar("db_session_ctx", default=None)
user_id_ctx: contextvars.ContextVar[Optional[uuid.UUID]] = contextvars.ContextVar("user_id_ctx", default=None)
session_id_ctx: contextvars.ContextVar[Optional[uuid.UUID]] = contextvars.ContextVar("session_id_ctx", default=None)
