"""Coverage Service — Orchestrates coverage consolidation."""

from datetime import datetime

from app.database.unit_of_work import UnitOfWork
from app.models.period import Period
from app.models.shift import Shift
from app.models.coverage_snapshot import CoverageSnapshot
from app.models.financial_snapshot import FinancialSnapshot
from app.models.financial_fact import FinancialFact
from app.domain.coverage.coverage_engine import CoverageEngine
from app.domain.financial.financial_snapshot_builder import FinancialSnapshotBuilder
from app.domain.constants.snapshot_status import SnapshotStatus
from app.domain.constants.financial_fact_status import FinancialFactStatus
from app.repositories.coverage_snapshot_repository import CoverageSnapshotRepository
from app.repositories.financial_snapshot_repository import FinancialSnapshotRepository
from app.repositories.financial_fact_repository import FinancialFactRepository
from app.common.result import Success, Failure, Result
from app.events.event_dispatcher import EventDispatcher, Event
from app.domain.events.event_names import DomainEventName
from app.core.logging import get_logger

logger = get_logger("service.coverage")

event_dispatcher = EventDispatcher()


class CoverageService:
    """Orchestrates coverage consolidation for a period.

    Steps:
    1. Validate period is closable
    2. Collect all shifts in the period
    3. Execute CoverageEngine for each shift
    4. Build CoverageSnapshot
    5. Build FinancialSnapshot
    6. Persist all data
    7. Emit events
    """

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def consolidate(self, period_id: int) -> Result[dict]:
        """Consolidate coverage for a period.

        This is the main entry point for the Coverage Engine.
        """
        period = self.uow.session.query(Period).get(period_id)
        if not period:
            return Failure(
                error="Period not found",
                code="period.not_found",
            )

        if period.status != "draft":
            return Failure(
                error="Period must be in draft status to consolidate",
                code="period.not_draft",
            )

        shifts = (
            self.uow.session.query(Shift)
            .filter(Shift.period_id == period_id)
            .all()
        )

        if not shifts:
            return Failure(
                error="No shifts found for period",
                code="period.no_shifts",
            )

        engine = CoverageEngine()
        coverage_results = engine.consolidate_period(shifts)

        total_facts = sum(r.total_facts for r in coverage_results)
        total_duration = sum(r.total_duration_minutes for r in coverage_results)
        all_inconsistencies = []
        for r in coverage_results:
            all_inconsistencies.extend(r.inconsistencies)

        now = datetime.utcnow()

        coverage_snapshot = CoverageSnapshot(
            period_id=period_id,
            status=SnapshotStatus.ACTIVE,
            total_assignments_completed=total_facts,
            total_extras_approved=0,
            total_duration_minutes=total_duration,
            inconsistencies=(
                [{"type": i.inconsistency_type, "details": i.details}
                 for i in all_inconsistencies]
                if all_inconsistencies else None
            ),
            consolidated_at=now,
        )
        self.uow.session.add(coverage_snapshot)
        self.uow.session.flush()

        builder = FinancialSnapshotBuilder()
        snapshot_data = builder.build(
            period_id=period_id,
            coverage_snapshot_id=coverage_snapshot.id,
            coverage_results=coverage_results,
        )

        financial_snapshot = FinancialSnapshot(
            period_id=period_id,
            coverage_snapshot_id=coverage_snapshot.id,
            status=SnapshotStatus.ACTIVE,
            total_facts=snapshot_data.total_facts,
            total_duration_minutes=snapshot_data.total_duration_minutes,
            created_at_snapshot=now,
        )
        self.uow.session.add(financial_snapshot)
        self.uow.session.flush()

        for fact_data in snapshot_data.facts:
            fact = FinancialFact(
                period_id=fact_data.period_id,
                doctor_id=fact_data.doctor_id,
                fact_type=fact_data.fact_type,
                duration_minutes=fact_data.duration_minutes,
                source_event=fact_data.source_event,
                source_id=fact_data.source_id,
                status=FinancialFactStatus.ACTIVE,
            )
            self.uow.session.add(fact)

        self.uow.session.flush()

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.COVERAGE_CONSOLIDATED_V1,
                data={
                    "period_id": period_id,
                    "coverage_snapshot_id": coverage_snapshot.id,
                    "total_facts": total_facts,
                    "total_duration_minutes": total_duration,
                },
            )
        )

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.FINANCIAL_SNAPSHOT_CREATED_V1,
                data={
                    "period_id": period_id,
                    "financial_snapshot_id": financial_snapshot.id,
                    "total_facts": snapshot_data.total_facts,
                },
            )
        )

        logger.info(
            "coverage.consolidated.v1",
            extra={
                "period_id": period_id,
                "total_facts": total_facts,
                "total_duration_minutes": total_duration,
                "inconsistencies": len(all_inconsistencies),
            },
        )

        return Success(data={
            "period_id": period_id,
            "coverage_snapshot_id": coverage_snapshot.id,
            "financial_snapshot_id": financial_snapshot.id,
            "total_facts": total_facts,
            "total_duration_minutes": total_duration,
            "inconsistencies": len(all_inconsistencies),
        })

    def invalidate_snapshots(self, period_id: int) -> Result[bool]:
        """Invalidate all snapshots for a period (used during reopening)."""
        period = self.uow.session.query(Period).get(period_id)
        if not period:
            return Failure(
                error="Period not found",
                code="period.not_found",
            )

        coverage_snapshots = (
            self.uow.session.query(CoverageSnapshot)
            .filter(CoverageSnapshot.period_id == period_id)
            .all()
        )
        for cs in coverage_snapshots:
            cs.status = SnapshotStatus.INVALIDATED

        financial_snapshots = (
            self.uow.session.query(FinancialSnapshot)
            .filter(FinancialSnapshot.period_id == period_id)
            .all()
        )
        for fs in financial_snapshots:
            fs.status = SnapshotStatus.INVALIDATED

        facts = (
            self.uow.session.query(FinancialFact)
            .filter(FinancialFact.period_id == period_id)
            .all()
        )
        for fact in facts:
            fact.status = FinancialFactStatus.REVOKED
            fact.revoked_at = datetime.utcnow()
            fact.revoked_reason = "Period reopened"

        self.uow.session.flush()

        logger.info(
            "coverage.snapshots_invalidated",
            extra={"period_id": period_id},
        )

        return Success(data=True)
