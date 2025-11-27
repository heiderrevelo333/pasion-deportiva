# app/dependencies/database.py
from app.core.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Generator

def get_db() -> Generator[Session, None, None]:
    """
    Creates a new SQLAlchemy session for a request and closes it afterwards.
    """
    db = SessionLocal()
    try:
        # The 'yield' statement is what makes this a dependency generator
        yield db 
    finally:
        db.close()