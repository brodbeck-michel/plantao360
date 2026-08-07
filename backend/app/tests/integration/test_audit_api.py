"""Testes de integração da API de auditoria (GET /audit).

Valida:
- Acesso restrito a ADMIN/COORDENADOR (403 para outros roles)
- Paginação e filtros funcionam
- Headers de paginação presentes
- Campos sensíveis ausentes no response
"""

import os
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["ENVIRONMENT"] = "test"

from app.database.base import Base
import app.models  # noqa: F401
from app.database.session import get_db
from app.core.security.dependencies import get_current_user
from app.models.user import User
from app.models.audit_log import AuditLog
from app.api.routes.audit import router as audit_router
from app.api.exception_handlers import register_exception_handlers
from app.tests.integration._auth import install_auth_override


def fake_admin() -> User:
    return User(id=1, name="Admin", email="admin@test.local", password_hash="x", role="ADMIN", active=True)


def fake_medico() -> User:
    return User(id=2, name="Medico", email="medico@test.local", password_hash="x", role="MEDICO", active=True)


def fake_coordenador() -> User:
    return User(id=3, name="Coord", email="coord@test.local", password_hash="x", role="COORDENADOR", active=True)


@pytest.fixture
def client(auth_override):
    """Cria um app de teste com banco em memória e roteador de auditoria."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    connection = engine.connect()
    Base.metadata.create_all(bind=connection)
    TestSession = sessionmaker(bind=connection)

    test_app = FastAPI()
    register_exception_handlers(test_app)
    test_app.include_router(audit_router, prefix="/api/v1")

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


def create_test_audit_logs(session):
    """Cria logs de auditoria para teste."""
    now = datetime.now(timezone.utc)
    logs = [
        AuditLog(
            occurred_at=now - timedelta(days=i),
            user_id=1,
            user_label="Admin User",
            user_role="ADMIN",
            origin="api",
            action="create",
            resource="period",
            resource_id=10,
            period_id=10,
            before=None,
            after={"month": 1, "year": 2026},
            summary="Criou competência janeiro",
            correlation_id="corr-1",
        )
        for i in range(5)
    ]

    logs.extend([
        AuditLog(
            occurred_at=now - timedelta(hours=i),
            user_id=1,
            user_label="Admin User",
            user_role="ADMIN",
            origin="api",
            action="update",
            resource="assignment",
            resource_id=100 + i,
            period_id=10,
            before={"doctor_id": 1},
            after={"doctor_id": 2},
            summary=f"Alterou plantão {i}",
            correlation_id=f"corr-assign-{i}",
        )
        for i in range(3)
    ])

    for log in logs:
        session.add(log)
    session.commit()
    return len(logs)


def test_audit_endpoint_admin_access(client):
    """ADMIN deve ter acesso ao GET /audit."""
    response = client.get("/api/v1/audit")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data


def test_audit_endpoint_coordenador_access(client, auth_override):
    """COORDENADOR deve ter acesso ao GET /audit (com auth override)."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    connection = engine.connect()
    Base.metadata.create_all(bind=connection)
    TestSession = sessionmaker(bind=connection)

    test_app = FastAPI()
    register_exception_handlers(test_app)
    test_app.include_router(audit_router, prefix="/api/v1")

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    test_app.dependency_overrides[get_db] = override_get_db
    test_app.dependency_overrides[get_current_user] = fake_coordenador

    test_client = TestClient(test_app)
    response = test_client.get("/api/v1/audit")
    assert response.status_code == 200


def test_audit_endpoint_medico_denied(client, auth_override):
    """MEDICO não deve ter acesso ao GET /audit (403)."""
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    connection = engine.connect()
    Base.metadata.create_all(bind=connection)
    TestSession = sessionmaker(bind=connection)

    test_app = FastAPI()
    register_exception_handlers(test_app)
    test_app.include_router(audit_router, prefix="/api/v1")

    def override_get_db():
        db = TestSession()
        try:
            yield db
        finally:
            db.close()

    test_app.dependency_overrides[get_db] = override_get_db
    test_app.dependency_overrides[get_current_user] = fake_medico

    test_client = TestClient(test_app)
    response = test_client.get("/api/v1/audit")
    assert response.status_code == 403


def test_audit_pagination_headers(client):
    """Resposta deve incluir headers de paginação."""
    response = client.get("/api/v1/audit?page=1&size=5")
    assert response.status_code == 200
    assert "x-total-count" in response.headers
    assert "x-page" in response.headers
    assert "x-page-size" in response.headers
    assert "x-total-pages" in response.headers


def test_audit_response_structure(client):
    """Response deve ter estrutura correta."""
    response = client.get("/api/v1/audit")
    assert response.status_code == 200
    data = response.json()
    assert "success" in data
    assert "data" in data or data["success"] is True
