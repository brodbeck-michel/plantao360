from typing import TypeVar, Generic, Optional, Any

from app.database.unit_of_work import UnitOfWork
from app.core.logging import get_logger

T = TypeVar("T")

logger = get_logger("service.base")


class BaseService(Generic[T]):
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def _log(self, event: str, **kwargs: Any) -> None:
        logger.info(event, extra={"event": event, **kwargs})
