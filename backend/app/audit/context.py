from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class AuditContext:
    user: str | None = None
    request_id: str | None = None
    correlation_id: str | None = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ip: str | None = None
    user_agent: str | None = None
