from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions.errors import (
    BusinessRuleError,
    NotFoundError,
    ConflictError,
    UnauthorizedError,
)


def register_exception_handlers(application: FastAPI) -> None:
    @application.exception_handler(BusinessRuleError)
    async def business_rule_error_handler(request: Request, exc: BusinessRuleError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": exc.status_code,
                "detail": exc.detail,
                "type": exc.error_type,
            },
        )

    @application.exception_handler(NotFoundError)
    async def not_found_error_handler(request: Request, exc: NotFoundError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": exc.status_code,
                "detail": exc.detail,
                "type": exc.error_type,
            },
        )

    @application.exception_handler(ConflictError)
    async def conflict_error_handler(request: Request, exc: ConflictError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": exc.status_code,
                "detail": exc.detail,
                "type": exc.error_type,
            },
        )

    @application.exception_handler(UnauthorizedError)
    async def unauthorized_error_handler(request: Request, exc: UnauthorizedError):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "status": exc.status_code,
                "detail": exc.detail,
                "type": exc.error_type,
            },
        )

    @application.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "status": 500,
                "detail": "Erro interno do servidor",
                "type": "internal_server_error",
            },
        )
