"""InstitutionTimeline — Global timeline for the institution."""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class TimelineEvent:
    """A single event in the institution timeline."""
    timestamp: str
    event_type: str
    entity_type: str
    entity_id: int
    description: str
    performed_by: str = ""
    previous_status: str = ""
    new_status: str = ""
    details: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "event_type": self.event_type,
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "description": self.description,
            "performed_by": self.performed_by,
            "previous_status": self.previous_status,
            "new_status": self.new_status,
            "details": self.details,
        }


@dataclass(frozen=True)
class InstitutionTimeline:
    """Global timeline reconstructing the complete chain of events.

    Reconstrói: Shift → Assignment → Extra → Coverage → Financial Facts →
    Remuneration → Payroll → Approval → Administrative Lock
    """
    entity_type: str = ""
    entity_id: int | None = None
    events: list[TimelineEvent] = field(default_factory=list)
    total_events: int = 0
    date_range: dict = field(default_factory=dict)
    generated_at: datetime | None = None

    @property
    def is_empty(self) -> bool:
        return len(self.events) == 0

    @property
    def event_types(self) -> list[str]:
        return list(set(e.event_type for e in self.events))

    def filter_by_type(self, event_type: str) -> list[TimelineEvent]:
        return [e for e in self.events if e.event_type == event_type]

    def filter_by_entity(self, entity_type: str) -> list[TimelineEvent]:
        return [e for e in self.events if e.entity_type == entity_type]

    def to_dict(self) -> dict:
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "events": [e.to_dict() for e in self.events],
            "total_events": self.total_events,
            "date_range": self.date_range,
            "event_types": self.event_types,
            "generated_at": self.generated_at.isoformat() if self.generated_at else None,
        }
