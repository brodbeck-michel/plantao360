"""DTO de response para logs de auditoria."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel


class AuditLogResponseDTO(BaseModel):
    """Resposta serializada de um registro de auditoria."""

    id: int
    occurred_at: datetime
    user_id: Optional[int] = None
    user_label: str
    user_role: str
    origin: str
    action: str
    resource: str
    resource_id: Optional[int] = None
    period_id: Optional[int] = None
    before: Optional[dict[str, Any]] = None
    after: Optional[dict[str, Any]] = None
    summary: Optional[str] = None
    correlation_id: Optional[str] = None

    class Config:
        from_attributes = True
