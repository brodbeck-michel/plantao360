from typing import Optional

from app.database.unit_of_work import UnitOfWork
from app.repositories.period_repository import PeriodRepository
from app.models.period import Period
from app.schemas.period.period_create import PeriodCreateDTO
from app.schemas.period.period_update import PeriodUpdateDTO
from app.schemas.period.period_response import PeriodResponseDTO
from app.schemas.period.period_filters import PeriodFilterDTO
from app.common.pagination import Page
from app.common.result import Success, Failure, Result
from app.common.api_response import ApiResponse
from app.events.event_dispatcher import EventDispatcher, Event
from app.domain.events.event_names import DomainEventName
from app.domain.errors.period_errors import PeriodErrorCode
from app.core.logging import get_logger

logger = get_logger("service.period")

event_dispatcher = EventDispatcher()


class PeriodService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    @property
    def repo(self) -> PeriodRepository:
        return PeriodRepository(self.uow.session)

    def list(self, filter_dto: PeriodFilterDTO) -> Page[PeriodResponseDTO]:
        skip = (filter_dto.page - 1) * filter_dto.size
        items = self.repo.search(
            skip=skip,
            limit=filter_dto.size,
            sort_by=filter_dto.sort_by,
            sort_direction=filter_dto.sort_direction,
            **filter_dto.to_filters(),
        )
        total = self.repo.count_filtered(**filter_dto.to_filters())
        dtos = [PeriodResponseDTO.model_validate(d) for d in items]
        return Page(
            items=dtos,
            page=filter_dto.page,
            size=filter_dto.size,
            total=total,
        )

    def get_by_id(self, id: int) -> Result[PeriodResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=PeriodErrorCode.PERIOD_NOT_FOUND,
                code=PeriodErrorCode.PERIOD_NOT_FOUND,
            )
        return Success(data=PeriodResponseDTO.model_validate(entity))

    def create(self, dto: PeriodCreateDTO) -> Result[PeriodResponseDTO]:
        if self.repo.exists_by_year_month(dto.year, dto.month):
            return Failure(
                error=f"Periodo {dto.year}/{dto.month:02d} ja cadastrado",
                code=PeriodErrorCode.PERIOD_ALREADY_EXISTS,
            )

        entity = Period(**dto.model_dump())
        created = self.repo.create(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.PERIOD_CREATED_V1,
                data={"id": created.id},
            )
        )

        logger.info("period.created.v1", extra={"period_id": created.id})
        return Success(data=PeriodResponseDTO.model_validate(created))

    def update(self, id: int, dto: PeriodUpdateDTO) -> Result[PeriodResponseDTO]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=PeriodErrorCode.PERIOD_NOT_FOUND,
                code=PeriodErrorCode.PERIOD_NOT_FOUND,
            )

        update_data = dto.model_dump(exclude_unset=True)
        for field_name, value in update_data.items():
            setattr(entity, field_name, value)

        updated = self.repo.update(entity)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.PERIOD_UPDATED_V1,
                data={"id": updated.id},
            )
        )

        logger.info("period.updated.v1", extra={"period_id": updated.id})
        return Success(data=PeriodResponseDTO.model_validate(updated))

    def delete(self, id: int) -> Result[bool]:
        entity = self.repo.get_by_id(id)
        if not entity:
            return Failure(
                error=PeriodErrorCode.PERIOD_NOT_FOUND,
                code=PeriodErrorCode.PERIOD_NOT_FOUND,
            )

        self.repo.soft_delete(id)

        event_dispatcher.dispatch(
            Event(
                name=DomainEventName.PERIOD_DEACTIVATED_V1,
                data={"id": id},
            )
        )

        logger.info("period.deactivated.v1", extra={"period_id": id})
        return Success(data=True)
