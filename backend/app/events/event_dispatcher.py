from typing import Any, Callable
from dataclasses import dataclass, field

from app.core.logging import get_logger

logger = get_logger("events")


@dataclass
class Event:
    name: str
    data: dict[str, Any] = field(default_factory=dict)


class EventDispatcher:
    def __init__(self):
        self._handlers: dict[str, list[Callable]] = {}

    def register(self, event_name: str, handler: Callable) -> None:
        if event_name not in self._handlers:
            self._handlers[event_name] = []
        self._handlers[event_name].append(handler)

    def dispatch(self, event: Event) -> None:
        handlers = self._handlers.get(event.name, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Error dispatching event {event.name}: {e}")

    def clear(self) -> None:
        self._handlers.clear()
