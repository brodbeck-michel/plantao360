from contextvars import ContextVar

from app.common.types import RequestID, CorrelationID

request_id_context: ContextVar[RequestID | None] = ContextVar(
    "request_id_context", default=None
)
correlation_id_context: ContextVar[CorrelationID | None] = ContextVar(
    "correlation_id_context", default=None
)


def set_request_id(value: RequestID) -> None:
    request_id_context.set(value)


def get_request_id() -> RequestID | None:
    return request_id_context.get()


def set_correlation_id(value: CorrelationID) -> None:
    correlation_id_context.set(value)


def get_correlation_id() -> CorrelationID | None:
    return correlation_id_context.get()
