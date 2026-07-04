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
