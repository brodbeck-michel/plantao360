"""InstitutionProjection — Projects institution-wide data for queries."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class InstitutionProjection:
    """Projects institution-wide data from all aggregates without modifying them."""
    total_doctors: int = 0
    active_doctors: int = 0
    total_periods: int = 0
    open_periods: int = 0
    closed_periods: int = 0
    total_shifts: int = 0
    total_assignments: int = 0
    total_extras: int = 0
    total_hours_worked: float = 0.0
    total_remuneration: float = 0.0
    average_cost_per_shift: float = 0.0
    average_coverage_rate: float = 0.0
    total_payroll_competencies: int = 0
    pending_approvals: int = 0
    locked_competencies: int = 0
    last_period_status: str = ""
    last_period_year_month: str = ""
    projected_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "total_doctors": self.total_doctors,
            "active_doctors": self.active_doctors,
            "total_periods": self.total_periods,
            "open_periods": self.open_periods,
            "closed_periods": self.closed_periods,
            "total_shifts": self.total_shifts,
            "total_assignments": self.total_assignments,
            "total_extras": self.total_extras,
            "total_hours_worked": self.total_hours_worked,
            "total_remuneration": self.total_remuneration,
            "average_cost_per_shift": self.average_cost_per_shift,
            "average_coverage_rate": self.average_coverage_rate,
            "total_payroll_competencies": self.total_payroll_competencies,
            "pending_approvals": self.pending_approvals,
            "locked_competencies": self.locked_competencies,
            "last_period_status": self.last_period_status,
            "last_period_year_month": self.last_period_year_month,
            "projected_at": self.projected_at.isoformat() if self.projected_at else None,
        }
