from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.unit_of_work import UnitOfWork
from app.core.security.dependencies import get_current_user, require_role
from app.core.security.password import verify_password
from app.models.user import User
from app.schemas.user import (
    LoginRequestDTO,
    LoginResponseDTO,
    ChangePasswordDTO,
    UserResponseDTO,
)
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


def _get_service(db: Session = Depends(get_db)) -> UserService:
    uow = UnitOfWork()
    uow._session = db
    return UserService(uow)


@router.post("/login", response_model=LoginResponseDTO)
def login(dto: LoginRequestDTO, service: UserService = Depends(_get_service)):
    result = service.authenticate(dto)
    if not result.is_success:
        raise HTTPException(status_code=401, detail=result.error)
    return result.data


@router.get("/me", response_model=UserResponseDTO)
def me(current_user: User = Depends(get_current_user)):
    return UserResponseDTO.model_validate(current_user)


@router.put("/me/password")
def change_my_password(
    dto: ChangePasswordDTO,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    uow = UnitOfWork()
    uow._session = db
    service = UserService(uow)
    result = service.change_password(current_user.id, dto.password)
    if not result.is_success:
        raise HTTPException(status_code=400, detail=result.error)
    db.commit()
    return {"ok": True}
