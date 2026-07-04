"""DashboardProjection — Projects operational dashboard data for queries."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class DashboardProjection:
    """Projects operational dashboard data from all aggregates without modifying them.

    Consumes data from Period, Shift, Doctor, ShiftPart, ShiftExtra aggregates
    to create a consolidated view optimized for the operational dashboard.

    Follows the same pattern as CoverageProjection, FinancialProjection, etc.
    """
    # Current period
    period_id: int = 0
    period_year: int = 0
    period_month: int = 0
    period_name: str = ""
    period_status: str = ""
    period_start_date: str = ""
    period_end_date: str = ""

    # Shifts
    total_shifts: int = 0
    assigned_shifts: int = 0
    unassigned_shifts: int = 0
    scheduled_shifts: int = 0
    in_progress_shifts: int = 0
    completed_shifts: int = 0
    cancelled_shifts: int = 0

    # Doctors
    total_doctors: int = 0
    active_doctors: int = 0
    doctors_with_shifts: int = 0
    doctors_without_shifts: int = 0

    # Coverage
    coverage_rate: float = 0.0
    total_duration_minutes: int = 0
    total_duration_hours: float = 0.0

    # Extras
    total_extras: int = 0
    pending_extras: int = 0
    approved_extras: int = 0
    rejected_extras: int = 0

    # Periods
    open_periods: int = 0
    closed_periods: int = 0

    # Computed
    doctors_per_shift: float = 0.0
    utilization_rate: float = 0.0

    projected_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "period_year": self.period_year,
            "period_month": self.period_month,
            "period_name": self.period_name,
            "period_status": self.period_status,
            "period_start_date": self.period_start_date,
            "period_end_date": self.period_end_date,
            "total_shifts": self.total_shifts,
            "assigned_shifts": self.assigned_shifts,
            "unassigned_shifts": self.unassigned_shifts,
            "scheduled_shifts": self.scheduled_shifts,
            "in_progress_shifts": self.in_progress_shifts,
            "completed_shifts": self.completed_shifts,
            "cancelled_shifts": self.cancelled_shifts,
            "total_doctors": self.total_doctors,
            "active_doctors": self.active_doctors,
            "doctors_with_shifts": self.doctors_with_shifts,
            "doctors_without_shifts": self.doctors_without_shifts,
            "coverage_rate": self.coverage_rate,
            "total_duration_minutes": self.total_duration_minutes,
            "total_duration_hours": self.total_duration_hours,
            "total_extras": self.total_extras,
            "pending_extras": self.pending_extras,
            "approved_extras": self.approved_extras,
            "rejected_extras": self.rejected_extras,
            "open_periods": self.open_periods,
            "closed_periods": self.closed_periods,
            "doctors_per_shift": self.doctors_per_shift,
            "utilization_rate": self.utilization_rate,
            "projected_at": self.projected_at.isoformat() if self.projected_at else None,
        }
