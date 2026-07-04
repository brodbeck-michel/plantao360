from dataclasses import dataclass


@dataclass(frozen=True)
class AssignmentDuration:
    minutes: int

    def __post_init__(self) -> None:
        if self.minutes <= 0:
            raise ValueError(f"Duration must be positive, got {self.minutes}")

    @property
    def hours(self) -> float:
        return self.minutes / 60.0

    @classmethod
    def from_start_end(cls, start_minutes: int, end_minutes: int) -> "AssignmentDuration":
        diff = end_minutes - start_minutes
        if diff <= 0:
            raise ValueError("End must be after start")
        return cls(minutes=diff)
