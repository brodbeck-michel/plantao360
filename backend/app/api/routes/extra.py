from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.unit_of_work import UnitOfWork
from app.services.extra_service import ExtraService
from app.services.audit_service import AuditService
from app.schemas.extra.extra_create import ExtraCreateDTO
from app.schemas.extra.extra_update import ExtraUpdateDTO
from app.schemas.extra.extra_filters import ExtraFilterDTO
from app.common.api_response import ApiResponse
from app.common.openapi import standard_responses
from app.core.security.dependencies import get_current_user
from app.models.shift_extra import ShiftExtra

router = APIRouter(prefix="/extras", tags=["Extras"], dependencies=[Depends(get_current_user)])


def _snapshot_shift_extra(shift_extra: ShiftExtra) -> dict:
    """Cria um snapshot do estado da hora extra para auditoria."""
    from app.models.doctor import Doctor
    from app.models.shift import Shift

    shift = shift_extra.shift
    doctor = shift_extra.doctor
    return {
        "shift_id": shift_extra.shift_id,
        "shift_date": shift.shift_date.isoformat() if shift.shift_date else None,
        "doctor_id": shift_extra.doctor_id,
        "doctor_name": doctor.name if doctor else None,
        "duration_minutes": shift_extra.duration_minutes,
        "justification": shift_extra.justification,
        "status": shift_extra.status,
    }


@router.get("", responses=standard_responses)
def list_extras(
    response: Response,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    shift_id: int | None = Query(None),
    doctor_id: int | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
):
    filter_dto = ExtraFilterDTO(
        page=page,
        size=size,
        shift_id=shift_id,
        doctor_id=doctor_id,
        status=status,
    )
    uow = UnitOfWork()
    uow._session = db
    service = ExtraService(uow)
    result = service.list(filter_dto)

    response.headers["X-Total-Count"] = str(result.total)
    response.headers["X-Page"] = str(result.page)
    response.headers["X-Page-Size"] = str(result.size)
    response.headers["X-Total-Pages"] = str(result.pages)

    return ApiResponse.ok(data=result.to_dict(), meta={"total": result.total})


@router.get("/{_id}", responses=standard_responses)
def get_extra(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = ExtraService(uow)
    result = service.get_by_id(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    return ApiResponse.ok(data=result.data.model_dump())


@router.post("", status_code=201, responses=standard_responses)
def create_extra(
    dto: ExtraCreateDTO,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    uow = UnitOfWork()
    uow._session = db
    service = ExtraService(uow)
    result = service.create(dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )

    audit_service = AuditService(db)
    created_extra = result.data
    shift_extra = db.query(ShiftExtra).filter(ShiftExtra.id == created_extra.id).first()
    if shift_extra:
        after = _snapshot_shift_extra(shift_extra)
        audit_service.record(
            action="create",
            resource="shift_extra",
            user=current_user,
            resource_id=shift_extra.id,
            after=after,
            period_id=shift_extra.shift.period_id,
        )

    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.put("/{_id}", responses=standard_responses)
def update_extra(
    _id: int,
    dto: ExtraUpdateDTO,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    shift_extra_before = db.query(ShiftExtra).filter(ShiftExtra.id == _id).first()
    before_snapshot = _snapshot_shift_extra(shift_extra_before) if shift_extra_before else None

    uow = UnitOfWork()
    uow._session = db
    service = ExtraService(uow)
    result = service.update(_id, dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )

    audit_service = AuditService(db)
    shift_extra = db.query(ShiftExtra).filter(ShiftExtra.id == _id).first()
    if shift_extra:
        after_snapshot = _snapshot_shift_extra(shift_extra)
        changed_fields = {}
        if before_snapshot:
            for key in before_snapshot:
                if before_snapshot.get(key) != after_snapshot.get(key):
                    changed_fields[key] = after_snapshot[key]
        audit_service.record(
            action="update",
            resource="shift_extra",
            user=current_user,
            resource_id=shift_extra.id,
            before=before_snapshot,
            after=changed_fields if changed_fields else after_snapshot,
            period_id=shift_extra.shift.period_id,
        )

    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/approve", responses=standard_responses)
def approve_extra(
    _id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    shift_extra_before = db.query(ShiftExtra).filter(ShiftExtra.id == _id).first()
    before_snapshot = _snapshot_shift_extra(shift_extra_before) if shift_extra_before else None

    uow = UnitOfWork()
    uow._session = db
    service = ExtraService(uow)
    result = service.approve(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )

    audit_service = AuditService(db)
    shift_extra = db.query(ShiftExtra).filter(ShiftExtra.id == _id).first()
    if shift_extra:
        after_snapshot = _snapshot_shift_extra(shift_extra)
        audit_service.record(
            action="update",
            resource="shift_extra",
            user=current_user,
            resource_id=shift_extra.id,
            before={"status": before_snapshot.get("status")} if before_snapshot else None,
            after={"status": after_snapshot.get("status")},
            period_id=shift_extra.shift.period_id,
        )

    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/reject", responses=standard_responses)
def reject_extra(
    _id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    shift_extra_before = db.query(ShiftExtra).filter(ShiftExtra.id == _id).first()
    before_snapshot = _snapshot_shift_extra(shift_extra_before) if shift_extra_before else None

    uow = UnitOfWork()
    uow._session = db
    service = ExtraService(uow)
    result = service.reject(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )

    audit_service = AuditService(db)
    shift_extra = db.query(ShiftExtra).filter(ShiftExtra.id == _id).first()
    if shift_extra:
        after_snapshot = _snapshot_shift_extra(shift_extra)
        audit_service.record(
            action="update",
            resource="shift_extra",
            user=current_user,
            resource_id=shift_extra.id,
            before={"status": before_snapshot.get("status")} if before_snapshot else None,
            after={"status": after_snapshot.get("status")},
            period_id=shift_extra.shift.period_id,
        )

    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/cancel", responses=standard_responses)
def cancel_extra(
    _id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    shift_extra_before = db.query(ShiftExtra).filter(ShiftExtra.id == _id).first()
    before_snapshot = _snapshot_shift_extra(shift_extra_before) if shift_extra_before else None

    uow = UnitOfWork()
    uow._session = db
    service = ExtraService(uow)
    result = service.cancel(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )

    audit_service = AuditService(db)
    shift_extra = db.query(ShiftExtra).filter(ShiftExtra.id == _id).first()
    if shift_extra:
        after_snapshot = _snapshot_shift_extra(shift_extra)
        audit_service.record(
            action="update",
            resource="shift_extra",
            user=current_user,
            resource_id=shift_extra.id,
            before={"status": before_snapshot.get("status")} if before_snapshot else None,
            after={"status": after_snapshot.get("status")},
            period_id=shift_extra.shift.period_id,
        )

    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.delete("/{_id}", responses=standard_responses)
def delete_extra(
    _id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    shift_extra_before = db.query(ShiftExtra).filter(ShiftExtra.id == _id).first()
    before_snapshot = _snapshot_shift_extra(shift_extra_before) if shift_extra_before else None
    period_id = shift_extra_before.shift.period_id if shift_extra_before else None

    uow = UnitOfWork()
    uow._session = db
    service = ExtraService(uow)
    result = service.delete(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )

    audit_service = AuditService(db)
    audit_service.record(
        action="delete",
        resource="shift_extra",
        user=current_user,
        resource_id=_id,
        before=before_snapshot,
        period_id=period_id,
    )

    db.commit()
    return ApiResponse.ok(data={"deleted": True})
