"""Payroll API routes."""

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.unit_of_work import UnitOfWork
from app.services.payroll_service import PayrollService
from app.schemas.payroll.payroll_create import PayrollCreateDTO
from app.schemas.payroll.payroll_filters import PayrollFilterDTO
from app.schemas.payroll.payroll_reopen import PayrollReopenDTO
from app.schemas.payroll.payroll_governance import (
    PayrollApprovalDTO,
    PayrollLockDTO,
    PayrollUnlockDTO,
    ChecklistItemUpdateDTO,
)
from app.common.api_response import ApiResponse
from app.common.openapi import standard_responses

router = APIRouter(prefix="/payrolls", tags=["Payrolls"])


@router.get("", responses=standard_responses)
def list_payrolls(
    response: Response,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    period_id: int | None = Query(None),
    year_month: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
):
    filter_dto = PayrollFilterDTO(
        page=page,
        size=size,
        period_id=period_id,
        year_month=year_month,
        status=status,
    )
    uow = UnitOfWork()
    uow._session = db
    service = PayrollService(uow)
    result = service.list(filter_dto)

    response.headers["X-Total-Count"] = str(result.total)
    response.headers["X-Page"] = str(result.page)
    response.headers["X-Page-Size"] = str(result.size)
    response.headers["X-Total-Pages"] = str(result.pages)

    return ApiResponse.ok(data=result.to_dict(), meta={"total": result.total})


@router.get("/{_id}", responses=standard_responses)
def get_payroll(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = PayrollService(uow)
    result = service.get_by_id(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    return ApiResponse.ok(data=result.data.model_dump())


@router.post("", status_code=201, responses=standard_responses)
def create_payroll(
    dto: PayrollCreateDTO,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = PayrollService(uow)
    result = service.create(dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/review", responses=standard_responses)
def review_payroll(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = PayrollService(uow)
    result = service.review(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/approve", responses=standard_responses)
def approve_payroll(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = PayrollService(uow)
    result = service.approve(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/export", responses=standard_responses)
def export_payroll(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = PayrollService(uow)
    result = service.export(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/pay", responses=standard_responses)
def mark_paid_payroll(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = PayrollService(uow)
    result = service.mark_paid(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/archive", responses=standard_responses)
def archive_payroll(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = PayrollService(uow)
    result = service.archive(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/reopen", responses=standard_responses)
def reopen_payroll(
    _id: int,
    dto: PayrollReopenDTO,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = PayrollService(uow)
    result = service.reopen(_id, dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.delete("/{_id}", responses=standard_responses)
def delete_payroll(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = PayrollService(uow)
    result = service.delete(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data={"deleted": True})


# --- Governance endpoints ---


@router.get("/{_id}/readiness", responses=standard_responses)
def validate_readiness(
    _id: int,
    db: Session = Depends(get_db),
):
    """Validate if a competency is ready for administrative closing."""
    uow = UnitOfWork()
    uow._session = db
    service = PayrollService(uow)
    result = service.validate_readiness(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/lock", responses=standard_responses)
def lock_payroll(
    _id: int,
    dto: PayrollLockDTO,
    db: Session = Depends(get_db),
):
    """Lock competency administratively — freezes all changes."""
    uow = UnitOfWork()
    uow._session = db
    service = PayrollService(uow)
    result = service.lock(_id, dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/unlock", responses=standard_responses)
def unlock_payroll(
    _id: int,
    dto: PayrollUnlockDTO,
    db: Session = Depends(get_db),
):
    """Unlock competency — removes administrative lock."""
    uow = UnitOfWork()
    uow._session = db
    service = PayrollService(uow)
    result = service.unlock(_id, dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/approve-administratively", responses=standard_responses)
def approve_administratively(
    _id: int,
    dto: PayrollApprovalDTO,
    db: Session = Depends(get_db),
):
    """Approve competency administratively — full governance process."""
    uow = UnitOfWork()
    uow._session = db
    service = PayrollService(uow)
    result = service.approve_administratively(_id, dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())
