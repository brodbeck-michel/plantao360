from __future__ import annotations

from typing import Any

from app.domain.events.event_collector import EventCollector


class AggregateRoot:
    def __init__(self) -> None:
        self._version: int = 1
        self._event_collector: EventCollector = EventCollector()

    @property
    def aggregate_id(self) -> int | None:
        return getattr(self, "id", None)

    @property
    def version(self) -> int:
        return self._version

    def add_event(self, name: str, data: dict[str, Any] | None = None) -> None:
        self._event_collector.add(name=name, data=data or {})

    @property
    def pending_events(self) -> list[dict[str, Any]]:
        return self._event_collector.events

    def clear_events(self) -> None:
        self._event_collector.clear()

    def before_transition(self, from_status: str, to_status: str) -> None:
        pass

    def after_transition(self, from_status: str, to_status: str) -> None:
        pass
