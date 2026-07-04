"""FinancialProjection — Projects financial data for queries."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class FinancialProjection:
    """Projects financial data from aggregates without modifying them."""
    period_id: int
    total_facts: int = 0
    total_duration_minutes: int = 0
    total_duration_hours: float = 0.0
    total_value: float = 0.0
    total_doctors: int = 0
    facts_by_type: dict[str, int] = field(default_factory=dict)
    facts_by_status: dict[str, int] = field(default_factory=dict)
    value_by_doctor: list[dict] = field(default_factory=list)
    value_by_fact_type: list[dict] = field(default_factory=list)
    rules_applied: list[dict] = field(default_factory=list)
    average_value_per_hour: float = 0.0
    projected_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "total_facts": self.total_facts,
            "total_duration_minutes": self.total_duration_minutes,
            "total_duration_hours": self.total_duration_hours,
            "total_value": self.total_value,
            "total_doctors": self.total_doctors,
            "facts_by_type": self.facts_by_type,
            "facts_by_status": self.facts_by_status,
            "value_by_doctor": self.value_by_doctor,
            "value_by_fact_type": self.value_by_fact_type,
            "rules_applied": self.rules_applied,
            "average_value_per_hour": self.average_value_per_hour,
            "projected_at": self.projected_at.isoformat() if self.projected_at else None,
        }
