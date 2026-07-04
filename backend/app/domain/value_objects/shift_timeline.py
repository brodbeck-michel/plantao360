from datetime import datetime
from dataclasses import dataclass


@dataclass
class ShiftTimeline:
    scheduled_start: datetime | None = None
    scheduled_end: datetime | None = None
    actual_start: datetime | None = None
    actual_end: datetime | None = None

    @property
    def has_schedule(self) -> bool:
        return self.scheduled_start is not None and self.scheduled_end is not None

    @property
    def has_actual(self) -> bool:
        return self.actual_start is not None and self.actual_end is not None

    @property
    def is_active(self) -> bool:
        return self.actual_start is not None and self.actual_end is None

    def record_start(self, now: datetime) -> None:
        self.actual_start = now

    def record_end(self, now: datetime) -> None:
        if self.actual_start is None:
            raise ValueError("Cannot end a shift that was never started")
        self.actual_end = now

    def planned_duration_minutes(self) -> int | None:
        if not self.has_schedule:
            return None
        delta = self.scheduled_end - self.scheduled_start  # type: ignore
        return int(delta.total_seconds() / 60)

    def actual_duration_minutes(self) -> int | None:
        if not self.has_actual:
            return None
        delta = self.actual_end - self.actual_start  # type: ignore
        return int(delta.total_seconds() / 60)
