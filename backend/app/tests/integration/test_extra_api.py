"""Integration tests for Extra API endpoints."""

import os
import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["ENVIRONMENT"] = "test"

from app.database.base import Base
import app.models  # noqa: F401
from app.database.session import get_db
from app.api.routes.extra import router as extra_router
from app.api.exception_handlers import register_exception_handlers
from app.models.shift_extra import ShiftExtra
from app.domain.constants.extra_status import ExtraStatus


@pytest.fixture
def client(auth_override):
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    connection = engine.connect()
    Base.metadata.create_all(bind=connection)
    TestSession = sessionmaker(bind=connection)

    test_app = FastAPI()
    register_exception_handlers(test_app)
    test_app.include_router(extra_router, prefix="/api/v1")

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


def _seed_extra(session):
    extra = ShiftExtra(
        shift_id=1,
        doctor_id=1,
        duration_minutes=60,
        justification="Cobertura de plantão",
        status=ExtraStatus.PENDING,
    )
    session.add(extra)
    session.commit()
    session.refresh(extra)
    return extra


def test_list_extras_empty(client):
    response = client.get("/api/v1/extras/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_create_extra(client):
    response = client.post(
        "/api/v1/extras/",
        json={
            "shift_id": 1,
            "doctor_id": 1,
            "duration_minutes": 60,
            "justification": "Cobertura de plantão",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True


def test_create_extra_invalid_duration(client):
    response = client.post(
        "/api/v1/extras/",
        json={
            "shift_id": 1,
            "doctor_id": 1,
            "duration_minutes": 0,
            "justification": "Teste",
        },
    )
    assert response.status_code == 422


def test_create_extra_empty_justification(client):
    response = client.post(
        "/api/v1/extras/",
        json={
            "shift_id": 1,
            "doctor_id": 1,
            "duration_minutes": 60,
            "justification": "",
        },
    )
    assert response.status_code == 422


def test_get_extra_not_found(client):
    response = client.get("/api/v1/extras/999")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "extra.not_found"


def test_approve_extra_not_found(client):
    response = client.patch("/api/v1/extras/999/approve")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False


def test_reject_extra_not_found(client):
    response = client.patch("/api/v1/extras/999/reject")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False


def test_cancel_extra_not_found(client):
    response = client.patch("/api/v1/extras/999/cancel")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False


def test_delete_extra_not_found(client):
    response = client.delete("/api/v1/extras/999")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False


def test_update_extra_not_found(client):
    response = client.put(
        "/api/v1/extras/999",
        json={"duration_minutes": 120},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
