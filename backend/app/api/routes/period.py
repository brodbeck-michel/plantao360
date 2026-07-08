from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.unit_of_work import UnitOfWork
from app.repositories.period_repository import PeriodRepository
from app.use_cases.periods import (
    CreatePeriod, UpdatePeriod, ClosePeriod, ReopenPeriod,
    GetPeriod, ListPeriods,
)
from app.schemas.period.period_create import PeriodCreateDTO
from app.schemas.period.period_update import PeriodUpdateDTO
from app.schemas.period.period_filters import PeriodFilterDTO
from app.common.api_response import ApiResponse
from app.common.openapi import standard_responses
from app.core.security.dependencies import get_current_user

router = APIRouter(prefix="/periods", tags=["Periods"], dependencies=[Depends(get_current_user)])


class PeriodErrorResponse(BaseModel):
    success: bool = False
    data: None = None
    meta: dict = Field(default_factory=dict)
    error: dict = Field(
        json_schema_extra={
            "example": {
                "code": "PERIOD_NOT_FOUND",
                "message": "Periodo nao encontrado",
                "details": None,
            }
        }
    )


class PeriodSuccessResponse(BaseModel):
    success: bool = True
    data: dict = Field(
        json_schema_extra={
            "example": {
                "id": 1,
                "year": 2026,
                "month": 6,
                "status": "draft",
                "created_at": "2026-06-26T10:00:00",
                "updated_at": "2026-06-26T10:00:00",
            }
        }
    )
    meta: dict = Field(default_factory=dict)


PERIOD_400_DESCRIPTION = """**Periodo ja existe** - Violacao de unicidade (year, month)."""

PERIOD_404_DESCRIPTION = """**Periodo nao encontrado**."""

PERIOD_409_DESCRIPTION = """**Conflito de transicao de estado**."""


@router.get("", responses=standard_responses)
def list_periods(
    response: Response,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    year: int | None = Query(None),
    month: int | None = Query(None),
    status: str | None = Query(None),
    sort_by: str = Query("id"),
    sort_direction: str = Query("asc"),
    db: Session = Depends(get_db),
):
    filter_dto = PeriodFilterDTO(
        page=page, size=size, year=year, month=month,
        status=status, sort_by=sort_by, sort_direction=sort_direction,
    )
    uow = UnitOfWork()
    uow._session = db
    repo = PeriodRepository(uow.session)
    use_case = ListPeriods(repo)
    result = use_case(filter_dto=filter_dto)

    page_data = result.data
    response.headers["X-Total-Count"] = str(page_data.total)
    response.headers["X-Page"] = str(page_data.page)
    response.headers["X-Page-Size"] = str(page_data.size)
    response.headers["X-Total-Pages"] = str(page_data.pages)

    return ApiResponse.ok(data=page_data.to_dict(), meta={"total": page_data.total})


@router.get("/{period_id}", responses=standard_responses)
def get_period(period_id: int, db: Session = Depends(get_db)):
    uow = UnitOfWork()
    uow._session = db
    repo = PeriodRepository(uow.session)
    use_case = GetPeriod(repo)
    result = use_case(id=period_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(code=result.code, message=result.error)
    return ApiResponse.ok(data=result.data.model_dump())


@router.post("", status_code=201, responses=standard_responses)
def create_period(dto: PeriodCreateDTO, db: Session = Depends(get_db)):
    uow = UnitOfWork()
    uow._session = db
    repo = PeriodRepository(uow.session)
    use_case = CreatePeriod(repo)
    result = use_case(dto=dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(code=result.code, message=result.error)
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{period_id}", responses=standard_responses)
def update_period(period_id: int, dto: PeriodUpdateDTO, db: Session = Depends(get_db)):
    uow = UnitOfWork()
    uow._session = db
    repo = PeriodRepository(uow.session)
    use_case = UpdatePeriod(repo)
    result = use_case(id=period_id, dto=dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(code=result.code, message=result.error)
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.delete("/{period_id}", responses=standard_responses)
def delete_period(period_id: int, db: Session = Depends(get_db)):
    from app.models.period import Period
    from app.domain.constants.period_status import PeriodStatus
    period = db.query(Period).filter(Period.id == period_id).first()
    if not period:
        return ApiResponse.fail_with_code(code="PERIOD_NOT_FOUND", message="Periodo nao encontrado")
    if period.status != PeriodStatus.DRAFT:
        return ApiResponse.fail_with_code(code="PERIOD_IMMUTABLE", message="Apenas periodos em rascunho podem ser excluidos")
    db.delete(period)
    db.commit()
    return ApiResponse.ok(data={"deleted": True})


@router.post("/{period_id}/close", responses=standard_responses)
def close_period(period_id: int, db: Session = Depends(get_db)):
    uow = UnitOfWork()
    uow._session = db
    repo = PeriodRepository(uow.session)
    use_case = ClosePeriod(repo)
    result = use_case(id=period_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(code=result.code, message=result.error)
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.post("/{period_id}/reopen", responses=standard_responses)
def reopen_period(period_id: int, db: Session = Depends(get_db)):
    uow = UnitOfWork()
    uow._session = db
    repo = PeriodRepository(uow.session)
    use_case = ReopenPeriod(repo)
    result = use_case(id=period_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(code=result.code, message=result.error)
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.post("/{period_id}/duplicate", responses=standard_responses)
def duplicate_period(period_id: int, db: Session = Depends(get_db)):
    from datetime import date as date_type
    from app.models.period import Period
    from app.models.shift import Shift
    from app.models.shift_part import ShiftPart
    from app.domain.constants.competency_dates import get_competency_dates
    period = db.query(Period).filter(Period.id == period_id).first()
    if not period:
        return ApiResponse.fail_with_code(code="PERIOD_NOT_FOUND", message="Periodo nao encontrado")

    new_month = period.month + 1 if period.month < 12 else 1
    new_year = period.year + 1 if period.month == 12 else period.year

    existing = db.query(Period).filter(Period.year == new_year, Period.month == new_month).first()
    if existing:
        return ApiResponse.fail_with_code(code="PERIOD_ALREADY_EXISTS", message=f"Periodo {new_year}/{new_month:02d} ja existe")

    new_period = Period(year=new_year, month=new_month, status="draft")
    db.add(new_period)
    db.flush()

    old_start, old_end = get_competency_dates(period.year, period.month)
    new_start, new_end = get_competency_dates(new_year, new_month)

    old_shifts = db.query(Shift).filter(
        Shift.period_id == period_id,
        Shift.shift_date >= old_start,
        Shift.shift_date <= old_end,
    ).all()
    old_shift_map = {}
    for old_shift in old_shifts:
        delta = old_shift.shift_date - old_start
        new_date = new_start + delta
        new_shift = Shift(
            period_id=new_period.id,
            shift_date=new_date,
            shift_type=old_shift.shift_type,
            status="draft",
            scheduled_start=old_shift.scheduled_start,
            scheduled_end=old_shift.scheduled_end,
            total_duration_minutes=old_shift.total_duration_minutes,
            doctor_count=old_shift.doctor_count,
        )
        db.add(new_shift)
        db.flush()
        old_shift_map[old_shift.id] = new_shift

    for old_shift in old_shifts:
        old_parts = db.query(ShiftPart).filter(ShiftPart.shift_id == old_shift.id).all()
        for part in old_parts:
            new_shift = old_shift_map.get(old_shift.id)
            if new_shift:
                new_part = ShiftPart(
                    shift_id=new_shift.id,
                    doctor_id=part.doctor_id,
                    start_time=part.start_time,
                    end_time=part.end_time,
                    status="planned",
                    duration_minutes=part.duration_minutes,
                )
                db.add(new_part)

    db.flush()
    db.commit()
    return ApiResponse.ok(data={"id": new_period.id, "year": new_period.year, "month": new_period.month, "status": new_period.status})


@router.post("/{period_id}/copy-from/{source_period_id}", responses=standard_responses)
def copy_from_period(period_id: int, source_period_id: int, db: Session = Depends(get_db)):
    from app.models.period import Period
    from app.models.shift import Shift
    from app.models.shift_part import ShiftPart
    from app.domain.constants.competency_dates import get_competency_dates
    period = db.query(Period).filter(Period.id == period_id).first()
    if not period:
        return ApiResponse.fail_with_code(code="PERIOD_NOT_FOUND", message="Periodo nao encontrado")
    source = db.query(Period).filter(Period.id == source_period_id).first()
    if not source:
        return ApiResponse.fail_with_code(code="PERIOD_NOT_FOUND", message="Periodo origem nao encontrado")

    src_start, src_end = get_competency_dates(source.year, source.month)
    tgt_start, tgt_end = get_competency_dates(period.year, period.month)

    source_shifts = db.query(Shift).filter(
        Shift.period_id == source_period_id,
        Shift.shift_date >= src_start,
        Shift.shift_date <= src_end,
    ).all()
    existing_shifts = db.query(Shift).filter(
        Shift.period_id == period_id,
        Shift.shift_date >= tgt_start,
        Shift.shift_date <= tgt_end,
    ).all()
    existing_keys = {(s.shift_date, s.shift_type) for s in existing_shifts}

    copied = 0
    for src_shift in source_shifts:
        if (src_shift.shift_date, src_shift.shift_type) not in existing_keys:
            new_shift = Shift(
                period_id=period_id,
                shift_date=src_shift.shift_date,
                shift_type=src_shift.shift_type,
                status="scheduled",
                scheduled_start=src_shift.scheduled_start,
                scheduled_end=src_shift.scheduled_end,
                total_duration_minutes=src_shift.total_duration_minutes,
                doctor_count=src_shift.doctor_count,
            )
            db.add(new_shift)
            db.flush()

            src_parts = db.query(ShiftPart).filter(ShiftPart.shift_id == src_shift.id).all()
            for part in src_parts:
                new_part = ShiftPart(
                    shift_id=new_shift.id,
                    doctor_id=part.doctor_id,
                    start_time=part.start_time,
                    end_time=part.end_time,
                    status="planned",
                    duration_minutes=part.duration_minutes,
                )
                db.add(new_part)
            copied += 1

    db.flush()
    db.commit()
    return ApiResponse.ok(data={"copied_shifts": copied})


@router.get("/{period_id}/workspace", responses=standard_responses)
def get_workspace(period_id: int, db: Session = Depends(get_db)):
    from app.services.workspace_service import WorkspaceService
    service = WorkspaceService(db)
    data = service.build_workspace(period_id)
    if data is None:
        return ApiResponse.fail_with_code(code="PERIOD_NOT_FOUND", message="Periodo nao encontrado")
    db.commit()
    return ApiResponse.ok(data=data)
