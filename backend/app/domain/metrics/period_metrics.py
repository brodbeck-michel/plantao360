from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class PeriodMetrics:
    period_id: int
    year: int
    month: int
    status: str
    number_of_shifts: int = 0
    number_of_doctors: int = 0
    number_of_extras: int = 0
    total_hours: float = 0.0
    total_amount: float = 0.0
    opened_at: datetime | None = None
    closed_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year": self.year,
            "month": self.month,
            "status": self.status,
            "number_of_shifts": self.number_of_shifts,
            "number_of_doctors": self.number_of_doctors,
            "number_of_extras": self.number_of_extras,
            "total_hours": self.total_hours,
            "total_amount": self.total_amount,
            "opened_at": self.opened_at.isoformat() if self.opened_at else None,
            "closed_at": self.closed_at.isoformat() if self.closed_at else None,
        }
