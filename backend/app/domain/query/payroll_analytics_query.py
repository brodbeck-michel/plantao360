"""PayrollAnalyticsQuery — Business question about payroll."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PayrollAnalyticsQuery:
    """Represents a business question about payroll competencies."""
    payroll_id: int | None = None
    period_id: int | None = None
    year_month: str | None = None
    status: str | None = None
    include_audit: bool = True
    include_versions: bool = False
    include_seal: bool = False
    include_checklist: bool = False
    include_approval: bool = False
    include_timeline: bool = False
    sort_by: str = "year_month"
    sort_direction: str = "desc"

    def to_dict(self) -> dict:
        return {
            "payroll_id": self.payroll_id,
            "period_id": self.period_id,
            "year_month": self.year_month,
            "status": self.status,
            "include_audit": self.include_audit,
            "include_versions": self.include_versions,
            "include_seal": self.include_seal,
            "include_checklist": self.include_checklist,
            "include_approval": self.include_approval,
            "include_timeline": self.include_timeline,
            "sort_by": self.sort_by,
            "sort_direction": self.sort_direction,
        }
