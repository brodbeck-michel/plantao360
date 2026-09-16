"""RQE indicator routes — Read-only endpoint do indicador de horas por RQE."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.api_response import ApiResponse
from app.core.security.dependencies import get_current_user
from app.database.session import get_db
from app.services.rqe_indicator_service import RqeIndicatorService

router = APIRouter(
    prefix="/indicators",
    tags=["Indicadores"],
    dependencies=[Depends(get_current_user)],
)


@router.get(
    "/rqe-hours",
    summary="Horas de plantão cobertas por médicos com RQE",
    description="""Percentual de **horas** de plantão da competência cobertas por
médicos com RQE.

Não confundir com o `rqe_stats` do dashboard, que conta **médicos**. Aqui a métrica é
ponderada por hora trabalhada.

**Regras de cálculo:**
- Horas = partes de plantão (exceto `cancelled`) + extras com status `approved`.
- RQE é a fotografia atual do cadastro do médico, sem historização.
- Base completa da competência, sem truncamento.

**Parâmetros opcionais:**
- `period_id` — ID da competência
- `year_month` — Competência no formato YYYY-MM

Sem nenhum dos dois, usa a competência mais recente ainda não paga.""",
    response_description="Indicador consolidado de horas por RQE",
    responses={
        200: {"description": "Indicador retornado com sucesso"},
    },
)
def get_rqe_hours_indicator(
    period_id: int | None = Query(None, description="ID da competência"),
    year_month: str | None = Query(None, description="Competência (YYYY-MM)"),
    db: Session = Depends(get_db),
):
    service = RqeIndicatorService(db)
    result = service.execute(period_id=period_id, year_month=year_month)

    return ApiResponse.ok(data=result.to_dict())
