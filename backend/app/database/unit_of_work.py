from typing import Generator

from sqlalchemy.orm import Session

from app.database.base import SessionLocal


class UnitOfWork:
    def __init__(self):
        self._session: Session | None = None

    def __enter__(self) -> "UnitOfWork":
        self._session = SessionLocal()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            self.rollback()
        else:
            self.commit()
        self.close()

    @property
    def session(self) -> Session:
        if self._session is None:
            raise RuntimeError("UnitOfWork not initialized")
        return self._session

    def commit(self) -> None:
        if self._session:
            self._session.commit()

    def rollback(self) -> None:
        if self._session:
            self._session.rollback()

    def close(self) -> None:
        if self._session:
            self._session.close()
            self._session = None
