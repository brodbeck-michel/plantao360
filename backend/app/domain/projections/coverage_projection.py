"""CoverageProjection — Projects coverage data for queries."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class CoverageProjection:
    """Projects coverage data from aggregates without modifying them.

    Consome CoverageEngine results e FinancialSnapshot para criar
    uma visão otimizada para consulta.
    """
    period_id: int
    total_shifts: int = 0
    total_assignments_completed: int = 0
    total_assignments_planned: int = 0
    total_extras_approved: int = 0
    total_extras_rejected: int = 0
    total_extras_pending: int = 0
    total_duration_minutes: int = 0
    total_duration_hours: float = 0.0
    coverage_rate: float = 0.0
    uncovered_shifts: int = 0
    inconsistency_count: int = 0
    inconsistencies: list[dict] = field(default_factory=list)
    doctor_coverage: list[dict] = field(default_factory=list)
    shift_type_coverage: list[dict] = field(default_factory=list)
    projected_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "total_shifts": self.total_shifts,
            "total_assignments_completed": self.total_assignments_completed,
            "total_assignments_planned": self.total_assignments_planned,
            "total_extras_approved": self.total_extras_approved,
            "total_extras_rejected": self.total_extras_rejected,
            "total_extras_pending": self.total_extras_pending,
            "total_duration_minutes": self.total_duration_minutes,
            "total_duration_hours": self.total_duration_hours,
            "coverage_rate": self.coverage_rate,
            "uncovered_shifts": self.uncovered_shifts,
            "inconsistency_count": self.inconsistency_count,
            "inconsistencies": self.inconsistencies,
            "doctor_coverage": self.doctor_coverage,
            "shift_type_coverage": self.shift_type_coverage,
            "projected_at": self.projected_at.isoformat() if self.projected_at else None,
        }
