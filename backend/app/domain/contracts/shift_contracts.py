from dataclasses import dataclass


@dataclass(frozen=True)
class AssignDoctor:
    doctor_id: int
    shift_id: int
    start_time: str
    end_time: str


@dataclass(frozen=True)
class RemoveDoctor:
    doctor_id: int
    shift_id: int


@dataclass(frozen=True)
class ValidateCoverage:
    shift_id: int
    min_doctors: int = 1
    max_doctors: int | None = None


@dataclass(frozen=True)
class ValidateOverlap:
    doctor_id: int
    shift_id: int
    start_time: str
    end_time: str
