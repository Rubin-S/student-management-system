# backend/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database URL. For now, it's a local SQLite file.
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./sis.db")
# For PostgreSQL, it would look like this:
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
)

# Each instance of SessionLocal will be a database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models to inherit from
Base = declarative_base()

# --- Dependency for Database Session ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()