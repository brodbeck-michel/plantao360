from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.database.unit_of_work import UnitOfWork
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import (
    UserCreateDTO,
    UserUpdateDTO,
    UserResponseDTO,
    LoginRequestDTO,
    LoginResponseDTO,
)
from app.common.result import Success, Failure, Result
from app.common.api_response import ApiResponse
from app.core.security.password import hash_password, verify_password
from app.core.security.jwt import create_access_token
from app.core.logging import get_logger

logger = get_logger("service.user")


class UserService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @property
    def repo(self) -> UserRepository:
        return UserRepository(self.uow.session)

    def list(
        self,
        name: str | None = None,
        email: str | None = None,
        role: str | None = None,
        active: bool | None = None,
        page: int = 1,
        size: int = 20,
        sort_by: str = "id",
        sort_direction: str = "asc",
    ) -> dict:
        skip = (page - 1) * size
        users = self.repo.search(
            name=name, email=email, role=role, active=active,
            skip=skip, limit=size, sort_by=sort_by, sort_direction=sort_direction,
        )
        total = self.repo.count_filtered(
            name=name, email=email, role=role, active=active,
        )
        items = [UserResponseDTO.model_validate(u) for u in users]
        pages = (total + size - 1) // size if size > 0 else 0
        return {
            "items": [i.model_dump() for i in items],
            "page": page,
            "size": size,
            "total": total,
            "pages": pages,
        }

    def get_by_id(self, id: int) -> Result[UserResponseDTO]:
        user = self.repo.get_by_id(id)
        if not user:
            return Failure(error="Usuario nao encontrado", code="USER_NOT_FOUND")
        return Success(data=UserResponseDTO.model_validate(user))

    def create(self, dto: UserCreateDTO) -> Result[UserResponseDTO]:
        if self.repo.exists_by_email(dto.email):
            return Failure(error=f"Email {dto.email} ja cadastrado", code="USER_ALREADY_EXISTS")

        user = User(
            name=dto.name,
            email=dto.email,
            password_hash=hash_password(dto.password),
            role=dto.role,
            active=True,
        )
        created = self.repo.create(user)
        logger.info("user.created", extra={"user_id": created.id})
        return Success(data=UserResponseDTO.model_validate(created))

    def update(self, id: int, dto: UserUpdateDTO) -> Result[UserResponseDTO]:
        user = self.repo.get_by_id(id)
        if not user:
            return Failure(error="Usuario nao encontrado", code="USER_NOT_FOUND")

        if dto.email and self.repo.exists_by_email(dto.email, exclude_id=id):
            return Failure(error=f"Email {dto.email} ja cadastrado", code="USER_ALREADY_EXISTS")

        if dto.name is not None:
            user.name = dto.name
        if dto.email is not None:
            user.email = dto.email
        if dto.password is not None:
            user.password_hash = hash_password(dto.password)
        if dto.role is not None:
            user.role = dto.role
        if dto.active is not None:
            user.active = dto.active

        updated = self.repo.update(user)
        logger.info("user.updated", extra={"user_id": updated.id})
        return Success(data=UserResponseDTO.model_validate(updated))

    def activate(self, id: int) -> Result[UserResponseDTO]:
        user = self.repo.get_by_id(id)
        if not user:
            return Failure(error="Usuario nao encontrado", code="USER_NOT_FOUND")
        user.active = True
        updated = self.repo.update(user)
        logger.info("user.activated", extra={"user_id": updated.id})
        return Success(data=UserResponseDTO.model_validate(updated))

    def deactivate(self, id: int) -> Result[UserResponseDTO]:
        user = self.repo.get_by_id(id)
        if not user:
            return Failure(error="Usuario nao encontrado", code="USER_NOT_FOUND")
        user.active = False
        updated = self.repo.update(user)
        logger.info("user.deactivated", extra={"user_id": updated.id})
        return Success(data=UserResponseDTO.model_validate(updated))

    def delete(self, id: int) -> Result[bool]:
        user = self.repo.get_by_id(id)
        if not user:
            return Failure(error="Usuario nao encontrado", code="USER_NOT_FOUND")
        self.repo.soft_delete(id)
        logger.info("user.deleted", extra={"user_id": id})
        return Success(data=True)

    def authenticate(self, dto: LoginRequestDTO) -> Result[LoginResponseDTO]:
        user = self.repo.get_by_email(dto.email)
        if not user or not user.active:
            return Failure(error="Credenciais invalidas", code="INVALID_CREDENTIALS")

        if not verify_password(dto.password, user.password_hash):
            return Failure(error="Credenciais invalidas", code="INVALID_CREDENTIALS")

        user.last_login = datetime.now(timezone.utc)
        self.repo.update(user)

        token = create_access_token(data={"sub": str(user.id), "role": user.role})
        user_dto = UserResponseDTO.model_validate(user)

        logger.info("user.authenticated", extra={"user_id": user.id})
        return Success(data=LoginResponseDTO(access_token=token, user=user_dto))

    def change_password(self, user_id: int, new_password: str) -> Result[bool]:
        user = self.repo.get_by_id(user_id)
        if not user:
            return Failure(error="Usuario nao encontrado", code="USER_NOT_FOUND")
        user.password_hash = hash_password(new_password)
        self.repo.update(user)
        logger.info("user.password_changed", extra={"user_id": user_id})
        return Success(data=True)
