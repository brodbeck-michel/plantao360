"""Query API routes — Read-only endpoints for the query domain."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.query_service import QueryService
from app.domain.query.doctor_analytics_query import DoctorAnalyticsQuery
from app.domain.query.coverage_analytics_query import CoverageAnalyticsQuery
from app.domain.query.financial_analytics_query import FinancialAnalyticsQuery
from app.domain.query.payroll_analytics_query import PayrollAnalyticsQuery
from app.domain.query.timeline_query import TimelineQuery
from app.common.api_response import ApiResponse

router = APIRouter(prefix="/query", tags=["Query Domain"])


@router.get("/doctors")
def query_doctors(
    doctor_id: int | None = Query(None),
    active_only: bool = Query(True),
    period_id: int | None = Query(None),
    year_month: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """Query doctor analytics."""
    query = DoctorAnalyticsQuery(
        doctor_id=doctor_id,
        active_only=active_only,
        period_id=period_id,
        year_month=year_month,
    )
    service = QueryService(db)
    results = service.execute_doctor_query(query)
    return ApiResponse.ok(data=[r.to_dict() for r in results])


@router.get("/coverage")
def query_coverage(
    period_id: int | None = Query(None),
    year_month: str | None = Query(None),
    shift_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """Query coverage analytics."""
    query = CoverageAnalyticsQuery(
        period_id=period_id,
        year_month=year_month,
        shift_type=shift_type,
    )
    service = QueryService(db)
    result = service.execute_coverage_query(query)
    return ApiResponse.ok(data=result.to_dict())


@router.get("/financial")
def query_financial(
    period_id: int | None = Query(None),
    year_month: str | None = Query(None),
    doctor_id: int | None = Query(None),
    fact_type: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """Query financial analytics."""
    query = FinancialAnalyticsQuery(
        period_id=period_id,
        year_month=year_month,
        doctor_id=doctor_id,
        fact_type=fact_type,
    )
    service = QueryService(db)
    result = service.execute_financial_query(query)
    return ApiResponse.ok(data=result.to_dict())


@router.get("/payroll")
def query_payroll(
    payroll_id: int | None = Query(None),
    period_id: int | None = Query(None),
    year_month: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """Query payroll analytics."""
    query = PayrollAnalyticsQuery(
        payroll_id=payroll_id,
        period_id=period_id,
        year_month=year_month,
        status=status,
    )
    service = QueryService(db)
    result = service.execute_payroll_query(query)
    if isinstance(result, list):
        return ApiResponse.ok(data=[r.to_dict() for r in result])
    return ApiResponse.ok(data=result.to_dict())


@router.get("/timeline")
def query_timeline(
    entity_type: str = Query(...),
    entity_id: int | None = Query(None),
    start_date: str | None = Query(None),
    end_date: str | None = Query(None),
    from_date: str | None = Query(None, description="Data inicial (YYYY-MM-DD)"),
    to_date: str | None = Query(None, description="Data final (YYYY-MM-DD)"),
    event_type: str | None = Query(None, description="Filtrar por tipo de evento"),
    limit: int = Query(50, ge=1, le=200, description="Limite de resultados"),
    offset: int = Query(0, ge=0, description="Offset para paginação"),
    db: Session = Depends(get_db),
):
    """Query entity timeline.

    Suporta filtros por:
    - entity_type + entity_id (timeline de entidade específica)
    - from_date + to_date (intervalo de tempo)
    - event_type (tipo de evento específico)
    - limit + offset (paginação)
    """
    query = TimelineQuery(
        entity_type=entity_type,
        entity_id=entity_id,
        start_date=start_date,
        end_date=end_date,
        from_date=from_date,
        to_date=to_date,
        event_type=event_type,
        limit=limit,
        offset=offset,
    )
    service = QueryService(db)
    result = service.execute_timeline_query(query)
    return ApiResponse.ok(data=result.to_dict())


@router.get("/explain/remuneration")
def explain_remuneration(
    doctor_id: int = Query(...),
    period_id: int = Query(...),
    year_month: str = Query(...),
    db: Session = Depends(get_db),
):
    """Explain why a doctor received a specific remuneration."""
    service = QueryService(db)
    result = service.explain_remuneration(doctor_id, period_id, year_month)
    return ApiResponse.ok(data=result.to_dict())


@router.get("/explain/extra-rejection")
def explain_extra_rejection(
    extra_id: int = Query(...),
    period_id: int = Query(...),
    db: Session = Depends(get_db),
):
    """Explain why an extra was rejected."""
    service = QueryService(db)
    result = service.explain_extra_rejection(extra_id, period_id)
    return ApiResponse.ok(data=result.to_dict())


@router.get("/explain/competency-reopen")
def explain_competency_reopen(
    payroll_id: int = Query(...),
    year_month: str = Query(...),
    db: Session = Depends(get_db),
):
    """Explain why a competency was reopened."""
    service = QueryService(db)
    result = service.explain_competency_reopen(payroll_id, year_month)
    return ApiResponse.ok(data=result.to_dict())


@router.get("/audit")
def get_audit_analytics(
    year_month: str | None = Query(None),
    db: Session = Depends(get_db),
):
    """Get audit analytics."""
    service = QueryService(db)
    result = service.get_audit_analytics(year_month)
    return ApiResponse.ok(data=result.to_dict())


@router.get("/kpi/coverage")
def get_coverage_kpi(
    period_id: int = Query(...),
    year_month: str = Query(...),
    db: Session = Depends(get_db),
):
    """Get coverage KPI."""
    service = QueryService(db)
    result = service.get_coverage_kpi(period_id, year_month)
    return ApiResponse.ok(data=result.to_dict())


@router.get("/kpi/financial")
def get_financial_kpi(
    period_id: int = Query(...),
    year_month: str = Query(...),
    db: Session = Depends(get_db),
):
    """Get financial KPI."""
    service = QueryService(db)
    result = service.get_financial_kpi(period_id, year_month)
    return ApiResponse.ok(data=result.to_dict())


@router.get("/kpi/payroll")
def get_payroll_kpi(
    period_id: int = Query(...),
    year_month: str = Query(...),
    db: Session = Depends(get_db),
):
    """Get payroll KPI."""
    service = QueryService(db)
    result = service.get_payroll_kpi(period_id, year_month)
    return ApiResponse.ok(data=result.to_dict())


@router.get("/kpi/operational")
def get_operational_kpi(
    period_id: int = Query(...),
    year_month: str = Query(...),
    db: Session = Depends(get_db),
):
    """Get operational KPI."""
    service = QueryService(db)
    result = service.get_operational_kpi(period_id, year_month)
    return ApiResponse.ok(data=result.to_dict())
