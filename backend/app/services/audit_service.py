"""Serviço de auditoria para registrar alterações nas entidades do domínio."""

from typing import Any, Optional
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.user import User
from app.core.logging import get_logger

logger = get_logger("service.audit")


class AuditService:
    """Registra alterações em entidades (create/update/delete) com autor, antes/depois e contexto."""

    # Campos explícitos que são gravados por recurso — FR-004 (nunca password_hash nem credenciais)
    AUDITED_FIELDS = {
        "assignment": ["shift_id", "shift_date", "shift_type", "doctor_id", "doctor_name", "start_time", "end_time", "status"],
        "shift_extra": ["shift_id", "shift_date", "doctor_id", "doctor_name", "duration_minutes", "justification", "status"],
        "doctor": ["name", "crm", "specialty", "doctor_type", "has_rqe", "career_start_date", "active"],
        "user": ["name", "email", "role", "active", "doctor_id"],
        "period": ["year", "month", "status"],
    }

    def __init__(self, session: Session):
        self.session = session

    def record(
        self,
        action: str,
        resource: str,
        user: Optional[User],
        resource_id: Optional[int] = None,
        before: Optional[dict[str, Any]] = None,
        after: Optional[dict[str, Any]] = None,
        period_id: Optional[int] = None,
        summary: Optional[str] = None,
        correlation_id: Optional[str] = None,
    ) -> AuditLog:
        """
        Registra uma alteração (create/update/delete) numa entidade.

        :param action: 'create' | 'update' | 'delete'
        :param resource: tipo de recurso ('assignment' | 'shift_extra' | 'doctor' | 'user' | 'period')
        :param user: usuário autenticado (None se origem='system')
        :param resource_id: id da entidade alterada
        :param before: estado anterior (None em create)
        :param after: estado resultante (None em delete)
        :param period_id: competência relacionada (quando aplicável)
        :param summary: descrição curta legível (ex.: "Removeu Maria Oliveira do T3 de 12/07")
        :param correlation_id: id de correlação da requisição (para ligar ao log estruturado)
        :return: AuditLog criado
        """
        # Determinação de origem e usuário
        if user:
            origin = "user"
            user_id = user.id
            user_label = user.email
            user_role = user.role
        else:
            origin = "system"
            user_id = None
            user_label = "system"
            user_role = "SYSTEM"

        # Garantir que before/after contêm apenas campos audáveis (FR-004)
        if before:
            before = self._filter_fields(resource, before)
        if after:
            after = self._filter_fields(resource, after)

        # Invariante 2-4: action define o estado de before/after
        if action == "create":
            before = None
        elif action == "delete":
            after = None

        audit_entry = AuditLog(
            occurred_at=datetime.now(timezone.utc),
            user_id=user_id,
            user_label=user_label,
            user_role=user_role,
            origin=origin,
            action=action,
            resource=resource,
            resource_id=resource_id,
            period_id=period_id,
            before=before,
            after=after,
            summary=summary,
            correlation_id=correlation_id,
        )

        self.session.add(audit_entry)
        logger.info(
            f"audit.{action}.v1",
            extra={
                "resource": resource,
                "resource_id": resource_id,
                "user_id": user_id,
                "user_label": user_label,
                "origin": origin,
            },
        )

        return audit_entry

    def record_many(
        self,
        entries: list[dict[str, Any]],
    ) -> list[AuditLog]:
        """
        Registra múltiplas alterações (ex.: duplicação de semana) numa única transação.
        Recebe uma lista de dicts com as mesmas chaves de `record()`.

        :param entries: lista de dicts, cada um com keys: action, resource, user, resource_id, before, after, period_id, summary, correlation_id
        :return: lista de AuditLog criados
        """
        audit_logs = []
        for entry_data in entries:
            audit_log = self.record(
                action=entry_data.get("action"),
                resource=entry_data.get("resource"),
                user=entry_data.get("user"),
                resource_id=entry_data.get("resource_id"),
                before=entry_data.get("before"),
                after=entry_data.get("after"),
                period_id=entry_data.get("period_id"),
                summary=entry_data.get("summary"),
                correlation_id=entry_data.get("correlation_id"),
            )
            audit_logs.append(audit_log)

        return audit_logs

    def _filter_fields(self, resource: str, data: dict[str, Any]) -> dict[str, Any]:
        """
        Remove campos não audáveis de before/after — FR-004.
        Retorna apenas os campos da lista explícita para o recurso.

        :param resource: tipo de recurso
        :param data: dict com potencialmente muitos campos
        :return: dict filtrado contendo apenas campos audáveis
        """
        allowed_fields = self.AUDITED_FIELDS.get(resource, [])
        return {k: v for k, v in data.items() if k in allowed_fields}

    def query_audit_logs(
        self,
        user_id: Optional[int] = None,
        resource: Optional[str] = None,
        resource_id: Optional[int] = None,
        period_id: Optional[int] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        page: int = 1,
        size: int = 20,
    ):
        """
        Consulta a trilha de auditoria com filtros e paginação.
        Ordenação: mais recente primeiro (occurred_at DESC).

        :param user_id: filtrar por autor
        :param resource: filtrar por tipo de recurso
        :param resource_id: filtrar por id do recurso
        :param period_id: filtrar por competência
        :param start_date: filtrar eventos a partir desta data (UTC)
        :param end_date: filtrar eventos até esta data (UTC)
        :param page: número da página (1-based)
        :param size: itens por página
        :return: Page com AuditLog e metadados
        """
        query = self.session.query(AuditLog)

        if user_id is not None:
            query = query.filter(AuditLog.user_id == user_id)
        if resource is not None:
            query = query.filter(AuditLog.resource == resource)
        if resource_id is not None:
            query = query.filter(AuditLog.resource_id == resource_id)
        if period_id is not None:
            query = query.filter(AuditLog.period_id == period_id)
        if start_date is not None:
            query = query.filter(AuditLog.occurred_at >= start_date)
        if end_date is not None:
            query = query.filter(AuditLog.occurred_at <= end_date)

        # Ordenação: mais recente primeiro
        query = query.order_by(AuditLog.occurred_at.desc())

        total = query.count()
        skip = (page - 1) * size
        items = query.offset(skip).limit(size).all()

        from app.common.pagination import Page

        return Page(items=items, page=page, size=size, total=total)
