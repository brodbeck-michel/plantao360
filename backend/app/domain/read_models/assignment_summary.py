"""AssignmentSummary — Immutable read model for assignment queries."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class AssignmentSummary:
    """Immutable summary of an assignment for query purposes."""
    assignment_id: int
    shift_id: int
    doctor_id: int
    doctor_name: str
    doctor_crm: str
    status: str
    start_time: datetime | None = None
    end_time: datetime | None = None
    duration_minutes: int = 0
    shift_date: str = ""
    shift_type: str = ""
    created_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "assignment_id": self.assignment_id,
            "shift_id": self.shift_id,
            "doctor_id": self.doctor_id,
            "doctor_name": self.doctor_name,
            "doctor_crm": self.doctor_crm,
            "status": self.status,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_minutes": self.duration_minutes,
            "shift_date": self.shift_date,
            "shift_type": self.shift_type,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
