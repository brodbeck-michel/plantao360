"""DoctorAnalyticsQuery — Business question about doctors."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DoctorAnalyticsQuery:
    """Represents a business question about doctors.

    Nunca é um filtro HTTP. Representa uma pergunta de negócio.
    """
    doctor_id: int | None = None
    active_only: bool = True
    period_id: int | None = None
    year_month: str | None = None
    include_totals: bool = True
    include_remuneration: bool = False
    include_shifts: bool = True
    sort_by: str = "name"
    sort_direction: str = "asc"

    def to_dict(self) -> dict:
        return {
            "doctor_id": self.doctor_id,
            "active_only": self.active_only,
            "period_id": self.period_id,
            "year_month": self.year_month,
            "include_totals": self.include_totals,
            "include_remuneration": self.include_remuneration,
            "include_shifts": self.include_shifts,
            "sort_by": self.sort_by,
            "sort_direction": self.sort_direction,
        }
