"""CompetencyAudit — Audit data for a specific competency."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class CompetencyAudit:
    """Audit data for a specific payroll competency."""
    payroll_id: int
    year_month: str
    status: str
    current_version: int
    reopen_count: int
    created_by: str
    created_at: str
    audit_entries: list[dict] = field(default_factory=list)
    versions: list[dict] = field(default_factory=list)
    seal_present: bool = False
    checklist_complete: bool = False
    approval_present: bool = False
    lock_present: bool = False
    generated_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "payroll_id": self.payroll_id,
            "year_month": self.year_month,
            "status": self.status,
            "current_version": self.current_version,
            "reopen_count": self.reopen_count,
            "created_by": self.created_by,
            "created_at": self.created_at,
            "audit_entries": self.audit_entries,
            "versions": self.versions,
            "seal_present": self.seal_present,
            "checklist_complete": self.checklist_complete,
            "approval_present": self.approval_present,
            "lock_present": self.lock_present,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }
