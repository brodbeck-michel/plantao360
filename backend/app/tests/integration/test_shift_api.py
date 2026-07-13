import os
import pytest
from datetime import date

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["ENVIRONMENT"] = "test"

from app.database.base import Base
import app.models  # noqa: F401
from app.database.session import get_db
from app.api.routes.shift import router as shift_router
from app.api.exception_handlers import register_exception_handlers
from app.models.period import Period
from app.models.shift import Shift
from app.domain.constants.shift_status import ShiftStatus


@pytest.fixture
def client(auth_override):
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    connection = engine.connect()
    Base.metadata.create_all(bind=connection)
    TestSession = sessionmaker(bind=connection)

    test_app = FastAPI()
    register_exception_handlers(test_app)
    test_app.include_router(shift_router, prefix="/api/v1")

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    test_app.dependency_overrides[get_db] = override_get_db
    auth_override(test_app)

    with TestClient(test_app) as c:
        yield c

    test_app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=connection)
    connection.close()
    engine.dispose()


def _seed_period(session):
    period = Period(year=2025, month=1)
    session.add(period)
    session.commit()
    session.refresh(period)
    return period


def test_list_shifts(client):
    response = client.get("/api/v1/shifts/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_create_shift(client):
    response = client.post(
        "/api/v1/shifts/",
        json={
            "period_id": 1,
            "shift_date": "2025-01-15",
            "shift_type": "T1",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True


def test_get_shift(client):
    create_resp = client.post(
        "/api/v1/shifts/",
        json={
            "period_id": 1,
            "shift_date": "2025-01-15",
            "shift_type": "T1",
        },
    )
    entity_id = create_resp.json()["data"]["id"]
    response = client.get(f"/api/v1/shifts/{entity_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_get_shift_not_found(client):
    response = client.get("/api/v1/shifts/999")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False


def test_update_shift(client):
    create_resp = client.post(
        "/api/v1/shifts/",
        json={
            "period_id": 1,
            "shift_date": "2025-01-15",
            "shift_type": "T1",
        },
    )
    entity_id = create_resp.json()["data"]["id"]
    response = client.put(
        f"/api/v1/shifts/{entity_id}",
        json={"shift_type": "T2"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_delete_shift(client):
    create_resp = client.post(
        "/api/v1/shifts/",
        json={
            "period_id": 1,
            "shift_date": "2025-01-15",
            "shift_type": "T1",
        },
    )
    entity_id = create_resp.json()["data"]["id"]
    response = client.delete(f"/api/v1/shifts/{entity_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
