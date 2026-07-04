from datetime import datetime, timedelta
from dataclasses import dataclass


@dataclass(frozen=True)
class ShiftTimeRange:
    start: datetime
    end: datetime

    def __post_init__(self) -> None:
        if self.end <= self.start:
            raise ValueError(f"End time ({self.end}) must be after start time ({self.start})")

    @property
    def duration_minutes(self) -> int:
        delta = self.end - self.start
        return int(delta.total_seconds() / 60)

    @property
    def duration_hours(self) -> float:
        return self.duration_minutes / 60.0
