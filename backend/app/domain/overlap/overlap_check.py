from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True)
class OverlapCheckRequest:
    doctor_id: int
    shift_id: int
    start_time: time
    end_time: time
    exclude_assignment_id: int | None = None


@dataclass(frozen=True)
class OverlapResult:
    has_overlap: bool
    conflicting_assignment_ids: list[int]
    message: str = ""

    @classmethod
    def none(cls) -> "OverlapResult":
        return cls(has_overlap=False, conflicting_assignment_ids=[])

    @classmethod
    def found(cls, assignment_ids: list[int], message: str = "") -> "OverlapResult":
        return cls(
            has_overlap=True,
            conflicting_assignment_ids=assignment_ids,
            message=message,
        )
