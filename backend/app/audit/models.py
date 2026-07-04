"""Audit models - contratos para implementação futura."""

from datetime import datetime
from typing import Any

from app.common.types import UUIDStr, AuditID
from app.common.identifiers import generate_uuid_str


# TODO: Implementar com SQLAlchemy
class AuditLog:
    """Modelo base para logs de auditoria."""

    audit_id: AuditID
    id: int
    timestamp: datetime
    user_id: str | None
    action: str
    resource: str
    resource_id: str | None
    details: dict[str, Any] | None
    ip_address: str | None
    correlation_id: UUIDStr | None

    def __init__(
        self,
        action: str,
        resource: str,
        user_id: str | None = None,
        resource_id: str | None = None,
        details: dict[str, Any] | None = None,
        ip_address: str | None = None,
        correlation_id: UUIDStr | None = None,
    ):
        self.audit_id = generate_uuid_str()
        self.timestamp = datetime.utcnow()
        self.action = action
        self.resource = resource
        self.user_id = user_id
        self.resource_id = resource_id
        self.details = details
        self.ip_address = ip_address
        self.correlation_id = correlation_id
