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
from app.api.routes.period import router as period_router
from app.api.exception_handlers import register_exception_handlers


@pytest.fixture
def client(auth_override):
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    connection = engine.connect()
    Base.metadata.create_all(bind=connection)
    TestSession = sessionmaker(bind=connection)

    test_app = FastAPI()
    register_exception_handlers(test_app)
    test_app.include_router(period_router, prefix="/api/v1")

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


def test_list_periods(client):
    response = client.get("/api/v1/periods/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "items" in data["data"]
    assert "X-Total-Count" in response.headers


def test_create_period(client):
    response = client.post(
        "/api/v1/periods/",
        json={"year": 2026, "month": 6},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["year"] == 2026
    assert data["data"]["month"] == 6
    assert data["data"]["status"] == "draft"


def test_get_period(client):
    create_resp = client.post(
        "/api/v1/periods/",
        json={"year": 2026, "month": 6},
    )
    period_id = create_resp.json()["data"]["id"]
    response = client.get(f"/api/v1/periods/{period_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["year"] == 2026


def test_get_period_not_found(client):
    response = client.get("/api/v1/periods/999")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "PERIOD_NOT_FOUND"


def test_update_period(client):
    create_resp = client.post(
        "/api/v1/periods/",
        json={"year": 2026, "month": 6},
    )
    period_id = create_resp.json()["data"]["id"]
    response = client.patch(
        f"/api/v1/periods/{period_id}",
        json={"month": 7},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["month"] == 7


def test_close_period(client):
    create_resp = client.post(
        "/api/v1/periods/",
        json={"year": 2026, "month": 6},
    )
    period_id = create_resp.json()["data"]["id"]
    response = client.post(f"/api/v1/periods/{period_id}/close")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["status"] == "closed"


def test_reopen_period(client):
    create_resp = client.post(
        "/api/v1/periods/",
        json={"year": 2026, "month": 6},
    )
    period_id = create_resp.json()["data"]["id"]
    client.post(f"/api/v1/periods/{period_id}/close")
    response = client.post(f"/api/v1/periods/{period_id}/reopen")
    assert response.status_code == 200
    data = response.json()
    assert data["data"]["status"] == "draft"


def test_create_duplicate_period(client):
    client.post(
        "/api/v1/periods/",
        json={"year": 2026, "month": 6},
    )
    response = client.post(
        "/api/v1/periods/",
        json={"year": 2026, "month": 6},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "PERIOD_ALREADY_EXISTS"


def test_close_already_closed(client):
    create_resp = client.post(
        "/api/v1/periods/",
        json={"year": 2026, "month": 6},
    )
    period_id = create_resp.json()["data"]["id"]
    client.post(f"/api/v1/periods/{period_id}/close")
    response = client.post(f"/api/v1/periods/{period_id}/close")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is False
    assert data["error"]["code"] == "PERIOD_ALREADY_CLOSED"
