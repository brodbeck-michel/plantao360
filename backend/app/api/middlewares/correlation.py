from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from app.common.identifiers import generate_uuid_str
from app.common.context import set_request_id, set_correlation_id
from app.core.logging import get_logger

logger = get_logger("middleware.correlation")


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Request-ID") or generate_uuid_str()
        request_id = correlation_id

        set_request_id(request_id)
        set_correlation_id(correlation_id)

        request.state.correlation_id = correlation_id
        request.state.request_id = request_id

        response: Response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Correlation-ID"] = correlation_id

        logger.info(
            "Request processed",
            extra={
                "event": "REQUEST",
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "request_id": request_id,
                "correlation_id": correlation_id,
            },
        )

        return response
