"""PayrollProjection — Projects payroll data for queries."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class PayrollProjection:
    """Projects payroll data from aggregates without modifying them."""
    payroll_id: int
    period_id: int
    year_month: str
    status: str
    current_version: int
    total_value: float = 0.0
    total_doctors: int = 0
    total_facts: int = 0
    total_rules: int = 0
    reopen_count: int = 0
    reopen_reason: str | None = None
    created_by: str = ""
    approved_by: str | None = None
    approved_at: datetime | None = None
    locked_by: str | None = None
    locked_at: datetime | None = None
    checklist_complete: bool = False
    checklist_items: list[dict] = field(default_factory=list)
    audit_entries_count: int = 0
    versions: list[dict] = field(default_factory=list)
    projected_at: datetime | None = None

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
            "total_rules": self.total_rules,
            "reopen_count": self.reopen_count,
            "reopen_reason": self.reopen_reason,
            "created_by": self.created_by,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "locked_by": self.locked_by,
            "locked_at": self.locked_at.isoformat() if self.locked_at else None,
            "checklist_complete": self.checklist_complete,
            "checklist_items": self.checklist_items,
            "audit_entries_count": self.audit_entries_count,
            "versions": self.versions,
            "projected_at": self.projected_at.isoformat() if self.projected_at else None,
        }
