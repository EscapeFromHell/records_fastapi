from typing import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from src.core.db.session import SessionLocal
from src.core.repository import RecordRepo, UserRepo


def get_db() -> Generator:
    """Генератор сессии БД."""
    with SessionLocal() as db:
        yield db


def record_repo(db: Session = Depends(get_db, use_cache=True)) -> RecordRepo:
    """DI для репозитория RecordRepo."""
    return RecordRepo(db)


def user_repo(db: Session = Depends(get_db, use_cache=True)) -> UserRepo:
    """DI для репозитория UserRepo."""
    return UserRepo(db)
