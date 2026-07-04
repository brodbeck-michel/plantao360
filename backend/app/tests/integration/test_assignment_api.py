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
from app.api.routes.assignment import router as assignment_router
from app.api.exception_handlers import register_exception_handlers
from app.models.shift import Shift
from app.models.period import Period
from app.models.doctor import Doctor

_test_data = {}


@pytest.fixture
def client():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    connection = engine.connect()
    Base.metadata.create_all(bind=connection)
    TestSession = sessionmaker(bind=connection)

    session = TestSession()
    doctor = Doctor(name="Test Doctor", crm="12345/ES", hour_rate=150.0, specialty="Clinica Medica", active=True)
    session.add(doctor)
    doctor2 = Doctor(name="Second Doctor", crm="67890/ES", hour_rate=200.0, specialty="Cardiologia", active=True)
    session.add(doctor2)
    period = Period(year=2025, month=1)
    session.add(period)
    session.commit()
    session.refresh(doctor)
    session.refresh(doctor2)
    session.refresh(period)
    shift = Shift(period_id=period.id, shift_date=date(2025, 1, 15), shift_type="T1", status="scheduled")
    session.add(shift)
    session.commit()
    session.refresh(shift)
    _test_data["shift_id"] = shift.id
    _test_data["doctor_id"] = doctor.id
    _test_data["doctor2_id"] = doctor2.id
    session.close()

    test_app = FastAPI()
    register_exception_handlers(test_app)
    test_app.include_router(assignment_router, prefix="/api/v1")

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


def _payload(**overrides):
    data = {
        "shift_id": _test_data["shift_id"],
        "doctor_id": _test_data["doctor_id"],
        "start_time": "08:00",
        "end_time": "20:00",
    }
    data.update(overrides)
    return data


def test_list_assignments(client):
    response = client.get("/api/v1/assignments/")
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_create_assignment(client):
    response = client.post("/api/v1/assignments/", json=_payload())
    assert response.status_code in (200, 201)
    body = response.json()
    assert body["success"] is True
    assert body["data"]["shift_id"] == _test_data["shift_id"]
    assert body["data"]["doctor_id"] == _test_data["doctor_id"]


def test_get_assignment_not_found(client):
    response = client.get("/api/v1/assignments/999")
    assert response.status_code == 200
    assert response.json()["success"] is False


def test_confirm_assignment(client):
    create_resp = client.post("/api/v1/assignments/", json=_payload())
    assignment_id = create_resp.json()["data"]["id"]
    response = client.patch(f"/api/v1/assignments/{assignment_id}/confirm")
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_cancel_assignment(client):
    create_resp = client.post("/api/v1/assignments/", json=_payload())
    assignment_id = create_resp.json()["data"]["id"]
    response = client.patch(f"/api/v1/assignments/{assignment_id}/cancel")
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_remove_assignment(client):
    create_resp = client.post("/api/v1/assignments/", json=_payload())
    assignment_id = create_resp.json()["data"]["id"]
    response = client.delete(f"/api/v1/assignments/{assignment_id}")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] == "cancelled"


def test_swap_doctor(client):
    create_resp = client.post("/api/v1/assignments/", json=_payload())
    assignment_id = create_resp.json()["data"]["id"]
    response = client.put(f"/api/v1/assignments/{assignment_id}", json={"doctor_id": _test_data["doctor2_id"]})
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["doctor_id"] == _test_data["doctor2_id"]


def test_create_assignment_invalid_doctor(client):
    response = client.post("/api/v1/assignments/", json=_payload(doctor_id=99999))
    body = response.json()
    assert body["success"] is False

