"""ShiftSummary — Immutable read model for shift queries."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class ShiftSummary:
    """Immutable summary of a shift for query purposes."""
    shift_id: int
    period_id: int
    shift_date: str
    shift_type: str
    status: str
    scheduled_start: datetime | None = None
    scheduled_end: datetime | None = None
    actual_start: datetime | None = None
    actual_end: datetime | None = None
    total_duration_minutes: int = 0
    doctor_count: int = 0
    doctors: list[int] = field(default_factory=list)
    has_extras: bool = False
    created_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "shift_id": self.shift_id,
            "period_id": self.period_id,
            "shift_date": self.shift_date,
            "shift_type": self.shift_type,
            "status": self.status,
            "scheduled_start": self.scheduled_start.isoformat() if self.scheduled_start else None,
            "scheduled_end": self.scheduled_end.isoformat() if self.scheduled_end else None,
            "actual_start": self.actual_start.isoformat() if self.actual_start else None,
            "actual_end": self.actual_end.isoformat() if self.actual_end else None,
            "total_duration_minutes": self.total_duration_minutes,
            "doctor_count": self.doctor_count,
            "doctors": self.doctors,
            "has_extras": self.has_extras,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
