"""Dashboard API routes — Read-only endpoint for the operational dashboard."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.dashboard_service import DashboardService
from app.domain.query.dashboard_query import DashboardQuery
from app.common.api_response import ApiResponse
from app.core.security.dependencies import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"], dependencies=[Depends(get_current_user)])


@router.get(
    "",
    summary="Dashboard operacional",
    description="""Retorna dados consolidados para o dashboard operacional.

**Inclui:**
- Competência atual
- Health Cards (Cobertura, Pessoal, Extras, Competência)
- KPIs operacionais
- Últimas atividades
- Alertas operacionais
- Próximas ações

**Parâmetros opcionais:**
- `period_id` — ID de período específico
- `year_month` — Competência no formato YYYY-MM
- `organization_id` — ID da organização (futuro multi-unit)
- `sector_id` — ID do setor (futuro setorial)
- `doctor_id` — ID do médico (dashboard individual)
- `include_health_cards` — Incluir health cards (default: true)
- `include_kpis` — Incluir KPIs (default: true)
- `include_recent_activities` — Incluir atividades recentes (default: true)
- `include_operational_alerts` — Incluir alertas (default: true)
- `include_upcoming_actions` — Incluir próximas ações (default: true)
- `activity_limit` — Limite de atividades (default: 10)
- `alert_limit` — Limite de alertas (default: 20)""",
    response_description="Dashboard consolidado",
    responses={
        200: {"description": "Dashboard retornado com sucesso"},
    },
)
def get_operational_dashboard(
    period_id: int | None = Query(None, description="ID do período"),
    year_month: str | None = Query(None, description="Competência (YYYY-MM)"),
    organization_id: int | None = Query(None, description="ID da organização (futuro)"),
    sector_id: int | None = Query(None, description="ID do setor (futuro)"),
    doctor_id: int | None = Query(None, description="ID do médico (futuro)"),
    include_health_cards: bool = Query(True, description="Incluir health cards"),
    include_kpis: bool = Query(True, description="Incluir KPIs"),
    include_recent_activities: bool = Query(True, description="Incluir atividades recentes"),
    include_operational_alerts: bool = Query(True, description="Incluir alertas operacionais"),
    include_upcoming_actions: bool = Query(True, description="Incluir próximas ações"),
    activity_limit: int = Query(10, ge=1, le=50, description="Limite de atividades"),
    alert_limit: int = Query(20, ge=1, le=50, description="Limite de alertas"),
    db: Session = Depends(get_db),
):
    query = DashboardQuery(
        period_id=period_id,
        year_month=year_month,
        organization_id=organization_id,
        sector_id=sector_id,
        doctor_id=doctor_id,
        include_health_cards=include_health_cards,
        include_kpis=include_kpis,
        include_recent_activities=include_recent_activities,
        include_operational_alerts=include_operational_alerts,
        include_upcoming_actions=include_upcoming_actions,
        activity_limit=activity_limit,
        alert_limit=alert_limit,
    )

    service = DashboardService(db)
    result = service.execute(query)

    return ApiResponse.ok(data=result.to_dict())
