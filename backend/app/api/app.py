from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.lifespan import create_lifespan
from app.api.middlewares.correlation import CorrelationIDMiddleware
from app.api.middlewares.access_log import AccessLogMiddleware
from app.api.routes import health, readiness, doctors, period, shift, assignment, extra, coverage, payroll, dashboard, auth
from app.api.exception_handlers import register_exception_handlers


def create_app() -> FastAPI:
    settings = get_settings()
    setup_logging(settings.LOG_LEVEL)

    application = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        openapi_url="/api/v1/openapi.json",
        lifespan=create_lifespan(),
        redirect_slashes=False,
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.add_middleware(AccessLogMiddleware)
    application.add_middleware(CorrelationIDMiddleware)

    register_exception_handlers(application)

    application.include_router(health.router, prefix="/api/v1")
    application.include_router(readiness.router, prefix="/api/v1")
    application.include_router(auth.router, prefix="/api/v1")
    application.include_router(doctors.router, prefix="/api/v1")
    application.include_router(period.router, prefix="/api/v1")
    application.include_router(shift.router, prefix="/api/v1")
    application.include_router(assignment.router, prefix="/api/v1")
    application.include_router(extra.router, prefix="/api/v1")
    application.include_router(coverage.router, prefix="/api/v1")
    application.include_router(payroll.router, prefix="/api/v1")
    application.include_router(dashboard.router, prefix="/api/v1/query")

    return application
