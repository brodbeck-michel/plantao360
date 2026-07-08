from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.models.shift import Shift
from app.domain.constants.shift_status import ShiftStatus
from app.events.event_dispatcher import EventDispatcher, Event
from app.domain.events.event_names import DomainEventName
from app.core.logging import get_logger

logger = get_logger("service.shift.lifecycle")

event_dispatcher = EventDispatcher()


class ShiftLifecycleService:
    """Evaluates and persists automatic status transitions for shifts.

    Called on-demand during queries. No background workers, no cron.
    Only two transitions are allowed:
      - SCHEDULED  -> IN_PROGRESS  (now >= scheduled_start)
      - IN_PROGRESS -> COMPLETED   (now >= scheduled_end)

    DRAFT and CANCELLED are never modified automatically.
    """

    def __init__(self, db: Session):
        self.db = db

    def refresh_status(self, shift: Shift) -> bool:
        """Evaluate a single shift and persist if status changed. Returns True if changed."""
        if shift.status not in (ShiftStatus.SCHEDULED, ShiftStatus.IN_PROGRESS):
            return False

        now = datetime.now(timezone.utc)

        if shift.status == ShiftStatus.SCHEDULED:
            if self._parse_utc(shift.scheduled_start) is not None and now >= self._parse_utc(shift.scheduled_start):
                shift.status = ShiftStatus.IN_PROGRESS
                self.db.flush()
                event_dispatcher.dispatch(Event(
                    name=DomainEventName.SHIFT_STARTED_AUTOMATICALLY_V1,
                    data={"shift_id": shift.id},
                ))
                logger.info(
                    "shift.started.automatically",
                    extra={"shift_id": shift.id},
                )
                return True

        if shift.status == ShiftStatus.IN_PROGRESS:
            if self._parse_utc(shift.scheduled_end) is not None and now >= self._parse_utc(shift.scheduled_end):
                shift.status = ShiftStatus.COMPLETED
                self.db.flush()
                event_dispatcher.dispatch(Event(
                    name=DomainEventName.SHIFT_COMPLETED_AUTOMATICALLY_V1,
                    data={"shift_id": shift.id},
                ))
                logger.info(
                    "shift.completed.automatically",
                    extra={"shift_id": shift.id},
                )
                return True

        return False

    def refresh_statuses(self, shifts: list[Shift]) -> int:
        """Refresh a batch of shifts. Returns count of changes."""
        count = 0
        for shift in shifts:
            if self.refresh_status(shift):
                count += 1
        if count > 0:
            self.db.flush()
        return count

    def refresh_period(self, period_id: int) -> int:
        """Refresh all active shifts in a period. Returns count of changes."""
        shifts = self.db.query(Shift).filter(
            Shift.period_id == period_id,
            Shift.status.in_([ShiftStatus.SCHEDULED, ShiftStatus.IN_PROGRESS]),
        ).all()
        return self.refresh_statuses(shifts)

    @staticmethod
    def _parse_utc(value: Optional[datetime]) -> Optional[datetime]:
        """Ensure a datetime is timezone-aware (UTC)."""
        if value is None:
            return None
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value
