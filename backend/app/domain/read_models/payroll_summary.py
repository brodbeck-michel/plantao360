"""PayrollSummary — Immutable read model for payroll queries."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class PayrollSummary:
    """Immutable summary of a payroll competency for query purposes."""
    payroll_id: int
    period_id: int
    year_month: str
    status: str
    current_version: int
    total_value: float = 0.0
    total_doctors: int = 0
    total_facts: int = 0
    reopen_count: int = 0
    reopen_reason: str | None = None
    created_by: str = ""
    approved_by: str | None = None
    approved_at: datetime | None = None
    locked_by: str | None = None
    locked_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "payroll_id": self.payroll_id,
            "period_id": self.period_id,
            "year_month": self.year_month,
            "status": self.status,
            "current_version": self.current_version,
            "total_value": self.total_value,
            "total_doctors": self.total_doctors,
            "total_facts": self.total_facts,
            "reopen_count": self.reopen_count,
            "reopen_reason": self.reopen_reason,
            "created_by": self.created_by,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "locked_by": self.locked_by,
            "locked_at": self.locked_at.isoformat() if self.locked_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
