from typing import Any, Callable
from functools import wraps

from app.core.logging import get_logger

logger = get_logger("audit")


def audit(action: str, resource: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.info(
                f"AUDIT: {action} on {resource}",
                extra={
                    "event": "AUDIT",
                    "action": action,
                    "resource": resource,
                },
            )
            return func(*args, **kwargs)

        return wrapper

    return decorator
