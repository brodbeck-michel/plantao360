from abc import ABC, abstractmethod
from datetime import datetime, timezone


class ClockProvider(ABC):
    @abstractmethod
    def now(self) -> datetime: ...


class SystemClock(ClockProvider):
    def now(self) -> datetime:
        return datetime.now(timezone.utc)


class FutureClock(ClockProvider):
    def __init__(self, fixed_time: datetime):
        self._fixed_time = fixed_time

    def now(self) -> datetime:
        return self._fixed_time
