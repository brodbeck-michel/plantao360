from fastapi.testclient import TestClient

from app.api.app import create_app


def test_health_check():
    app = create_app()
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data
    assert "environment" in data
    assert "database" in data
    assert "timestamp" in data


def test_docs_available():
    app = create_app()
    client = TestClient(app)
    response = client.get("/api/v1/docs")
    assert response.status_code == 200


def test_readiness_check():
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


def test_openapi_json():
    app = create_app()
    client = TestClient(app)
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "paths" in data
