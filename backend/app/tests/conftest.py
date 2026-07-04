import os

os.environ["ENVIRONMENT"] = "test"

# Clear settings cache so get_settings() picks up the test environment
from app.core.settings.factory import get_settings
get_settings.cache_clear()

import pytest


@pytest.fixture
def engine():
    from sqlalchemy import create_engine
    from app.database.base import Base

    eng = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)
    eng.dispose()


@pytest.fixture
def db_session(engine):
    from sqlalchemy.orm import sessionmaker
    from app.database.unit_of_work import UnitOfWork

    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def uow(engine):
    from sqlalchemy.orm import sessionmaker
    from app.database.unit_of_work import UnitOfWork

    Session = sessionmaker(bind=engine)
    _uow = UnitOfWork()
    _uow._session = Session()
    yield _uow
    try:
        _uow.rollback()
    except Exception:
        pass
    _uow.close()
