from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.unit_of_work import UnitOfWork
from app.core.security.dependencies import get_current_user, require_role
from app.services.audit_service import AuditService
from app.models.user import User
from app.schemas.user import UserCreateDTO, UserUpdateDTO, UserResponseDTO, ChangePasswordDTO
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def _snapshot_user(user: User) -> dict:
    """Cria snapshot do usuário para auditoria (SEM password_hash — FR-004)."""
    return {
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "active": user.active,
        "doctor_id": user.doctor_id,
    }


@router.get("", response_model=list[UserResponseDTO])
def list_users(
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_role("ADMIN")),
):
    uow = UnitOfWork()
    uow._session = db
    service = UserService(uow)
    result = service.list()
    return result.get("items", [])


@router.get("/{user_id}", response_model=UserResponseDTO)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_role("ADMIN")),
):
    uow = UnitOfWork()
    uow._session = db
    service = UserService(uow)
    result = service.get_by_id(user_id)
    if not result.is_success:
        raise HTTPException(status_code=404, detail=result.error)
    return result.data


@router.post("", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED)
def create_user(
    dto: UserCreateDTO,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_role("ADMIN")),
):
    uow = UnitOfWork()
    uow._session = db
    service = UserService(uow)
    result = service.create(dto)
    if not result.is_success:
        raise HTTPException(status_code=400, detail=result.error)

    audit_service = AuditService(db)
    user = db.query(User).filter(User.id == result.data.id).first()
    if user:
        audit_service.record(
            action="create",
            resource="user",
            user=_current_user,
            resource_id=user.id,
            after=_snapshot_user(user),
        )

    db.commit()
    return result.data


@router.put("/{user_id}", response_model=UserResponseDTO)
def update_user(
    user_id: int,
    dto: UserUpdateDTO,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_role("ADMIN")),
):
    user_before = db.query(User).filter(User.id == user_id).first()
    before_snapshot = _snapshot_user(user_before) if user_before else None

    uow = UnitOfWork()
    uow._session = db
    service = UserService(uow)
    result = service.update(user_id, dto)
    if not result.is_success:
        raise HTTPException(status_code=400, detail=result.error)

    audit_service = AuditService(db)
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        after_snapshot = _snapshot_user(user)
        changed_fields = {}
        if before_snapshot:
            for key in before_snapshot:
                if before_snapshot.get(key) != after_snapshot.get(key):
                    changed_fields[key] = after_snapshot[key]
        audit_service.record(
            action="update",
            resource="user",
            user=_current_user,
            resource_id=user.id,
            before=before_snapshot,
            after=changed_fields if changed_fields else after_snapshot,
        )

    db.commit()
    return result.data


@router.post("/{user_id}/activate", response_model=UserResponseDTO)
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_role("ADMIN")),
):
    user_before = db.query(User).filter(User.id == user_id).first()
    before_snapshot = _snapshot_user(user_before) if user_before else None

    uow = UnitOfWork()
    uow._session = db
    service = UserService(uow)
    result = service.activate(user_id)
    if not result.is_success:
        raise HTTPException(status_code=400, detail=result.error)

    audit_service = AuditService(db)
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        audit_service.record(
            action="update",
            resource="user",
            user=_current_user,
            resource_id=user.id,
            before={"active": before_snapshot.get("active")} if before_snapshot else None,
            after={"active": user.active},
        )

    db.commit()
    return result.data


@router.post("/{user_id}/deactivate", response_model=UserResponseDTO)
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_role("ADMIN")),
):
    user_before = db.query(User).filter(User.id == user_id).first()
    before_snapshot = _snapshot_user(user_before) if user_before else None

    uow = UnitOfWork()
    uow._session = db
    service = UserService(uow)
    result = service.deactivate(user_id)
    if not result.is_success:
        raise HTTPException(status_code=400, detail=result.error)

    audit_service = AuditService(db)
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        audit_service.record(
            action="update",
            resource="user",
            user=_current_user,
            resource_id=user.id,
            before={"active": before_snapshot.get("active")} if before_snapshot else None,
            after={"active": user.active},
        )

    db.commit()
    return result.data


@router.post("/{user_id}/password")
def change_user_password(
    user_id: int,
    dto: ChangePasswordDTO,
    db: Session = Depends(get_db),
    _current_user: User = Depends(require_role("ADMIN")),
):
    uow = UnitOfWork()
    uow._session = db
    service = UserService(uow)
    result = service.change_password(user_id, dto.password)
    if not result.is_success:
        raise HTTPException(status_code=400, detail=result.error)

    audit_service = AuditService(db)
    audit_service.record(
        action="update",
        resource="user",
        user=_current_user,
        resource_id=user_id,
        after={"password_changed": True},
    )

    db.commit()
    return {"ok": True}
