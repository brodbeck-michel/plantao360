import time
import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.common.context import get_request_id, get_correlation_id

logger = logging.getLogger("middleware.access")


class AccessLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        response: Response = await call_next(request)

        duration_ms = round((time.time() - start_time) * 1000, 2)
        request_id = get_request_id() or ""
        correlation_id = get_correlation_id() or ""

        logger.info(
            "Access log",
            extra={
                "event": "REQUEST",
                "method": request.method,
                "path": request.url.path,
                "status": response.status_code,
                "duration_ms": duration_ms,
                "request_id": request_id,
                "correlation_id": correlation_id,
            },
        )

        return response
