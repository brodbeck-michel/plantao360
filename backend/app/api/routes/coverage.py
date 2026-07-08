"""Coverage API routes."""

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.unit_of_work import UnitOfWork
from app.services.coverage_service import CoverageService
from app.common.api_response import ApiResponse
from app.common.openapi import standard_responses
from app.core.security.dependencies import get_current_user

router = APIRouter(prefix="/coverage", tags=["Coverage"], dependencies=[Depends(get_current_user)])


@router.post("/consolidate/{period_id}", responses=standard_responses)
def consolidate_period(
    period_id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = CoverageService(uow)
    result = service.consolidate(period_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data=result.data)


@router.post("/invalidate/{period_id}", responses=standard_responses)
def invalidate_snapshots(
    period_id: int,
    db: Session = Depends(get_db),
):
    uow = UnitOfWork()
    uow._session = db
    service = CoverageService(uow)
    result = service.invalidate_snapshots(period_id)
    if result.is_failure:
        return ApiResponse.fail_with_code(
            code=result.code,
            message=result.error,
        )
    db.commit()
    return ApiResponse.ok(data={"invalidated": True})
