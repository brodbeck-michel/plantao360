from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.base import SessionLocal


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
