from dataclasses import dataclass
from datetime import datetime

from app.domain.constants.period_status import PeriodStatus


@dataclass(frozen=True)
class PeriodSnapshot:
    id: int
    year: int
    month: int
    status: PeriodStatus
    created_at: datetime | None
    updated_at: datetime | None
    number_of_shifts: int = 0
    number_of_doctors: int = 0
    total_hours: float = 0.0

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "year": self.year,
            "month": self.month,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "number_of_shifts": self.number_of_shifts,
            "number_of_doctors": self.number_of_doctors,
            "total_hours": self.total_hours,
        }
