"""DashboardService — Aggregates data for the operational dashboard."""

from dataclasses import dataclass, field
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import func, and_

from app.models.period import Period
from app.models.shift import Shift
from app.models.doctor import Doctor
from app.models.shift_part import ShiftPart
from app.models.shift_extra import ShiftExtra
from app.domain.constants.period_status import PeriodStatus
from app.domain.constants.shift_status import ShiftStatus
from app.domain.constants.extra_status import ExtraStatus
from app.domain.query.dashboard_query import DashboardQuery
from app.domain.read_models.dashboard_summary import (
    DashboardSummary,
    CurrentPeriodSummary,
    HealthCardSummary,
    OperationalKPISummary,
    ActivitySummary,
    OperationalAlertSummary,
    UpcomingActionSummary,
)
from app.core.logging import get_logger

logger = get_logger("service.dashboard")

MONTH_NAMES = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}


# DashboardProjection — antes em domain/projections (consumidor único: este service).
# Inlinada aqui no colapso da domain/ (spec 004, Grupo B).
@dataclass(frozen=True)
class DashboardProjection:
    """Projects operational dashboard data from all aggregates without modifying them.

    Consumes data from Period, Shift, Doctor, ShiftPart, ShiftExtra aggregates
    to create a consolidated view optimized for the operational dashboard.
    """
    # Current period
    period_id: int = 0
    period_year: int = 0
    period_month: int = 0
    period_name: str = ""
    period_status: str = ""
    period_start_date: str = ""
    period_end_date: str = ""

    # Shifts
    total_shifts: int = 0
    assigned_shifts: int = 0
    unassigned_shifts: int = 0
    scheduled_shifts: int = 0
    in_progress_shifts: int = 0
    completed_shifts: int = 0
    cancelled_shifts: int = 0

    # Doctors
    total_doctors: int = 0
    active_doctors: int = 0
    doctors_with_shifts: int = 0
    doctors_without_shifts: int = 0

    # Coverage
    coverage_rate: float = 0.0
    total_duration_minutes: int = 0
    total_duration_hours: float = 0.0

    # Extras
    total_extras: int = 0
    pending_extras: int = 0
    approved_extras: int = 0
    rejected_extras: int = 0

    # Periods
    open_periods: int = 0
    closed_periods: int = 0

    # Computed
    doctors_per_shift: float = 0.0
    utilization_rate: float = 0.0

    projected_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "period_year": self.period_year,
            "period_month": self.period_month,
            "period_name": self.period_name,
            "period_status": self.period_status,
            "period_start_date": self.period_start_date,
            "period_end_date": self.period_end_date,
            "total_shifts": self.total_shifts,
            "assigned_shifts": self.assigned_shifts,
            "unassigned_shifts": self.unassigned_shifts,
            "scheduled_shifts": self.scheduled_shifts,
            "in_progress_shifts": self.in_progress_shifts,
            "completed_shifts": self.completed_shifts,
            "cancelled_shifts": self.cancelled_shifts,
            "total_doctors": self.total_doctors,
            "active_doctors": self.active_doctors,
            "doctors_with_shifts": self.doctors_with_shifts,
            "doctors_without_shifts": self.doctors_without_shifts,
            "coverage_rate": self.coverage_rate,
            "total_duration_minutes": self.total_duration_minutes,
            "total_duration_hours": self.total_duration_hours,
            "total_extras": self.total_extras,
            "pending_extras": self.pending_extras,
            "approved_extras": self.approved_extras,
            "rejected_extras": self.rejected_extras,
            "open_periods": self.open_periods,
            "closed_periods": self.closed_periods,
            "doctors_per_shift": self.doctors_per_shift,
            "utilization_rate": self.utilization_rate,
            "projected_at": self.projected_at.isoformat() if self.projected_at else None,
        }


class DashboardService:
    """Read-only service for the operational dashboard.

    Follows the Query Domain pattern:
    Route -> DashboardService -> DashboardProjection -> Repositories -> DashboardSummary
    """

    def __init__(self, session: Session):
        self._session = session

    def execute(self, query: DashboardQuery) -> DashboardSummary:
        """Execute a dashboard query and return consolidated summary."""
        projection = self._build_projection(query)
        health_cards = self._build_health_cards(projection, query)
        kpis = self._build_kpis(projection)
        recent_activities = self._build_recent_activities(query)
        operational_alerts = self._build_operational_alerts(projection, query)
        upcoming_actions = self._build_upcoming_actions(projection, query)

        return DashboardSummary(
            current_period=self._build_current_period(projection),
            health_cards=health_cards,
            kpis=kpis,
            recent_activities=recent_activities,
            operational_alerts=operational_alerts,
            upcoming_actions=upcoming_actions,
            generated_at=datetime.utcnow(),
        )

    def _build_projection(self, query: DashboardQuery) -> DashboardProjection:
        """Build the dashboard projection from database queries."""
        # Current period
        current_period = self._get_current_period(query)

        # Shifts
        total_shifts = 0
        assigned_shifts = 0
        unassigned_shifts = 0
        scheduled_shifts = 0
        in_progress_shifts = 0
        completed_shifts = 0
        cancelled_shifts = 0

        if current_period:
            from app.services.shift_lifecycle_service import ShiftLifecycleService
            lifecycle = ShiftLifecycleService(self._session)
            lifecycle.refresh_period(current_period.id)

            total_shifts = (
                self._session.query(func.count(Shift.id))
                .filter(Shift.period_id == current_period.id)
                .scalar()
            )

            # Assigned shifts = shifts with at least one shift_part
            assigned_shifts = (
                self._session.query(func.count(func.distinct(ShiftPart.shift_id)))
                .join(Shift, Shift.id == ShiftPart.shift_id)
                .filter(Shift.period_id == current_period.id)
                .scalar()
            )

            unassigned_shifts = total_shifts - assigned_shifts

            # Shift status counts
            shift_status_counts = (
                self._session.query(Shift.status, func.count(Shift.id))
                .filter(Shift.period_id == current_period.id)
                .group_by(Shift.status)
                .all()
            )
            status_map = dict(shift_status_counts)
            scheduled_shifts = status_map.get(ShiftStatus.SCHEDULED, 0)
            in_progress_shifts = status_map.get(ShiftStatus.IN_PROGRESS, 0)
            completed_shifts = status_map.get(ShiftStatus.COMPLETED, 0)
            cancelled_shifts = status_map.get(ShiftStatus.CANCELLED, 0)

        # Doctors
        total_doctors = self._session.query(func.count(Doctor.id)).scalar()
        active_doctors = (
            self._session.query(func.count(Doctor.id))
            .filter(Doctor.active == True)
            .scalar()
        )

        doctors_with_shifts = 0
        doctors_without_shifts = 0
        if current_period:
            doctors_with_shifts = (
                self._session.query(func.count(func.distinct(ShiftPart.doctor_id)))
                .join(Shift, Shift.id == ShiftPart.shift_id)
                .filter(Shift.period_id == current_period.id)
                .scalar()
            )
            doctors_without_shifts = max(0, active_doctors - doctors_with_shifts)

        # Coverage
        total_duration_minutes = 0
        total_duration_hours = 0.0
        coverage_rate = 0.0

        if current_period and total_shifts > 0:
            duration_result = (
                self._session.query(func.sum(ShiftPart.duration_minutes))
                .join(Shift, Shift.id == ShiftPart.shift_id)
                .filter(Shift.period_id == current_period.id)
                .scalar()
            )
            total_duration_minutes = duration_result or 0
            total_duration_hours = total_duration_minutes / 60.0
            coverage_rate = (assigned_shifts / total_shifts * 100) if total_shifts > 0 else 0.0

        # Extras
        total_extras = 0
        pending_extras = 0
        approved_extras = 0
        rejected_extras = 0

        if current_period:
            extras_counts = (
                self._session.query(ShiftExtra.status, func.count(ShiftExtra.id))
                .join(Shift, Shift.id == ShiftExtra.shift_id)
                .filter(Shift.period_id == current_period.id)
                .group_by(ShiftExtra.status)
                .all()
            )
            extras_map = dict(extras_counts)
            total_extras = sum(extras_map.values())
            pending_extras = extras_map.get(ExtraStatus.PENDING, 0)
            approved_extras = extras_map.get(ExtraStatus.APPROVED, 0)
            rejected_extras = extras_map.get(ExtraStatus.REJECTED, 0)

        # Periods
        open_periods = (
            self._session.query(func.count(Period.id))
            .filter(Period.status == PeriodStatus.DRAFT)
            .scalar()
        )
        closed_periods = (
            self._session.query(func.count(Period.id))
            .filter(Period.status == PeriodStatus.CLOSED)
            .scalar()
        )

        # Computed
        doctors_per_shift = (active_doctors / total_shifts) if total_shifts > 0 else 0.0
        utilization_rate = (assigned_shifts / (active_doctors * 2)) if active_doctors > 0 else 0.0

        return DashboardProjection(
            period_id=current_period.id if current_period else 0,
            period_year=current_period.year if current_period else 0,
            period_month=current_period.month if current_period else 0,
            period_name=self._get_period_name(current_period),
            period_status=current_period.status if current_period else "",
            total_shifts=total_shifts,
            assigned_shifts=assigned_shifts,
            unassigned_shifts=unassigned_shifts,
            scheduled_shifts=scheduled_shifts,
            in_progress_shifts=in_progress_shifts,
            completed_shifts=completed_shifts,
            cancelled_shifts=cancelled_shifts,
            total_doctors=total_doctors,
            active_doctors=active_doctors,
            doctors_with_shifts=doctors_with_shifts,
            doctors_without_shifts=doctors_without_shifts,
            coverage_rate=coverage_rate,
            total_duration_minutes=total_duration_minutes,
            total_duration_hours=total_duration_hours,
            total_extras=total_extras,
            pending_extras=pending_extras,
            approved_extras=approved_extras,
            rejected_extras=rejected_extras,
            open_periods=open_periods,
            closed_periods=closed_periods,
            doctors_per_shift=doctors_per_shift,
            utilization_rate=utilization_rate,
            projected_at=datetime.utcnow(),
        )

    def _get_current_period(self, query: DashboardQuery) -> Period | None:
        """Get the current active period."""
        if query.period_id:
            return (
                self._session.query(Period)
                .filter(Period.id == query.period_id)
                .first()
            )
        if query.year_month:
            parts = query.year_month.split("-")
            if len(parts) == 2:
                year, month = int(parts[0]), int(parts[1])
                return (
                    self._session.query(Period)
                    .filter(Period.year == year, Period.month == month)
                    .first()
                )
        # Default: most recent non-paid period
        return (
            self._session.query(Period)
            .filter(Period.status != PeriodStatus.PAID)
            .order_by(Period.year.desc(), Period.month.desc())
            .first()
        )

    def _get_period_name(self, period: Period | None) -> str:
        """Get formatted period name."""
        if not period:
            return "Nenhuma competência ativa"
        month_name = MONTH_NAMES.get(period.month, "")
        return f"{month_name}/{period.year}"

    def _build_current_period(self, projection: DashboardProjection) -> CurrentPeriodSummary | None:
        """Build the current period summary."""
        if projection.period_id == 0:
            return None
        return CurrentPeriodSummary(
            period_id=projection.period_id,
            year=projection.period_year,
            month=projection.period_month,
            name=projection.period_name,
            status=projection.period_status,
            total_shifts=projection.total_shifts,
            total_doctors=projection.active_doctors,
            total_hours=projection.total_duration_hours,
        )

    def _build_health_cards(
        self, projection: DashboardProjection, query: DashboardQuery
    ) -> list[HealthCardSummary]:
        """Build health cards based on operational status."""
        cards = []

        # Coverage card
        coverage_status = "healthy" if projection.coverage_rate >= 80 else "warning" if projection.coverage_rate >= 60 else "critical"
        coverage_severity = "low" if projection.coverage_rate >= 80 else "medium" if projection.coverage_rate >= 60 else "high"
        coverage_trend = f"+{projection.coverage_rate:.0f}%" if projection.coverage_rate >= 80 else f"{projection.coverage_rate:.0f}%"
        cards.append(HealthCardSummary(
            card_id="coverage",
            label="Cobertura",
            status=coverage_status,
            severity=coverage_severity,
            value=f"{projection.coverage_rate:.0f}%",
            detail=f"{projection.assigned_shifts}/{projection.total_shifts} plantões distribuídos",
            trend=coverage_trend,
            trend_direction="up" if projection.coverage_rate >= 80 else "down",
            icon="HealthAndSafety",
            action_route="/app/shifts",
        ))

        # Staffing card
        staffing_status = "healthy" if projection.active_doctors >= 20 else "warning" if projection.active_doctors >= 10 else "critical"
        staffing_severity = "low" if projection.active_doctors >= 20 else "medium" if projection.active_doctors >= 10 else "high"
        cards.append(HealthCardSummary(
            card_id="staffing",
            label="Pessoal",
            status=staffing_status,
            severity=staffing_severity,
            value=f"{projection.active_doctors} médicos",
            detail=f"{projection.doctors_with_shifts} alocados, {projection.doctors_without_shifts} disponíveis",
            trend="",
            trend_direction="flat",
            icon="People",
            action_route="/app/doctors",
        ))

        # Extras card
        extras_status = "healthy" if projection.pending_extras == 0 else "warning" if projection.pending_extras <= 5 else "critical"
        extras_severity = "low" if projection.pending_extras == 0 else "medium" if projection.pending_extras <= 5 else "high"
        cards.append(HealthCardSummary(
            card_id="extras",
            label="Extras",
            status=extras_status,
            severity=extras_severity,
            value=f"{projection.pending_extras} pendentes",
            detail=f"{projection.approved_extras} aprovados, {projection.rejected_extras} rejeitados",
            trend="",
            trend_direction="flat",
            icon="AddCircle",
            action_route="/app/extras",
        ))

        # Period card
        period_status = "healthy" if projection.period_status == "draft" else "info" if projection.period_status == "closed" else "default"
        period_severity = "low"
        cards.append(HealthCardSummary(
            card_id="period",
            label="Competência",
            status=period_status,
            severity=period_severity,
            value=projection.period_name,
            detail=f"Status: {projection.period_status} | {projection.open_periods} aberta(s)",
            trend="",
            trend_direction="flat",
            icon="CalendarMonth",
            action_route="/app/periods",
        ))

        return cards

    def _build_kpis(self, projection: DashboardProjection) -> OperationalKPISummary:
        """Build operational KPIs."""
        return OperationalKPISummary(
            total_shifts=projection.total_shifts,
            assigned_shifts=projection.assigned_shifts,
            unassigned_shifts=projection.unassigned_shifts,
            coverage_rate=projection.coverage_rate,
            active_doctors=projection.active_doctors,
            total_extras=projection.total_extras,
            pending_extras=projection.pending_extras,
            approved_extras=projection.approved_extras,
            open_periods=projection.open_periods,
            total_hours=projection.total_duration_hours,
            doctors_per_shift=projection.doctors_per_shift,
            utilization_rate=projection.utilization_rate,
        )

    def _build_recent_activities(self, query: DashboardQuery) -> list[ActivitySummary]:
        """Build recent activities from domain events."""
        activities = []

        # Recent shifts
        recent_shifts = (
            self._session.query(Shift)
            .order_by(Shift.created_at.desc())
            .limit(query.activity_limit)
            .all()
        )

        for shift in recent_shifts:
            month_name = MONTH_NAMES.get(shift.shift_date.month if hasattr(shift.shift_date, 'month') else 0, "")
            activities.append(ActivitySummary(
                activity_id=f"shift-{shift.id}",
                entity_type="shift",
                entity_id=shift.id,
                event_type="created",
                description=f"Plantão {shift.shift_type} do dia {shift.shift_date}",
                timestamp=shift.created_at.isoformat() if shift.created_at else "",
                icon="EventNote",
                color="info",
            ))

        # Recent doctors
        recent_doctors = (
            self._session.query(Doctor)
            .order_by(Doctor.created_at.desc())
            .limit(5)
            .all()
        )

        for doctor in recent_doctors:
            activities.append(ActivitySummary(
                activity_id=f"doctor-{doctor.id}",
                entity_type="doctor",
                entity_id=doctor.id,
                event_type="created",
                description=f"Médico {doctor.name} cadastrado",
                timestamp=doctor.created_at.isoformat() if doctor.created_at else "",
                icon="LocalHospital",
                color="success",
            ))

        # Sort by timestamp descending and limit
        activities.sort(key=lambda a: a.timestamp, reverse=True)
        return activities[:query.activity_limit]

    def _build_operational_alerts(
        self, projection: DashboardProjection, query: DashboardQuery
    ) -> list[OperationalAlertSummary]:
        """Build operational alerts based on current state."""
        alerts = []

        # Coverage alert
        if projection.coverage_rate < 80:
            severity = "high" if projection.coverage_rate < 60 else "medium"
            alerts.append(OperationalAlertSummary(
                alert_id="coverage-low",
                severity=severity,
                category="coverage",
                title="Cobertura abaixo do mínimo",
                description=f"Cobertura atual é {projection.coverage_rate:.0f}%. Mínimo recomendado: 80%.",
                action_route="/app/shifts",
                icon="Warning",
                color="warning",
            ))

        # Unassigned shifts alert
        if projection.unassigned_shifts > 0:
            severity = "high" if projection.unassigned_shifts > 20 else "medium"
            alerts.append(OperationalAlertSummary(
                alert_id="unassigned-shifts",
                severity=severity,
                category="staffing",
                title=f"{projection.unassigned_shifts} plantões sem médico",
                description="Existem plantões aguardando distribuição.",
                action_route="/app/assignments",
                icon="PersonAdd",
                color="warning",
            ))

        # Pending extras alert
        if projection.pending_extras > 0:
            severity = "medium" if projection.pending_extras <= 5 else "high"
            alerts.append(OperationalAlertSummary(
                alert_id="pending-extras",
                severity=severity,
                category="extras",
                title=f"{projection.pending_extras} extras pendentes",
                description="Extras aguardando aprovação.",
                action_route="/app/extras",
                icon="AddCircle",
                color="warning",
            ))

        # No current period alert
        if projection.period_id == 0:
            alerts.append(OperationalAlertSummary(
                alert_id="no-period",
                severity="high",
                category="period",
                title="Nenhuma competência ativa",
                description="Crie uma nova competência para iniciar o ciclo operacional.",
                action_route="/app/periods/new",
                icon="CalendarMonth",
                color="error",
            ))

        return alerts[:query.alert_limit]

    def _build_upcoming_actions(
        self, projection: DashboardProjection, query: DashboardQuery
    ) -> list[UpcomingActionSummary]:
        """Build upcoming actions based on current state."""
        actions = []

        if projection.unassigned_shifts > 0:
            actions.append(UpcomingActionSummary(
                action_id="distribute-shifts",
                entity_type="shift",
                entity_id=0,
                title="Distribuir plantões",
                description=f"{projection.unassigned_shifts} plantões aguardando distribuição",
                priority="high",
                action_route="/app/assignments",
                icon="PersonAdd",
            ))

        if projection.pending_extras > 0:
            actions.append(UpcomingActionSummary(
                action_id="review-extras",
                entity_type="extra",
                entity_id=0,
                title="Revisar extras",
                description=f"{projection.pending_extras} extras pendentes de aprovação",
                priority="medium",
                action_route="/app/extras",
                icon="AddCircle",
            ))

        if projection.period_status == "closed":
            actions.append(UpcomingActionSummary(
                action_id="process-payroll",
                entity_type="payroll",
                entity_id=0,
                title="Processar folha",
                description="Competência fechada, pronta para processamento financeiro",
                priority="medium",
                action_route="/app/payroll",
                icon="Receipt",
            ))

        return actions
