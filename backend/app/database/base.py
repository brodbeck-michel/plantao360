from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.config import get_settings


_engine = None
_SessionLocal = None


def _get_engine():
    global _engine
    if _engine is None:
        settings = get_settings()
        connect_args = {}
        if settings.DATABASE_URL.startswith("sqlite"):
            connect_args["check_same_thread"] = False
        _engine = create_engine(
            settings.DATABASE_URL,
            connect_args=connect_args,
            pool_pre_ping=True,
        )
    return _engine


def _get_session_local():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_get_engine())
    return _SessionLocal


class Base(DeclarativeBase):
    pass


class _EngineProxy:
    def __getattr__(self, name):
        return getattr(_get_engine(), name)


class _SessionLocalProxy:
    def __call__(self, *args, **kwargs):
        return _get_session_local()(*args, **kwargs)


engine = _EngineProxy()
SessionLocal = _SessionLocalProxy()
