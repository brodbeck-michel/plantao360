from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.unit_of_work import UnitOfWork
from app.services.extra_service import ExtraService
from app.schemas.extra.extra_create import ExtraCreateDTO
from app.schemas.extra.extra_update import ExtraUpdateDTO
from app.schemas.extra.extra_filters import ExtraFilterDTO
from app.common.api_response import ApiResponse
from app.common.openapi import standard_responses

router = APIRouter(prefix="/extras", tags=["Extras"])


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
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.put("/{_id}", responses=standard_responses)
def update_extra(
    _id: int,
    dto: ExtraUpdateDTO,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = ExtraService(uow)
    result = service.update(_id, dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/approve", responses=standard_responses)
def approve_extra(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = ExtraService(uow)
    result = service.approve(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/reject", responses=standard_responses)
def reject_extra(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = ExtraService(uow)
    result = service.reject(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/cancel", responses=standard_responses)
def cancel_extra(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = ExtraService(uow)
    result = service.cancel(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.delete("/{_id}", responses=standard_responses)
def delete_extra(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = ExtraService(uow)
    result = service.delete(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data={"deleted": True})
