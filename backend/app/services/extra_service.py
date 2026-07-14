"""Extra service."""

from app.database.unit_of_work import UnitOfWork
from app.repositories.extra_repository import ExtraRepository
from app.models.shift_extra import ShiftExtra
from app.schemas.extra.extra_create import ExtraCreateDTO
from app.schemas.extra.extra_update import ExtraUpdateDTO
from app.schemas.extra.extra_response import ExtraResponseDTO
from app.schemas.extra.extra_filters import ExtraFilterDTO
from app.common.result import Success, Failure, Result
from app.common.api_response import ApiResponse
from app.events.event_dispatcher import EventDispatcher, Event
from app.domain.events.event_names import DomainEventName
from app.domain.errors.extra_errors import ExtraErrorCode
from app.domain.constants.extra_status import ExtraStatus
from app.core.logging import get_logger

logger = get_logger("service.extra")

event_dispatcher = EventDispatcher()


# ExtraStateMachine — antes em domain/state_machines (consumidor único: este service).
# Inlinada no colapso da domain/ (spec 005, Grupo D). Transições preservadas.
class ExtraStateMachine:
    def __init__(self, aggregate) -> None:
        self._aggregate = aggregate

    def approve(self) -> None:
        self._transition(ExtraStatus.PENDING, ExtraStatus.APPROVED)

    def reject(self) -> None:
        self._transition(ExtraStatus.PENDING, ExtraStatus.REJECTED)

    def cancel(self) -> None:
        current = self._aggregate.status
        allowed = {ExtraStatus.PENDING, ExtraStatus.APPROVED}
        if current not in allowed:
            raise ValueError(f"Cannot cancel extra in status '{current}'")
        self._transition(current, ExtraStatus.CANCELLED)

    def _transition(self, from_status: str, to_status: str) -> None:
        current = self._aggregate.status
        if current != from_status:
            raise ValueError(
                f"Cannot transition from '{current}' to '{to_status}': "
                f"expected '{from_status}'"
            )
        self._aggregate.status = to_status


class ExtraService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @property
    def repo(self) -> ExtraRepository:
        return ExtraRepository(self.uow.session)

    def list(self, filter_dto: ExtraFilterDTO):
        skip = (filter_dto.page - 1) * filter_dto.size
        query = self.repo.session.query(ShiftExtra)

        if filter_dto.shift_id is not None:
            query = query.filter(ShiftExtra.shift_id == filter_dto.shift_id)
        if filter_dto.doctor_id is not None:
            query = query.filter(ShiftExtra.doctor_id == filter_dto.doctor_id)
        if filter_dto.status is not None:
            query = query.filter(ShiftExtra.status == filter_dto.status)

        total = query.count()
        items = query.offset(skip).limit(filter_dto.size).all()
        dtos = [ExtraResponseDTO.model_validate(d) for d in items]

        from app.common.pagination import Page
        return Page(
            items=dtos,
            page=filter_dto.page,
            size=filter_dto.size,
            total=total,
        )

    def get_by_id(self, id: int) -> Result[ExtraResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=ExtraErrorCode.EXTRA_NOT_FOUND,
                code=ExtraErrorCode.EXTRA_NOT_FOUND,
            )
        return Success(data=ExtraResponseDTO.model_validate(entity))

    def create(self, dto: ExtraCreateDTO) -> Result[ExtraResponseDTO]:
        entity = ShiftExtra(
            shift_id=dto.shift_id,
            doctor_id=dto.doctor_id,
            duration_minutes=dto.duration_minutes,
            justification=dto.justification,
            status="pending",
        )
        created = self.repo.create(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.SHIFT_CREATED_V1,
                data={"id": created.id},
            )
        )

        logger.info("extra.created.v1", extra={"extra_id": created.id})
        return Success(data=ExtraResponseDTO.model_validate(created))

    def update(self, id: int, dto: ExtraUpdateDTO) -> Result[ExtraResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=ExtraErrorCode.EXTRA_NOT_FOUND,
                code=ExtraErrorCode.EXTRA_NOT_FOUND,
            )

        update_data = dto.model_dump(exclude_unset=True)
        for field_name, value in update_data.items():
            setattr(entity, field_name, value)

        updated = self.repo.update(entity)

        logger.info("extra.updated.v1", extra={"extra_id": updated.id})
        return Success(data=ExtraResponseDTO.model_validate(updated))

    def approve(self, id: int) -> Result[ExtraResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=ExtraErrorCode.EXTRA_NOT_FOUND,
                code=ExtraErrorCode.EXTRA_NOT_FOUND,
            )

        sm = ExtraStateMachine(entity)
        sm.approve()

        updated = self.repo.update(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.SHIFT_UPDATED_V1,
                data={"id": updated.id},
            )
        )

        logger.info("extra.approved.v1", extra={"extra_id": updated.id})
        return Success(data=ExtraResponseDTO.model_validate(updated))

    def reject(self, id: int) -> Result[ExtraResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=ExtraErrorCode.EXTRA_NOT_FOUND,
                code=ExtraErrorCode.EXTRA_NOT_FOUND,
            )

        sm = ExtraStateMachine(entity)
        sm.reject()

        updated = self.repo.update(entity)

        logger.info("extra.rejected.v1", extra={"extra_id": updated.id})
        return Success(data=ExtraResponseDTO.model_validate(updated))

    def cancel(self, id: int) -> Result[ExtraResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=ExtraErrorCode.EXTRA_NOT_FOUND,
                code=ExtraErrorCode.EXTRA_NOT_FOUND,
            )

        sm = ExtraStateMachine(entity)
        sm.cancel()

        updated = self.repo.update(entity)

        logger.info("extra.cancelled.v1", extra={"extra_id": updated.id})
        return Success(data=ExtraResponseDTO.model_validate(updated))

    def delete(self, id: int) -> Result[bool]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=ExtraErrorCode.EXTRA_NOT_FOUND,
                code=ExtraErrorCode.EXTRA_NOT_FOUND,
            )
        self.repo.delete(id)
        logger.info("extra.deleted", extra={"extra_id": id})
        return Success(data=True)
