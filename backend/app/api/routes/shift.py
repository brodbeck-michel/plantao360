from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.unit_of_work import UnitOfWork
from app.services.shift_service import ShiftService
from app.schemas.shift.shift_create import ShiftCreateDTO
from app.schemas.shift.shift_update import ShiftUpdateDTO
from app.schemas.shift.shift_filters import ShiftFilterDTO
from app.common.api_response import ApiResponse
from app.common.openapi import standard_responses
from app.core.security.dependencies import get_current_user

router = APIRouter(prefix="/shifts", tags=["Shifts"], dependencies=[Depends(get_current_user)])


@router.get("", responses=standard_responses)
def list_shifts(
    response: Response,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    sort_by: str = Query("id"),
    sort_direction: str = Query("asc"),
    period_id: int | None = Query(None),
    shift_type: str | None = Query(None),
    status: str | None = Query(None),
    db: Session = Depends(get_db),
):
    filter_dto = ShiftFilterDTO(
        page=page,
        size=size,
        sort_by=sort_by,
        sort_direction=sort_direction,
        period_id=period_id,
        shift_type=shift_type,
        status=status,
    )
    uow = UnitOfWork()
    uow._session = db
    service = ShiftService(uow)
    result = service.list(filter_dto)

    response.headers["X-Total-Count"] = str(result.total)
    response.headers["X-Page"] = str(result.page)
    response.headers["X-Page-Size"] = str(result.size)
    response.headers["X-Total-Pages"] = str(result.pages)

    return ApiResponse.ok(data=result.to_dict(), meta={"total": result.total})


@router.get("/{_id}", responses=standard_responses)
def get_shift(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = ShiftService(uow)
    result = service.get_by_id(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    return ApiResponse.ok(data=result.data.model_dump())


@router.post("", status_code=201, responses=standard_responses)
def create_shift(
    dto: ShiftCreateDTO,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = ShiftService(uow)
    result = service.create(dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.put("/{_id}", responses=standard_responses)
def update_shift(
    _id: int,
    dto: ShiftUpdateDTO,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = ShiftService(uow)
    result = service.update(_id, dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/start", responses=standard_responses)
def start_shift(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = ShiftService(uow)
    result = service.start(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/complete", responses=standard_responses)
def complete_shift(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = ShiftService(uow)
    result = service.complete(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.patch("/{_id}/cancel", responses=standard_responses)
def cancel_shift(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = ShiftService(uow)
    result = service.cancel(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data.model_dump())


@router.delete("/{_id}", responses=standard_responses)
def delete_shift(
    _id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = ShiftService(uow)
    result = service.delete(_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data={"deleted": True})
