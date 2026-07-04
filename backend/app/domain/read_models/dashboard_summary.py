"""DashboardSummary — Immutable read models for operational dashboard."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class CurrentPeriodSummary:
    """Immutable summary of the current active period."""
    period_id: int
    year: int
    month: int
    name: str
    status: str
    total_shifts: int = 0
    total_doctors: int = 0
    total_hours: float = 0.0
    start_date: str = ""
    end_date: str = ""

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year": self.year,
            "month": self.month,
            "name": self.name,
            "status": self.status,
            "total_shifts": self.total_shifts,
            "total_doctors": self.total_doctors,
            "total_hours": self.total_hours,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }


@dataclass(frozen=True)
class HealthCardSummary:
    """Immutable health card for operational status display."""
    card_id: str
    label: str
    status: str  # healthy | warning | critical
    severity: str  # low | medium | high | critical
    value: str
    detail: str
    trend: str = ""  # +5% | -3% | stable
    trend_direction: str = "flat"  # up | down | flat
    icon: str = ""
    action_route: str = ""

    def to_dict(self) -> dict:
        return {
            "card_id": self.card_id,
            "label": self.label,
            "status": self.status,
            "severity": self.severity,
            "value": self.value,
            "detail": self.detail,
            "trend": self.trend,
            "trend_direction": self.trend_direction,
            "icon": self.icon,
            "action_route": self.action_route,
        }


@dataclass(frozen=True)
class OperationalKPISummary:
    """Immutable KPI summary for the operational dashboard."""
    total_shifts: int = 0
    assigned_shifts: int = 0
    unassigned_shifts: int = 0
    coverage_rate: float = 0.0
    active_doctors: int = 0
    total_extras: int = 0
    pending_extras: int = 0
    approved_extras: int = 0
    open_periods: int = 0
    total_hours: float = 0.0
    doctors_per_shift: float = 0.0
    utilization_rate: float = 0.0

    def to_dict(self) -> dict:
        return {
            "total_shifts": self.total_shifts,
            "assigned_shifts": self.assigned_shifts,
            "unassigned_shifts": self.unassigned_shifts,
            "coverage_rate": self.coverage_rate,
            "active_doctors": self.active_doctors,
            "total_extras": self.total_extras,
            "pending_extras": self.pending_extras,
            "approved_extras": self.approved_extras,
            "open_periods": self.open_periods,
            "total_hours": self.total_hours,
            "doctors_per_shift": self.doctors_per_shift,
            "utilization_rate": self.utilization_rate,
        }


@dataclass(frozen=True)
class ActivitySummary:
    """Immutable activity entry for the recent activities feed."""
    activity_id: str
    entity_type: str
    entity_id: int
    event_type: str
    description: str
    performed_by: str = ""
    timestamp: str = ""
    icon: str = ""
    color: str = "info"

    def to_dict(self) -> dict:
        return {
            "activity_id": self.activity_id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "event_type": self.event_type,
            "description": self.description,
            "performed_by": self.performed_by,
            "timestamp": self.timestamp,
            "icon": self.icon,
            "color": self.color,
        }


@dataclass(frozen=True)
class OperationalAlertSummary:
    """Immutable operational alert for dashboard display."""
    alert_id: str
    severity: str  # low | medium | high | critical
    category: str  # coverage | staffing | extras | period
    title: str
    description: str
    entity_type: str = ""
    entity_id: int = 0
    action_route: str = ""
    created_at: str = ""
    icon: str = ""
    color: str = "warning"

    def to_dict(self) -> dict:
        return {
            "alert_id": self.alert_id,
            "severity": self.severity,
            "category": self.category,
            "title": self.title,
            "description": self.description,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "action_route": self.action_route,
            "created_at": self.created_at,
            "icon": self.icon,
            "color": self.color,
        }


@dataclass(frozen=True)
class UpcomingActionSummary:
    """Immutable upcoming action for dashboard display."""
    action_id: str
    entity_type: str
    entity_id: int
    title: str
    description: str
    priority: str  # low | medium | high
    due_date: str = ""
    action_route: str = ""
    icon: str = ""

    def to_dict(self) -> dict:
        return {
            "action_id": self.action_id,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "due_date": self.due_date,
            "action_route": self.action_route,
            "icon": self.icon,
        }


@dataclass(frozen=True)
class DashboardSummary:
    """Immutable consolidated summary for the operational dashboard.

    Aggregates all dashboard data into a single read model.
    Returned by DashboardService and consumed by the frontend.
    """
    current_period: CurrentPeriodSummary | None = None
    health_cards: list[HealthCardSummary] = field(default_factory=list)
    kpis: OperationalKPISummary = OperationalKPISummary()
    recent_activities: list[ActivitySummary] = field(default_factory=list)
    operational_alerts: list[OperationalAlertSummary] = field(default_factory=list)
    upcoming_actions: list[UpcomingActionSummary] = field(default_factory=list)
    generated_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "current_period": self.current_period.to_dict() if self.current_period else None,
            "health_cards": [hc.to_dict() for hc in self.health_cards],
            "kpis": self.kpis.to_dict(),
            "recent_activities": [a.to_dict() for a in self.recent_activities],
            "operational_alerts": [a.to_dict() for a in self.operational_alerts],
            "upcoming_actions": [a.to_dict() for a in self.upcoming_actions],
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }
