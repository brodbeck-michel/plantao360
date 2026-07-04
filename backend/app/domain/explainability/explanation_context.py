"""ExplanationContext — Context for a domain explanation."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class ExplanationContext:
    """Context providing additional information for an explanation."""
    entity_type: str = ""
    entity_id: int | None = None
    period_id: int | None = None
    year_month: str | None = None
    doctor_id: int | None = None
    version: int | None = None
    requested_by: str = ""
    requested_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "period_id": self.period_id,
            "year_month": self.year_month,
            "doctor_id": self.doctor_id,
            "version": self.version,
            "requested_by": self.requested_by,
            "requested_at": self.requested_at.isoformat() if self.requested_at else None,
        }
