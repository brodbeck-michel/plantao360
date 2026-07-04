"""Infrastructure test: empty DB → alembic → seed → API → health → readiness.

This test validates the complete bootstrap flow from an empty database to a
fully functional API. It is part of the Quality Gates for Sprint 14.3 ETAPA 2.

The test uses a temporary SQLite file (not in-memory) to simulate real
Alembic migration behavior, which requires a file-based database.

IMPORTANT: Because the SQLAlchemy engine is a global singleton, all tests
in this module share a single database and app instance via module-level
fixtures. The individual assertions validate each step of the pipeline.
"""
import os
import subprocess
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


# ── Shared infrastructure (module-level) ───────────────────────

_backend_dir = Path(__file__).resolve().parent.parent.parent.parent


@pytest.fixture(scope="module")
def bootstrap_env(tmp_path_factory):
    """Run the full pipeline: alembic → seed, once for the module."""
    tmp = tmp_path_factory.mktemp("bootstrap")
    db_path = tmp / "test_bootstrap.db"
    db_url = f"sqlite:///{db_path}"

    env = os.environ.copy()
    env["DATABASE_URL"] = db_url
    env["ENVIRONMENT"] = "test"
    env["SECRET_KEY"] = "test-secret-key-for-infrastructure-test"

    # Step 1: alembic upgrade head
    alembic_result = subprocess.run(
        [sys.executable, "-m", "alembic", "upgrade", "head"],
        cwd=str(_backend_dir),
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert alembic_result.returncode == 0, (
        f"alembic upgrade head failed:\n"
        f"STDOUT: {alembic_result.stdout}\n"
        f"STDERR: {alembic_result.stderr}"
    )

    # Step 2: seed demo data
    seed_result = subprocess.run(
        [sys.executable, "-m", "app.seed.seed_data", "--dataset", "demo"],
        cwd=str(_backend_dir),
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert seed_result.returncode == 0, (
        f"seed demo failed:\n"
        f"STDOUT: {seed_result.stdout}\n"
        f"STDERR: {seed_result.stderr}"
    )

    # Set env vars for the app (engine singleton reads these once)
    # IMPORTANT: Clear the settings cache so get_settings() picks up the new env vars
    os.environ["DATABASE_URL"] = db_url
    os.environ["ENVIRONMENT"] = "test"
    os.environ["SECRET_KEY"] = env["SECRET_KEY"]

    from app.core.settings.factory import get_settings
    get_settings.cache_clear()

    yield {"db_path": db_path, "db_url": db_url}


@pytest.fixture(scope="module")
def client(bootstrap_env):
    """Create a TestClient against the bootstrapped database."""
    # Point the app at the bootstrapped database (not test.db)
    os.environ["DATABASE_URL"] = bootstrap_env["db_url"]
    os.environ["ENVIRONMENT"] = "test"

    from app.core.settings.factory import get_settings
    get_settings.cache_clear()

    # Reset the engine singleton so it reconnects to the correct DB
    import app.database.base as base_mod
    base_mod._engine = None
    base_mod._SessionLocal = None

    from app.api.app import create_app
    app = create_app()
    with TestClient(app) as c:
        yield c


# ── Tests ──────────────────────────────────────────────────────

class TestBootstrapPipeline:
    """Validate each stage of the bootstrap pipeline."""

    def test_01_alembic_creates_schema(self, bootstrap_env):
        """Schema was created by alembic (verified by fixture assertion)."""
        assert bootstrap_env["db_path"].exists()

    def test_02_seed_populates_data(self, bootstrap_env):
        """Demo data was seeded (verified by fixture assertion)."""
        import sqlite3
        conn = sqlite3.connect(str(bootstrap_env["db_path"]))
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM doctors")
        count = cur.fetchone()[0]
        conn.close()
        assert count > 0, "No doctors found after seed"

    def test_03_health_ok(self, client):
        """Health endpoint returns ok with connected database."""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["database"] == "connected"
        assert "version" in data
        assert "environment" in data
        assert "timestamp" in data

    def test_04_readiness_all_true(self, client):
        """Readiness endpoint returns ready with all checks true."""
        response = client.get("/api/v1/readiness")
        assert response.status_code == 200
        data = response.json()
        assert data["ready"] is True
        assert data["checks"]["database"] is True
        assert data["checks"]["settings"] is True
        assert data["checks"]["storage"] is True
        assert data["checks"]["migrations"] is True

    def test_05_api_endpoints_respond(self, client):
        """Core API endpoints respond (not 500)."""
        for endpoint in ["/api/v1/doctors", "/api/v1/periods"]:
            response = client.get(endpoint)
            assert response.status_code in (200, 422), (
                f"{endpoint} returned {response.status_code}"
            )
