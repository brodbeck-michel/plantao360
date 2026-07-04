"""PeriodSummary — Immutable read model for period queries."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class PeriodSummary:
    """Immutable summary of a period for query purposes."""
    period_id: int
    year: int
    month: int
    status: str
    total_shifts: int = 0
    total_doctors: int = 0
    total_extras: int = 0
    total_hours: float = 0.0
    total_duration_minutes: int = 0
    created_at: datetime | None = None
    updated_at: datetime | None = None
    closed_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year": self.year,
            "month": self.month,
            "status": self.status,
            "total_shifts": self.total_shifts,
            "total_doctors": self.total_doctors,
            "total_extras": self.total_extras,
            "total_hours": self.total_hours,
            "total_duration_minutes": self.total_duration_minutes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
        }
