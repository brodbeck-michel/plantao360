"""DoctorSummary — Immutable read model for doctor queries."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class DoctorSummary:
    """Immutable summary of a doctor for query purposes.

    Desacoplado do Model SQLAlchemy. Consome dados do Aggregate sem modificá-lo.
    """
    doctor_id: int
    name: str
    crm: str
    hour_rate: float
    active: bool
    total_shifts: int = 0
    total_hours: float = 0.0
    total_extras: int = 0
    total_remuneration: float = 0.0
    last_shift_date: datetime | None = None
    created_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "doctor_id": self.doctor_id,
            "name": self.name,
            "crm": self.crm,
            "hour_rate": self.hour_rate,
            "active": self.active,
            "total_shifts": self.total_shifts,
            "total_hours": self.total_hours,
            "total_extras": self.total_extras,
            "total_remuneration": self.total_remuneration,
            "last_shift_date": self.last_shift_date.isoformat() if self.last_shift_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
