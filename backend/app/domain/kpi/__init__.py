"""KPI Domain — Key Performance Indicators."""

from app.domain.kpi.coverage_kpi import CoverageKPI
from app.domain.kpi.financial_kpi import FinancialKPI
from app.domain.kpi.payroll_kpi import PayrollKPI
from app.domain.kpi.operational_kpi import OperationalKPI

__all__ = [
    "CoverageKPI",
    "FinancialKPI",
    "PayrollKPI",
    "OperationalKPI",
]
