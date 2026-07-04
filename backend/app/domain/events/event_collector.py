from __future__ import annotations

from typing import Any


class EventCollector:
    def __init__(self) -> None:
        self._events: list[dict[str, Any]] = []

    def add(self, name: str, data: dict[str, Any] | None = None) -> None:
        self._events.append({"name": name, "data": data or {}})

    @property
    def events(self) -> list[dict[str, Any]]:
        return list(self._events)

    def clear(self) -> None:
        self._events.clear()

    def __len__(self) -> int:
        return len(self._events)

    def __bool__(self) -> bool:
        return len(self._events) > 0
