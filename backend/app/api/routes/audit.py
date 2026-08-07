"""Rotas de auditoria — consulta da trilha (somente-leitura, ADMIN/COORDENADOR apenas)."""

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.audit_service import AuditService
from app.schemas.audit import AuditLogResponseDTO, AuditFilterDTO
from app.common.api_response import ApiResponse
from app.common.openapi import standard_responses
from app.core.security.dependencies import require_role

router = APIRouter(prefix="/audit", tags=["Audit"], dependencies=[Depends(require_role("ADMIN", "COORDENADOR"))])


@router.get("", responses=standard_responses)
def query_audit_logs(
    response: Response,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    user_id: int | None = Query(None),
    resource: str | None = Query(None),
    resource_id: int | None = Query(None),
    period_id: int | None = Query(None),
    start_date: str | None = Query(None),
    end_date: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """
    Consulta a trilha de auditoria com filtros e paginação.

    Retorna registros ordenados por data (mais recentes primeiro).
    Acesso restrito a ADMIN e COORDENADOR (FR-006).

    **Filtros opcionais**:
    - `user_id`: autor da ação
    - `resource`: tipo de recurso (assignment, shift_extra, doctor, user, period)
    - `resource_id`: id do recurso específico
    - `period_id`: competência relacionada
    - `start_date`: filtrar eventos a partir desta data (ISO 8601)
    - `end_date`: filtrar eventos até esta data (ISO 8601)

    **Paginação**:
    - `page`: número da página (1-based)
    - `size`: itens por página (max 100)
    """
    from datetime import datetime

    filter_dto = AuditFilterDTO(
        page=page,
        size=size,
        user_id=user_id,
        resource=resource,
        resource_id=resource_id,
        period_id=period_id,
        start_date=datetime.fromisoformat(start_date) if start_date else None,
        end_date=datetime.fromisoformat(end_date) if end_date else None,
    )

    audit_service = AuditService(db)
    page_result = audit_service.query_audit_logs(
        user_id=filter_dto.user_id,
        resource=filter_dto.resource,
        resource_id=filter_dto.resource_id,
        period_id=filter_dto.period_id,
        start_date=filter_dto.start_date,
        end_date=filter_dto.end_date,
        page=filter_dto.page,
        size=filter_dto.size,
    )

    response.headers["X-Total-Count"] = str(page_result.total)
    response.headers["X-Page"] = str(page_result.page)
    response.headers["X-Page-Size"] = str(page_result.size)
    response.headers["X-Total-Pages"] = str(page_result.pages)

    dtos = [AuditLogResponseDTO.model_validate(log) for log in page_result.items]
    return ApiResponse.ok(data=[dto.model_dump() for dto in dtos], meta={"total": page_result.total})
