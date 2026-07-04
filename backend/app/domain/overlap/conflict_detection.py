from dataclasses import dataclass


@dataclass(frozen=True)
class ConflictDetectionRequest:
    doctor_id: int
    shift_date: str
    start_time: str
    end_time: str
    exclude_assignment_id: int | None = None


@dataclass(frozen=True)
class ConflictResult:
    has_conflict: bool
    conflicting_shift_ids: list[int]
    message: str = ""

    @classmethod
    def none(cls) -> "ConflictResult":
        return cls(has_conflict=False, conflicting_shift_ids=[])

    @classmethod
    def found(cls, shift_ids: list[int], message: str = "") -> "ConflictResult":
        return cls(
            has_conflict=True,
            conflicting_shift_ids=shift_ids,
            message=message,
        )
