from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.unit_of_work import UnitOfWork
from app.services.doctor_service import DoctorService
from app.services.audit_service import AuditService
from app.schemas.doctor.doctor_create import DoctorCreateDTO
from app.schemas.doctor.doctor_update import DoctorUpdateDTO
from app.schemas.doctor.doctor_filters import DoctorFilterDTO
from app.common.api_response import ApiResponse
from app.common.openapi import standard_responses
from app.core.security.dependencies import get_current_user
from app.models.doctor import Doctor

router = APIRouter(prefix="/doctors", tags=["Doctors"], dependencies=[Depends(get_current_user)])


def _snapshot_doctor(doctor: Doctor) -> dict:
    """Cria um snapshot do estado do médico para auditoria."""
    return {
        "name": doctor.name,
        "crm": doctor.crm,
        "specialty": doctor.specialty,
        "doctor_type": doctor.doctor_type,
        "has_rqe": doctor.has_rqe,
        "career_start_date": doctor.career_start_date.isoformat() if doctor.career_start_date else None,
        "active": doctor.active,
    }


@router.get("", responses=standard_responses)
def list_doctors(
    response: Response,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    name: str | None = Query(None),
    crm: str | None = Query(None),
    active: bool | None = Query(None),
    sort_by: str = Query("id"),
    sort_direction: str = Query("asc"),
    db: Session = Depends(get_db),
):
    filter_dto = DoctorFilterDTO(
        page=page,
        size=size,
        name=name,
        crm=crm,
        active=active,
        sort_by=sort_by,
        sort_direction=sort_direction,
    )
    uow = UnitOfWork()
    uow._session = db
    service = DoctorService(uow)
    result = service.list(filter_dto)

    response.headers["X-Total-Count"] = str(result.total)
    response.headers["X-Page"] = str(result.page)
    response.headers["X-Page-Size"] = str(result.size)
    response.headers["X-Total-Pages"] = str(result.pages)

    return ApiResponse.ok(data=result.to_dict(), meta={"total": result.total})


@router.get("/{doctor_id}", responses=standard_responses)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = DoctorService(uow)
    result = service.get_by_id(doctor_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    return ApiResponse.ok(data=result.data.model_dump())


@router.post("", status_code=201, responses=standard_responses)
def create_doctor(
    dto: DoctorCreateDTO,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    uow = UnitOfWork()
    uow._session = db
    service = DoctorService(uow)
    result = service.create(dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )

    audit_service = AuditService(db)
    doctor = db.query(Doctor).filter(Doctor.id == result.data.id).first()
    if doctor:
        audit_service.record(
            action="create",
            resource="doctor",
            user=current_user,
            resource_id=doctor.id,
            after=_snapshot_doctor(doctor),
        )

    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.put("/{doctor_id}", responses=standard_responses)
def update_doctor(
    doctor_id: int,
    dto: DoctorUpdateDTO,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    doctor_before = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    before_snapshot = _snapshot_doctor(doctor_before) if doctor_before else None

    uow = UnitOfWork()
    uow._session = db
    service = DoctorService(uow)
    result = service.update(doctor_id, dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )

    audit_service = AuditService(db)
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor:
        after_snapshot = _snapshot_doctor(doctor)
        changed_fields = {}
        if before_snapshot:
            for key in before_snapshot:
                if before_snapshot.get(key) != after_snapshot.get(key):
                    changed_fields[key] = after_snapshot[key]
        audit_service.record(
            action="update",
            resource="doctor",
            user=current_user,
            resource_id=doctor.id,
            before=before_snapshot,
            after=changed_fields if changed_fields else after_snapshot,
        )

    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.delete("/{doctor_id}", responses=standard_responses)
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    doctor_before = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    before_snapshot = _snapshot_doctor(doctor_before) if doctor_before else None

    uow = UnitOfWork()
    uow._session = db
    service = DoctorService(uow)
    result = service.delete(doctor_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )

    audit_service = AuditService(db)
    audit_service.record(
        action="delete",
        resource="doctor",
        user=current_user,
        resource_id=doctor_id,
        before=before_snapshot,
    )

    db.commit()
    return ApiResponse.ok(data={"deleted": True})
