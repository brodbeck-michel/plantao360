from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.common.identifiers import generate_uuid_str
from app.common.types import EventID, CorrelationID


@dataclass
class DomainEvent:
    event_id: EventID = field(default_factory=generate_uuid_str)
    event_name: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    correlation_id: CorrelationID | None = None
