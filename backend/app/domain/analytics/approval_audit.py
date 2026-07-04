"""ApprovalAudit — Audit data for approvals."""

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ApprovalAudit:
    """Audit data for approval processes."""
    payroll_id: int
    year_month: str
    approved_by: str
    approved_at: str
    version: int
    checklist_version: int
    checklist_items_satisfied: int
    checklist_items_total: int
    readiness_status: str
    justification: str = ""
    observations: str = ""
    generated_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "payroll_id": self.payroll_id,
            "year_month": self.year_month,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at,
            "version": self.version,
            "checklist_version": self.checklist_version,
            "checklist_items_satisfied": self.checklist_items_satisfied,
            "checklist_items_total": self.checklist_items_total,
            "readiness_status": self.readiness_status,
            "justification": self.justification,
            "observations": self.observations,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }
