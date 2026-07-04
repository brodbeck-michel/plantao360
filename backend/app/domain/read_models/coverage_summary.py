"""CoverageSummary — Immutable read model for coverage queries."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class CoverageSummary:
    """Immutable summary of coverage for query purposes."""
    period_id: int
    total_shifts: int = 0
    total_assignments_completed: int = 0
    total_assignments_planned: int = 0
    total_extras_approved: int = 0
    total_extras_pending: int = 0
    total_duration_minutes: int = 0
    coverage_rate: float = 0.0
    inconsistency_count: int = 0
    inconsistencies: list[dict] = field(default_factory=list)
    consolidated_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "total_shifts": self.total_shifts,
            "total_assignments_completed": self.total_assignments_completed,
            "total_assignments_planned": self.total_assignments_planned,
            "total_extras_approved": self.total_extras_approved,
            "total_extras_pending": self.total_extras_pending,
            "total_duration_minutes": self.total_duration_minutes,
            "coverage_rate": self.coverage_rate,
            "inconsistency_count": self.inconsistency_count,
            "inconsistencies": self.inconsistencies,
            "consolidated_at": self.consolidated_at.isoformat() if self.consolidated_at else None,
        }
