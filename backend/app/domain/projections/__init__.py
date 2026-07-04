"""Projections — Transform aggregates into query-optimized formats."""

from app.domain.projections.coverage_projection import CoverageProjection
from app.domain.projections.dashboard_projection import DashboardProjection
from app.domain.projections.financial_projection import FinancialProjection
from app.domain.projections.payroll_projection import PayrollProjection
from app.domain.projections.institution_projection import InstitutionProjection

__all__ = [
    "CoverageProjection",
    "DashboardProjection",
    "FinancialProjection",
    "PayrollProjection",
    "InstitutionProjection",
]
