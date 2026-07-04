from fastapi.testclient import TestClient

from app.api.app import create_app


def test_readiness_returns_all_checks():
    app = create_app()
    client = TestClient(app)
    response = client.get("/api/v1/readiness")
    assert response.status_code == 200
    data = response.json()
    assert "ready" in data
    assert "checks" in data
    assert data["checks"]["database"] is True
    assert data["checks"]["settings"] is True
    assert data["checks"]["storage"] is True
    assert data["checks"]["migrations"] is True


def test_readiness_has_timestamp():
    app = create_app()
    client = TestClient(app)
    response = client.get("/api/v1/readiness")
    data = response.json()
    assert "timestamp" in data


def test_readiness_ready_when_all_true():
    app = create_app()
    client = TestClient(app)
    response = client.get("/api/v1/readiness")
    data = response.json()
    all_checks_true = all(data["checks"].values())
    assert data["ready"] == all_checks_true
