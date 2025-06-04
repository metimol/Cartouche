"""
Database session management for the Cartouche Bot Service.
Sets up SQLAlchemy connection and session handling.
"""

import os
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.settings import DB_PATH

# Ensure database directory exists
db_path = Path(DB_PATH)
db_path.parent.mkdir(parents=True, exist_ok=True)

# Create SQLite database URL
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # Needed for SQLite
    pool_size=5,  # Number of connections to keep open in the pool
    max_overflow=10,  # Number of connections that can be opened beyond pool_size
)

# Create sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """
    Dependency for database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
