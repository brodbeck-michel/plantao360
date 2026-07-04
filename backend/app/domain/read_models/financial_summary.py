"""FinancialSummary — Immutable read model for financial queries."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class FinancialSummary:
    """Immutable summary of financial data for query purposes."""
    period_id: int
    total_facts: int = 0
    total_duration_minutes: int = 0
    total_value: float = 0.0
    total_doctors: int = 0
    facts_by_type: dict[str, int] = field(default_factory=dict)
    facts_by_status: dict[str, int] = field(default_factory=dict)
    rules_applied: list[str] = field(default_factory=list)
    created_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "total_facts": self.total_facts,
            "total_duration_minutes": self.total_duration_minutes,
            "total_value": self.total_value,
            "total_doctors": self.total_doctors,
            "facts_by_type": self.facts_by_type,
            "facts_by_status": self.facts_by_status,
            "rules_applied": self.rules_applied,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
