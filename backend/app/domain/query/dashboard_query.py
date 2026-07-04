"""DashboardQuery — Business question about operational dashboard."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DashboardQuery:
    """Represents a business question about the operational dashboard.

    Used by the Query Domain to retrieve consolidated operational data
    for the current period, including health cards, KPIs, activities,
    and alerts.

    Follows the same pattern as DoctorAnalyticsQuery, CoverageAnalyticsQuery, etc.
    """
    # Period filters
    period_id: int | None = None
    year_month: str | None = None

    # Future evolution: multi-unit, sector-specific, doctor-specific dashboards
    organization_id: int | None = None
    sector_id: int | None = None
    doctor_id: int | None = None

    # Include flags
    include_health_cards: bool = True
    include_kpis: bool = True
    include_recent_activities: bool = True
    include_operational_alerts: bool = True
    include_upcoming_actions: bool = True

    # Pagination
    activity_limit: int = 10
    alert_limit: int = 20

    # Sorting
    sort_by: str = "generated_at"
    sort_direction: str = "desc"

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year_month": self.year_month,
            "organization_id": self.organization_id,
            "sector_id": self.sector_id,
            "doctor_id": self.doctor_id,
            "include_health_cards": self.include_health_cards,
            "include_kpis": self.include_kpis,
            "include_recent_activities": self.include_recent_activities,
            "include_operational_alerts": self.include_operational_alerts,
            "include_upcoming_actions": self.include_upcoming_actions,
            "activity_limit": self.activity_limit,
            "alert_limit": self.alert_limit,
            "sort_by": self.sort_by,
            "sort_direction": self.sort_direction,
        }
