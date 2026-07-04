"""Runtime Manager — centralized startup logic for Plantão 360.

This module is the single source of truth for how the application initializes
based on its runtime mode. It replaces all scattered create_all() calls,
seed invocations, and environment-based conditionals.

Runtime Modes:
    - DEMO:       alembic upgrade head → seed demo → ready
    - DEVELOPMENT: alembic upgrade head → ready (seed optional via CLI)
    - PRODUCTION:  alembic upgrade head → ready (seed manual, never auto)
    - TEST:        create_all() in-memory → ready (no migrations, no seed)

Architecture Rule:
    The Runtime decides what happens at startup.
    Alembic owns the schema. Seed owns the data. The Runtime orchestrates both.
"""
import logging
import subprocess
import sys
from enum import StrEnum
from pathlib import Path
from typing import Optional

from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


class RuntimeMode(StrEnum):
    """Supported runtime modes.

    Each mode defines a distinct initialization flow:
        - TEST:        create_all() in-memory, no migrations, no seed
        - DEMO:        alembic → seed demo → API
        - DEVELOPMENT: alembic → API (seed manual)
        - PRODUCTION:  alembic → API (no seed, no reload)
    """
    TEST = "test"
    DEMO = "demo"
    DEVELOPMENT = "development"
    PRODUCTION = "production"


def detect_mode(environment: str) -> RuntimeMode:
    """Map an ENVIRONMENT string to a RuntimeMode.

    Rules:
        - ENVIRONMENT=test → TEST
        - ENVIRONMENT=production → PRODUCTION
        - ENVIRONMENT=development + DEMO_MODE=true → DEMO
        - ENVIRONMENT=development + DEMO_MODE=false → DEVELOPMENT
        - anything else → DEVELOPMENT
    """
    env = environment.lower().strip()

    if env == "test":
        return RuntimeMode.TEST

    if env == "production":
        return RuntimeMode.PRODUCTION

    if env == "development":
        from app.core.config import get_settings
        settings = get_settings()
        if getattr(settings, "DEMO_MODE", False):
            return RuntimeMode.DEMO
        return RuntimeMode.DEVELOPMENT

    return RuntimeMode.DEVELOPMENT


class RuntimeManager:
    """Centralized startup orchestrator.

    Responsible for:
        1. Running database migrations (or create_all for test mode)
        2. Seeding data (only in DEMO mode)
        3. Validating the database is ready

    NOT responsible for:
        - Business logic
        - Data generation (that's seed's job)
        - Schema definition (that's Alembic's job)
    """

    def __init__(self, mode: RuntimeMode, backend_dir: Optional[Path] = None):
        self.mode = mode
        self.backend_dir = backend_dir or self._detect_backend_dir()
        self._seed_module = "app.seed.seed_data"

    @staticmethod
    def _detect_backend_dir() -> Path:
        """Find the backend directory relative to this file."""
        return Path(__file__).resolve().parent.parent.parent

    def _run_command(self, cmd: list[str], description: str) -> subprocess.CompletedProcess:
        """Run a shell command and return the result."""
        logger.info("RuntimeManager: %s", description)
        logger.debug("RuntimeManager: command=%s", " ".join(cmd))

        result = subprocess.run(
            cmd,
            cwd=str(self.backend_dir),
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            logger.error(
                "RuntimeManager: %s failed (exit %d)\nSTDOUT: %s\nSTDERR: %s",
                description,
                result.returncode,
                result.stdout,
                result.stderr,
            )
        else:
            logger.info("RuntimeManager: %s succeeded", description)

        return result

    def run_migrations(self) -> bool:
        """Run alembic upgrade head. Returns True on success."""
        if self.mode == RuntimeMode.TEST:
            logger.info("RuntimeManager: test mode — skipping alembic (using create_all)")
            return True

        result = self._run_command(
            [sys.executable, "-m", "alembic", "upgrade", "head"],
            description="Running database migrations",
        )
        return result.returncode == 0

    def seed_data(self, dataset: str = "demo", clear: bool = False) -> bool:
        """Seed the database. Returns True on success.

        Only runs in DEMO mode. In other modes, this is a no-op.
        """
        if self.mode != RuntimeMode.DEMO:
            logger.info(
                "RuntimeManager: mode=%s — seed skipped (only runs in DEMO mode)",
                self.mode.value,
            )
            return True

        cmd = [sys.executable, "-m", self._seed_module, "--dataset", dataset]
        if clear:
            cmd.append("--clear")

        result = self._run_command(cmd, description=f"Seeding {dataset} dataset")
        return result.returncode == 0

    def initialize_database(self, engine: Optional[Engine] = None) -> bool:
        """Full database initialization: migrations + seed.

        Returns True if the database is ready to serve requests.
        """
        logger.info("RuntimeManager: initializing in %s mode", self.mode.value)

        # Step 1: Schema
        if not self.run_migrations():
            logger.error("RuntimeManager: migrations failed — aborting startup")
            return False

        # Step 2: Seed (only in DEMO mode)
        if not self.seed_data(dataset="demo", clear=True):
            logger.error("RuntimeManager: seed failed — aborting startup")
            return False

        logger.info("RuntimeManager: database initialization complete")
        return True

    def get_startup_info(self) -> dict:
        """Return a summary of the current runtime configuration."""
        return {
            "mode": self.mode.value,
            "migrations": "alembic" if self.mode != RuntimeMode.TEST else "create_all",
            "seed": "auto (demo)" if self.mode == RuntimeMode.DEMO else "manual",
            "database": "managed" if self.mode == RuntimeMode.PRODUCTION else "local",
        }


def create_runtime(environment: Optional[str] = None) -> RuntimeManager:
    """Factory function to create a RuntimeManager from the current environment.

    Usage:
        runtime = create_runtime()
        runtime.initialize_database()
    """
    import os
    from app.core.config import get_settings

    if environment is None:
        settings = get_settings()
        environment = settings.ENVIRONMENT

    mode = detect_mode(environment)
    return RuntimeManager(mode=mode)
