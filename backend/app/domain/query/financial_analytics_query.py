"""FinancialAnalyticsQuery — Business question about financials."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FinancialAnalyticsQuery:
    """Represents a business question about financial data."""
    period_id: int | None = None
    year_month: str | None = None
    doctor_id: int | None = None
    fact_type: str | None = None
    include_rules: bool = True
    include_explanations: bool = False
    include_version_comparison: bool = False
    compare_versions: list[int] = field(default_factory=list)
    sort_by: str = "total_value"
    sort_direction: str = "desc"

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year_month": self.year_month,
            "doctor_id": self.doctor_id,
            "fact_type": self.fact_type,
            "include_rules": self.include_rules,
            "include_explanations": self.include_explanations,
            "include_version_comparison": self.include_version_comparison,
            "compare_versions": self.compare_versions,
            "sort_by": self.sort_by,
            "sort_direction": self.sort_direction,
        }
