"""AuditAnalytics — Audit analytics queries and results."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class ReopenedCompetency:
    """Record of a reopened competency."""
    payroll_id: int
    year_month: str
    reopened_by: str
    reopened_at: str
    reason: str
    previous_version: int
    new_version: int

    def to_dict(self) -> dict:
        return {
            "payroll_id": self.payroll_id,
            "year_month": self.year_month,
            "reopened_by": self.reopened_by,
            "reopened_at": self.reopened_at,
            "reason": self.reason,
            "previous_version": self.previous_version,
            "new_version": self.new_version,
        }


@dataclass(frozen=True)
class ApprovalRecord:
    """Record of an approval."""
    payroll_id: int
    year_month: str
    approved_by: str
    approved_at: str
    version: int
    checklist_complete: bool

    def to_dict(self) -> dict:
        return {
            "payroll_id": self.payroll_id,
            "year_month": self.year_month,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "version": self.version,
            "checklist_complete": self.checklist_complete,
        }


@dataclass(frozen=True)
class AuditAnalytics:
    """Audit analytics results."""
    total_competencies: int = 0
    reopened_competencies: list[ReopenedCompetency] = field(default_factory=list)
    reopen_count: int = 0
    reopen_rate: float = 0.0
    approvals: list[ApprovalRecord] = field(default_factory=list)
    average_time_to_close_days: float = 0.0
    average_time_to_approve_days: float = 0.0
    segregation_violations: int = 0
    changes_after_lock: int = 0
    audit_trail_integrity: bool = True
    generated_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "total_competencies": self.total_competencies,
            "reopened_competencies": [r.to_dict() for r in self.reopened_competencies],
            "reopen_count": self.reopen_count,
            "reopen_rate": self.reopen_rate,
            "approvals": [a.to_dict() for a in self.approvals],
            "average_time_to_close_days": self.average_time_to_close_days,
            "average_time_to_approve_days": self.average_time_to_approve_days,
            "segregation_violations": self.segregation_violations,
            "changes_after_lock": self.changes_after_lock,
            "audit_trail_integrity": self.audit_trail_integrity,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }
