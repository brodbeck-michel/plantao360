from typing import Optional

from app.database.unit_of_work import UnitOfWork
from app.repositories.shift_repository import ShiftRepository
from app.models.shift import Shift
from app.schemas.shift.shift_create import ShiftCreateDTO
from app.schemas.shift.shift_update import ShiftUpdateDTO
from app.schemas.shift.shift_response import ShiftResponseDTO
from app.schemas.shift.shift_filters import ShiftFilterDTO
from app.common.pagination import Page
from app.common.result import Success, Failure, Result
from app.common.api_response import ApiResponse
from app.events.event_dispatcher import EventDispatcher, Event
from app.domain.events.event_names import DomainEventName
from app.domain.errors.shift_errors import ShiftErrorCode
from app.domain.state_machines.shift_state_machine import ShiftStateMachine
from app.domain.rules.shift_rules import ShiftRules
from app.domain.constants.shift_status import ShiftStatus
from app.domain.constants.competency_dates import get_competency_dates
from app.core.logging import get_logger

logger = get_logger("service.shift")

event_dispatcher = EventDispatcher()


class ShiftService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @property
    def repo(self) -> ShiftRepository:
        return ShiftRepository(self.uow.session)

    def list(self, filter_dto: ShiftFilterDTO) -> Page[ShiftResponseDTO]:
        filters = filter_dto.to_filters()

        if filter_dto.period_id is not None:
            from app.models.period import Period
            period = self.uow.session.query(Period).filter(Period.id == filter_dto.period_id).first()
            if period:
                start_date, end_date = get_competency_dates(period.year, period.month)
                filters["shift_date >="] = start_date
                filters["shift_date <="] = end_date

        skip = (filter_dto.page - 1) * filter_dto.size
        items = self.repo.search(
            skip=skip,
            limit=filter_dto.size,
            sort_by=filter_dto.sort_by,
            sort_direction=filter_dto.sort_direction,
            **filters,
        )
        total = self.repo.count_filtered(**filters)
        dtos = [ShiftResponseDTO.model_validate(d) for d in items]
        return Page(
            items=dtos,
            page=filter_dto.page,
            size=filter_dto.size,
            total=total,
        )

    def get_by_id(self, id: int) -> Result[ShiftResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=ShiftErrorCode.SHIFT_NOT_FOUND,
                code=ShiftErrorCode.SHIFT_NOT_FOUND,
            )
        return Success(data=ShiftResponseDTO.model_validate(entity))

    def create(self, dto: ShiftCreateDTO) -> Result[ShiftResponseDTO]:
        entity = Shift(
            period_id=dto.period_id,
            shift_date=dto.shift_date,
            shift_type=dto.shift_type,
            scheduled_start=dto.scheduled_start,
            scheduled_end=dto.scheduled_end,
            doctor_count=dto.doctor_count,
            total_duration_minutes=dto.total_duration_minutes,
            status=ShiftStatus.DRAFT,
        )
        created = self.repo.create(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.SHIFT_CREATED_V1,
                data={"id": created.id},
            )
        )

        logger.info("shift.created.v1", extra={"shift_id": created.id})
        return Success(data=ShiftResponseDTO.model_validate(created))

    def update(self, id: int, dto: ShiftUpdateDTO) -> Result[ShiftResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=ShiftErrorCode.SHIFT_NOT_FOUND,
                code=ShiftErrorCode.SHIFT_NOT_FOUND,
            )

        rules = ShiftRules(entity)
        validation_errors = rules.validate_can_update()
        if validation_errors:
            return Failure(
                error=validation_errors[0],
                code=ShiftErrorCode.SHIFT_IMMUTABLE,
            )

        if dto.status is not None and dto.status != entity.status:
            valid_transitions = {
                ShiftStatus.DRAFT: {ShiftStatus.SCHEDULED, ShiftStatus.CANCELLED},
                ShiftStatus.SCHEDULED: {ShiftStatus.IN_PROGRESS, ShiftStatus.CANCELLED},
                ShiftStatus.IN_PROGRESS: {ShiftStatus.COMPLETED, ShiftStatus.CANCELLED},
            }
            allowed = valid_transitions.get(entity.status, set())
            if dto.status not in allowed:
                return Failure(
                    error=f"Cannot transition from '{entity.status}' to '{dto.status}'",
                    code=ShiftErrorCode.SHIFT_IMMUTABLE,
                )

        update_data = dto.model_dump(exclude_unset=True)
        for field_name, value in update_data.items():
            setattr(entity, field_name, value)

        updated = self.repo.update(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.SHIFT_UPDATED_V1,
                data={"id": updated.id},
            )
        )

        logger.info("shift.updated.v1", extra={"shift_id": updated.id})
        return Success(data=ShiftResponseDTO.model_validate(updated))

    def start(self, id: int) -> Result[ShiftResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=ShiftErrorCode.SHIFT_NOT_FOUND,
                code=ShiftErrorCode.SHIFT_NOT_FOUND,
            )

        rules = ShiftRules(entity)
        validation_errors = rules.validate_can_start()
        if validation_errors:
            return Failure(
                error=validation_errors[0],
                code=ShiftErrorCode.SHIFT_ALREADY_STARTED,
            )

        sm = ShiftStateMachine(entity)
        sm.start()

        updated = self.repo.update(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.SHIFT_STARTED_V1,
                data={"id": updated.id},
            )
        )

        logger.info("shift.started.v1", extra={"shift_id": updated.id})
        return Success(data=ShiftResponseDTO.model_validate(updated))

    def complete(self, id: int) -> Result[ShiftResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=ShiftErrorCode.SHIFT_NOT_FOUND,
                code=ShiftErrorCode.SHIFT_NOT_FOUND,
            )

        rules = ShiftRules(entity)
        validation_errors = rules.validate_can_complete()
        if validation_errors:
            return Failure(
                error=validation_errors[0],
                code=ShiftErrorCode.SHIFT_ALREADY_COMPLETED,
            )

        sm = ShiftStateMachine(entity)
        sm.complete()

        updated = self.repo.update(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.SHIFT_COMPLETED_V1,
                data={"id": updated.id},
            )
        )

        logger.info("shift.completed.v1", extra={"shift_id": updated.id})
        return Success(data=ShiftResponseDTO.model_validate(updated))

    def cancel(self, id: int) -> Result[ShiftResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=ShiftErrorCode.SHIFT_NOT_FOUND,
                code=ShiftErrorCode.SHIFT_NOT_FOUND,
            )

        rules = ShiftRules(entity)
        validation_errors = rules.validate_can_cancel()
        if validation_errors:
            return Failure(
                error=validation_errors[0],
                code=ShiftErrorCode.SHIFT_CANNOT_BE_CANCELLED,
            )

        sm = ShiftStateMachine(entity)
        sm.cancel()

        updated = self.repo.update(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.SHIFT_CANCELLED_V1,
                data={"id": updated.id},
            )
        )

        logger.info("shift.cancelled.v1", extra={"shift_id": updated.id})
        return Success(data=ShiftResponseDTO.model_validate(updated))

    def delete(self, id: int) -> Result[bool]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=ShiftErrorCode.SHIFT_NOT_FOUND,
                code=ShiftErrorCode.SHIFT_NOT_FOUND,
            )
        self.repo.soft_delete(id)
        logger.info("shift.deleted", extra={"shift_id": id})
        return Success(data=True)
