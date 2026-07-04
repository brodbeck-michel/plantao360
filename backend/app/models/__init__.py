"""Models SQLAlchemy - domínio Plantão 360."""

from app.models.base_mixins import TimestampMixin, SoftDeleteMixin
from app.models.doctor import Doctor
from app.models.period import Period
from app.models.shift import Shift
from app.models.shift_part import ShiftPart
from app.models.shift_extra import ShiftExtra
from app.models.payroll import Payroll
from app.models.financial_fact import FinancialFact
from app.models.coverage_snapshot import CoverageSnapshot
from app.models.financial_snapshot import FinancialSnapshot

__all__ = [
    "TimestampMixin",
    "SoftDeleteMixin",
    "Doctor",
    "Period",
    "Shift",
    "ShiftPart",
    "ShiftExtra",
    "Payroll",
    "FinancialFact",
    "CoverageSnapshot",
    "FinancialSnapshot",
]
