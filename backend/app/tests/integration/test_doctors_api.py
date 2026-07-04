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
from app.api.routes.doctors import router as doctors_router
from app.api.exception_handlers import register_exception_handlers


@pytest.fixture
def client():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    connection = engine.connect()
    Base.metadata.create_all(bind=connection)
    TestSession = sessionmaker(bind=connection)

    test_app = FastAPI()
    register_exception_handlers(test_app)
    test_app.include_router(doctors_router, prefix="/api/v1")

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    test_app.dependency_overrides[get_db] = override_get_db

    with TestClient(test_app) as c:
        yield c

    test_app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=connection)
    connection.close()
    engine.dispose()


def test_list_doctors(client):
    response = client.get("/api/v1/doctors/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "items" in data["data"]
    assert "X-Total-Count" in response.headers
    assert "X-Page" in response.headers
    assert "X-Page-Size" in response.headers
    assert "X-Total-Pages" in response.headers


def test_create_doctor(client):
    response = client.post(
        "/api/v1/doctors/",
        json={
            "name": "Dr. Teste API",
            "crm": "12345",
            "hour_rate": 150.0,
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["name"] == "Dr. Teste API"
    assert "error" not in data or data.get("error") is None


def test_get_doctor(client):
    create_resp = client.post(
        "/api/v1/doctors/",
        json={
            "name": "Dr. Find API",
            "crm": "54321",
            "hour_rate": 200.0,
        },
    )
    doctor_id = create_resp.json()["data"]["id"]
    response = client.get(f"/api/v1/doctors/{doctor_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["name"] == "Dr. Find API"


def test_get_doctor_not_found(client):
    response = client.get("/api/v1/doctors/999")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "DOCTOR_NOT_FOUND"


def test_update_doctor(client):
    create_resp = client.post(
        "/api/v1/doctors/",
        json={
            "name": "Dr. Update API",
            "crm": "11111",
            "hour_rate": 180.0,
        },
    )
    doctor_id = create_resp.json()["data"]["id"]
    response = client.put(
        f"/api/v1/doctors/{doctor_id}",
        json={"name": "Dr. Updated API"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["name"] == "Dr. Updated API"


def test_delete_doctor(client):
    create_resp = client.post(
        "/api/v1/doctors/",
        json={
            "name": "Dr. Delete API",
            "crm": "22222",
            "hour_rate": 190.0,
        },
    )
    doctor_id = create_resp.json()["data"]["id"]
    response = client.delete(f"/api/v1/doctors/{doctor_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


def test_create_doctor_duplicate_crm(client):
    client.post(
        "/api/v1/doctors/",
        json={"name": "Dr. First", "crm": "99999", "hour_rate": 150.0},
    )
    response = client.post(
        "/api/v1/doctors/",
        json={"name": "Dr. Second", "crm": "99999", "hour_rate": 200.0},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "DOCTOR_ALREADY_EXISTS"


def test_list_doctors_with_filters(client):
    client.post(
        "/api/v1/doctors/",
        json={"name": "Dr. Silva", "crm": "11111", "hour_rate": 150.0},
    )
    client.post(
        "/api/v1/doctors/",
        json={"name": "Dr. Santos", "crm": "22222", "hour_rate": 200.0},
    )
    response = client.get("/api/v1/doctors/?name=Silva")
    assert response.status_code == 200
    data = response.json()
    assert len(data["data"]["items"]) == 1
