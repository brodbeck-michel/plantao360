from datetime import time, datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class AssignmentTimeline:
    start_time: time
    end_time: time

    def __post_init__(self) -> None:
        if self.end_time <= self.start_time:
            raise ValueError(
                f"end_time ({self.end_time}) must be after start_time ({self.start_time})"
            )

    @property
    def duration_minutes(self) -> int:
        start_dt = datetime(2000, 1, 1, self.start_time.hour, self.start_time.minute)
        end_dt = datetime(2000, 1, 1, self.end_time.hour, self.end_time.minute)
        delta = end_dt - start_dt
        return int(delta.total_seconds() / 60)

    @property
    def duration_hours(self) -> float:
        return self.duration_minutes / 60.0

    def overlaps(self, other: "AssignmentTimeline") -> bool:
        return self.start_time < other.end_time and other.start_time < self.end_time
