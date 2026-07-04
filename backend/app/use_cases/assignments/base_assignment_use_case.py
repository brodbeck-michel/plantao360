from abc import ABC, abstractmethod
from typing import Any

from app.common.result import Result
from app.events.event_dispatcher import EventDispatcher, Event
from app.core.logging import get_logger

logger = get_logger("use_case.assignment")


class BaseAssignmentUseCase(ABC):
    def __init__(self, repo=None, shift_repo=None, doctor_repo=None):
        self.repo = repo
        self.shift_repo = shift_repo
        self.doctor_repo = doctor_repo
        self._events: list[Event] = []

    def __call__(self, **kwargs) -> Result:
        validation_result = self.validate(**kwargs)
        if validation_result is not None:
            return validation_result

        try:
            result = self.execute(**kwargs)
        except Exception as e:
            from app.common.result import Failure
            logger.error("assignment.use_case.error", extra={"error": str(e)})
            return Failure(error=str(e), code="INTERNAL_ERROR")

        self._emit_events()
        return result

    @abstractmethod
    def validate(self, **kwargs) -> Result | None:
        ...

    @abstractmethod
    def execute(self, **kwargs) -> Result:
        ...

    def _queue_event(self, name: str, data: dict[str, Any]) -> None:
        self._events.append(Event(name=name, data=data))

    def _emit_events(self) -> None:
        dispatcher = EventDispatcher()
        for event in self._events:
            dispatcher.dispatch(event)
        self._events.clear()
