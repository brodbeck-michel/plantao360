"""Read Models — Immutable models for query domain."""

from app.domain.read_models.doctor_summary import DoctorSummary
from app.domain.read_models.period_summary import PeriodSummary
from app.domain.read_models.shift_summary import ShiftSummary
from app.domain.read_models.assignment_summary import AssignmentSummary
from app.domain.read_models.coverage_summary import CoverageSummary
from app.domain.read_models.dashboard_summary import (
    DashboardSummary,
    CurrentPeriodSummary,
    HealthCardSummary,
    OperationalKPISummary,
    ActivitySummary,
    OperationalAlertSummary,
    UpcomingActionSummary,
)
from app.domain.read_models.financial_summary import FinancialSummary
from app.domain.read_models.payroll_summary import PayrollSummary

__all__ = [
    "DoctorSummary",
    "PeriodSummary",
    "ShiftSummary",
    "AssignmentSummary",
    "CoverageSummary",
    "DashboardSummary",
    "CurrentPeriodSummary",
    "HealthCardSummary",
    "OperationalKPISummary",
    "ActivitySummary",
    "OperationalAlertSummary",
    "UpcomingActionSummary",
    "FinancialSummary",
    "PayrollSummary",
]
