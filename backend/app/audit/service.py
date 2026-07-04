"""Audit service - contratos para implementação futura."""

from typing import Any

from app.audit.events import AuditAction


# TODO: Implementar service de auditoria
class AuditService:
    """Service para registro de eventos de auditoria."""

    def log(
        self,
        action: AuditAction,
        resource: str,
        user_id: str | None = None,
        resource_id: str | None = None,
        details: dict[str, Any] | None = None,
        ip_address: str | None = None,
        correlation_id: str | None = None,
    ) -> None:
        """Registra um evento de auditoria."""
        # TODO: Persistir no banco de dados
        # TODO: Enviar para fila de eventos (futuro)
        pass
