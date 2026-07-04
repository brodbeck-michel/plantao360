"""FastAPI lifespan handler for Plantão 360.

This module provides the lifespan context manager that runs at application
startup and shutdown. It delegates all initialization logic to the RuntimeManager.

Usage in app.py:
    from app.core.lifespan import create_lifespan
    app = FastAPI(lifespan=create_lifespan())
"""
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.core.runtime import RuntimeManager, RuntimeMode, create_runtime

logger = logging.getLogger(__name__)


@asynccontextmanager
async def app_lifespan(runtime: RuntimeManager) -> AsyncGenerator[None, None]:
    """Application lifespan handler.

    On startup:
        - TEST mode: skip (tests use create_all in fixtures)
        - DEMO/DEVELOPMENT/PRODUCTION: run migrations
        - DEMO mode: seed demo data after migrations

    On shutdown:
        - Log the shutdown event
    """
    # ── Startup ──────────────────────────────────────────────
    logger.info("Lifespan: starting in %s mode", runtime.mode.value)

    if runtime.mode == RuntimeMode.TEST:
        logger.info("Lifespan: test mode — no startup actions (fixtures handle DB)")
    else:
        # Run migrations
        success = runtime.run_migrations()
        if not success:
            logger.error("Lifespan: migrations failed — application may not work correctly")

        # Seed only in DEMO mode
        success = runtime.seed_data(dataset="demo", clear=True)
        if not success:
            logger.error("Lifespan: seed failed — application started without demo data")

    info = runtime.get_startup_info()
    logger.info("Lifespan: startup complete — %s", info)

    # ── Yield to application ─────────────────────────────────
    yield

    # ── Shutdown ─────────────────────────────────────────────
    logger.info("Lifespan: shutting down")


def create_lifespan(environment: str | None = None):
    """Factory that creates a lifespan handler bound to the current environment.

    The RuntimeManager is created lazily on first startup, not at import time.
    This avoids triggering settings/engine initialization during module imports.

    Usage:
        app = FastAPI(lifespan=create_lifespan())
    """
    _runtime: RuntimeManager | None = None

    def _get_runtime() -> RuntimeManager:
        nonlocal _runtime
        if _runtime is None:
            _runtime = create_runtime(environment=environment)
        return _runtime

    @asynccontextmanager
    async def lifespan(app):
        runtime = _get_runtime()
        async with app_lifespan(runtime):
            yield

    return lifespan
