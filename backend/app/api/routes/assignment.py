from fastapi import APIRouter, Depends, Query, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.unit_of_work import UnitOfWork
from app.services.assignment_service import AssignmentService
from app.schemas.assignment.assignment_create import AssignmentCreateDTO
from app.schemas.assignment.assignment_update import AssignmentUpdateDTO
from app.schemas.assignment.assignment_filters import AssignmentFilterDTO
from app.common.api_response import ApiResponse
from app.common.openapi import standard_responses

router = APIRouter(prefix="/assignments", tags=["Assignments"])


def _recalculate_shift_status(db: Session, shift_id: int) -> None:
    from app.models.shift import Shift
    from app.models.shift_part import ShiftPart
    from app.domain.constants.shift_status import ShiftStatus
    from app.domain.constants.assignment_status import AssignmentStatus

    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if not shift or shift.status == ShiftStatus.CANCELLED:
        return

    active_statuses = [AssignmentStatus.PLANNED, AssignmentStatus.CONFIRMED, AssignmentStatus.STARTED, AssignmentStatus.COMPLETED]
    active_count = db.query(ShiftPart).filter(
        ShiftPart.shift_id == shift_id,
        ShiftPart.status.in_(active_statuses),
    ).count()

    if active_count == 0 and shift.status != ShiftStatus.DRAFT:
        shift.status = ShiftStatus.DRAFT
        db.commit()
    elif active_count > 0 and shift.status == ShiftStatus.DRAFT:
        shift.status = ShiftStatus.SCHEDULED
        db.commit()


@router.get("", responses=standard_responses)
def list_assignments(
    response: Response,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("id"),
    sort_direction: str = Query("asc"),
    shift_id: int | None = Query(None),
    doctor_id: int | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
):
    filter_dto = AssignmentFilterDTO(
        page=page,
        size=size,
        sort_by=sort_by,
        sort_direction=sort_direction,
        shift_id=shift_id,
        doctor_id=doctor_id,
        status=status,
    )
    uow = UnitOfWork()
    uow._session = db
    service = AssignmentService(uow)
    result = service.list(filter_dto)

    response.headers["X-Total-Count"] = str(result.total)
    response.headers["X-Page"] = str(result.page)
    response.headers["X-Page-Size"] = str(result.size)
    response.headers["X-Total-Pages"] = str(result.pages)

    return ApiResponse.ok(data=result.to_dict(), meta={"total": result.total})


@router.get("/{_id}", responses=standard_responses)
def get_assignment(_id: int, db: Session = Depends(get_db)):
    uow = UnitOfWork()
    uow._session = db
    service = AssignmentService(uow)
    result = service.get_by_id(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(code=result.code, message=result.error)
    return ApiResponse.ok(data=result.data.model_dump())


@router.post("", status_code=201, responses=standard_responses)
def create_assignment(dto: AssignmentCreateDTO, db: Session = Depends(get_db)):
    uow = UnitOfWork()
    uow._session = db
    service = AssignmentService(uow)
    result = service.create(dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(code=result.code, message=result.error)
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.put("/{_id}", responses=standard_responses)
def update_assignment(_id: int, dto: AssignmentUpdateDTO, db: Session = Depends(get_db)):
    uow = UnitOfWork()
    uow._session = db
    service = AssignmentService(uow)
    result = service.update(_id, dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(code=result.code, message=result.error)
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/confirm", responses=standard_responses)
def confirm_assignment(_id: int, db: Session = Depends(get_db)):
    uow = UnitOfWork()
    uow._session = db
    service = AssignmentService(uow)
    result = service.confirm(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(code=result.code, message=result.error)
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/start", responses=standard_responses)
def start_assignment(_id: int, db: Session = Depends(get_db)):
    uow = UnitOfWork()
    uow._session = db
    service = AssignmentService(uow)
    result = service.start(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(code=result.code, message=result.error)
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/complete", responses=standard_responses)
def complete_assignment(_id: int, db: Session = Depends(get_db)):
    uow = UnitOfWork()
    uow._session = db
    service = AssignmentService(uow)
    result = service.complete(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(code=result.code, message=result.error)
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/cancel", responses=standard_responses)
def cancel_assignment(_id: int, db: Session = Depends(get_db)):
    uow = UnitOfWork()
    uow._session = db
    service = AssignmentService(uow)
    result = service.cancel(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(code=result.code, message=result.error)
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.delete("/{_id}", responses=standard_responses)
def remove_assignment(_id: int, db: Session = Depends(get_db)):
    uow = UnitOfWork()
    uow._session = db
    service = AssignmentService(uow)
    result = service.remove(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(code=result.code, message=result.error)
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


class DuplicateDayRequest(BaseModel):
    source_date: str
    target_date: str
    period_id: int


class DuplicateWeekRequest(BaseModel):
    source_start_date: str
    target_start_date: str
    period_id: int


class MoveAssignmentRequest(BaseModel):
    target_shift_id: int
    start_time: str | None = None
    end_time: str | None = None


@router.post("/duplicate-day", responses=standard_responses)
def duplicate_day(dto: DuplicateDayRequest, db: Session = Depends(get_db)):
    from datetime import date as date_type, time as time_type
    from app.models.shift import Shift
    from app.models.shift_part import ShiftPart

    source_shifts = db.query(Shift).filter(
        Shift.period_id == dto.period_id,
        Shift.shift_date == dto.source_date,
    ).all()
    if not source_shifts:
        return ApiResponse.ok(data={"copied": 0})

    target_shifts = db.query(Shift).filter(
        Shift.period_id == dto.period_id,
        Shift.shift_date == dto.target_date,
    ).all()
    target_map = {(s.shift_type): s for s in target_shifts}

    copied = 0
    target_shift_ids_to_recalculate = set()
    for src_shift in source_shifts:
        target_shift = target_map.get(src_shift.shift_type)
        if not target_shift:
            continue
        if target_shift.status == "cancelled":
            continue
        existing_parts = db.query(ShiftPart).filter(
            ShiftPart.shift_id == target_shift.id,
            ShiftPart.status.in_(["planned", "confirmed"]),
        ).count()
        if existing_parts > 0:
            continue
        src_parts = db.query(ShiftPart).filter(
            ShiftPart.shift_id == src_shift.id,
            ShiftPart.status.in_(["planned", "confirmed"]),
        ).all()
        for part in src_parts:
            new_part = ShiftPart(
                shift_id=target_shift.id,
                doctor_id=part.doctor_id,
                start_time=part.start_time,
                end_time=part.end_time,
                status="planned",
                duration_minutes=part.duration_minutes,
            )
            db.add(new_part)
            copied += 1
            target_shift_ids_to_recalculate.add(target_shift.id)

    db.commit()
    for sid in target_shift_ids_to_recalculate:
        _recalculate_shift_status(db, sid)
    return ApiResponse.ok(data={"copied": copied})


@router.post("/duplicate-week", responses=standard_responses)
def duplicate_week(dto: DuplicateWeekRequest, db: Session = Depends(get_db)):
    from datetime import date as date_type, timedelta
    from app.models.shift import Shift
    from app.models.shift_part import ShiftPart

    source_start = date_type.fromisoformat(dto.source_start_date)
    target_start = date_type.fromisoformat(dto.target_start_date)

    source_shifts = db.query(Shift).filter(
        Shift.period_id == dto.period_id,
        Shift.shift_date >= source_start,
        Shift.shift_date < source_start + timedelta(days=7),
    ).all()

    target_shifts = db.query(Shift).filter(
        Shift.period_id == dto.period_id,
        Shift.shift_date >= target_start,
        Shift.shift_date < target_start + timedelta(days=7),
    ).all()
    target_map = {(s.shift_date, s.shift_type): s for s in target_shifts}

    copied = 0
    target_shift_ids_to_recalculate = set()
    for src_shift in source_shifts:
        delta = src_shift.shift_date - source_start
        target_date = target_start + delta
        target_shift = target_map.get((target_date, src_shift.shift_type))
        if not target_shift:
            continue
        if target_shift.status == "cancelled":
            continue
        existing_parts = db.query(ShiftPart).filter(
            ShiftPart.shift_id == target_shift.id,
            ShiftPart.status.in_(["planned", "confirmed"]),
        ).count()
        if existing_parts > 0:
            continue
        src_parts = db.query(ShiftPart).filter(
            ShiftPart.shift_id == src_shift.id,
            ShiftPart.status.in_(["planned", "confirmed"]),
        ).all()
        for part in src_parts:
            new_part = ShiftPart(
                shift_id=target_shift.id,
                doctor_id=part.doctor_id,
                start_time=part.start_time,
                end_time=part.end_time,
                status="planned",
                duration_minutes=part.duration_minutes,
            )
            db.add(new_part)
            copied += 1
            target_shift_ids_to_recalculate.add(target_shift.id)

    db.commit()
    for sid in target_shift_ids_to_recalculate:
        _recalculate_shift_status(db, sid)
    return ApiResponse.ok(data={"copied": copied})


@router.put("/{_id}/move", responses=standard_responses)
def move_assignment(_id: int, dto: MoveAssignmentRequest, db: Session = Depends(get_db)):
    from datetime import time as time_type
    from app.models.shift_part import ShiftPart
    from app.models.shift import Shift
    from app.domain.constants.shift_status import ShiftStatus
    from app.repositories.shift_part_repository import ShiftPartRepository
    from app.repositories.shift_repository import ShiftRepository

    entity = db.query(ShiftPart).filter(ShiftPart.id == _id).first()
    if not entity:
        return ApiResponse.fail_with_code(code="ASSIGNMENT_NOT_FOUND", message="Atribuicao nao encontrada")

    target_shift = db.query(Shift).filter(Shift.id == dto.target_shift_id).first()
    if not target_shift:
        return ApiResponse.fail_with_code(code="SHIFT_NOT_FOUND", message="Turno de destino nao encontrado")

    if target_shift.status == ShiftStatus.CANCELLED:
        return ApiResponse.fail_with_code(
            code="ASSIGNMENT_SHIFT_NOT_FOUND",
            message="Não é possível atribuir médicos. Este turno está cancelado. Reative o turno ou altere o status antes de realizar novas atribuições.",
        )

    source_shift_id = entity.shift_id

    if dto.start_time:
        parts = dto.start_time.split(":")
        entity.start_time = time_type(int(parts[0]), int(parts[1]))
    if dto.end_time:
        parts = dto.end_time.split(":")
        entity.end_time = time_type(int(parts[0]), int(parts[1]))

    entity.shift_id = dto.target_shift_id
    db.commit()

    _recalculate_shift_status(db, source_shift_id)
    _recalculate_shift_status(db, dto.target_shift_id)

    return ApiResponse.ok(data={"id": entity.id, "shift_id": entity.shift_id})
