"""TimelineQuery — Business question about entity timeline."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TimelineQuery:
    """Represents a business question about the timeline of an entity.

    Supports filtering by entity, event type, date range, and pagination.
    """
    entity_type: str = ""
    entity_id: int | None = None
    start_date: str | None = None
    end_date: str | None = None
    from_date: str | None = None
    to_date: str | None = None
    event_type: str | None = None
    include_events: bool = True
    include_status_changes: bool = True
    include_audit: bool = False
    include_version_changes: bool = False
    event_types: list[str] = field(default_factory=list)
    limit: int = 50
    offset: int = 0
    sort_by: str = "timestamp"
    sort_direction: str = "asc"

    def to_dict(self) -> dict:
        return {
            "entity_type": self.entity_type,
            "entity_id": self.entity_id,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "event_type": self.event_type,
            "include_events": self.include_events,
            "include_status_changes": self.include_status_changes,
            "include_audit": self.include_audit,
            "include_version_changes": self.include_version_changes,
            "event_types": self.event_types,
            "limit": self.limit,
            "offset": self.offset,
            "sort_by": self.sort_by,
            "sort_direction": self.sort_direction,
        }
