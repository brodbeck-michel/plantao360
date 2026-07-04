from dataclasses import dataclass, field
from datetime import datetime

from app.domain.constants.period_status import PeriodStatus
from app.domain.events.event_names import DomainEventName


@dataclass(frozen=True)
class PeriodTransition:
    period_id: int
    previous_status: PeriodStatus
    new_status: PeriodStatus
    user: str
    timestamp: datetime
    reason: str = ""
    event_name: DomainEventName | None = None

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "previous_status": self.previous_status,
            "new_status": self.new_status,
            "user": self.user,
            "timestamp": self.timestamp.isoformat(),
            "reason": self.reason,
            "event_name": self.event_name,
        }
