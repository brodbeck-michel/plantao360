"""CoverageAnalyticsQuery — Business question about coverage."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class CoverageAnalyticsQuery:
    """Represents a business question about coverage."""
    period_id: int | None = None
    year_month: str | None = None
    shift_type: str | None = None
    include_inconsistencies: bool = True
    include_extras: bool = True
    include_uncovered: bool = False
    doctor_id: int | None = None
    sort_by: str = "shift_date"
    sort_direction: str = "asc"

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year_month": self.year_month,
            "shift_type": self.shift_type,
            "include_inconsistencies": self.include_inconsistencies,
            "include_extras": self.include_extras,
            "include_uncovered": self.include_uncovered,
            "doctor_id": self.doctor_id,
            "sort_by": self.sort_by,
            "sort_direction": self.sort_direction,
        }
