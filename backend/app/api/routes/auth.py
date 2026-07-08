from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.unit_of_work import UnitOfWork
from app.services.user_service import UserService
from app.schemas.user import LoginRequestDTO
from app.common.api_response import ApiResponse
from app.core.security.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login")
def login(dto: LoginRequestDTO, db: Session = Depends(get_db)):
    uow = UnitOfWork()
    uow._session = db
    service = UserService(uow)
    result = service.authenticate(dto)
    if result.is_failure:
        return ApiResponse.fail_with_code(code=result.code, message=result.error)
    return ApiResponse.ok(data=result.data.model_dump())


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    from app.schemas.user import UserResponseDTO
    return ApiResponse.ok(data=UserResponseDTO.model_validate(current_user).model_dump())
