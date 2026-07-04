from app.common.result import Success, Failure
from app.use_cases.periods.base_period_use_case import BasePeriodUseCase
from app.repositories.period_repository import PeriodRepository
from app.schemas.period.period_response import PeriodResponseDTO
from app.domain.errors.period_errors import PeriodErrorCode
from app.domain.constants.period_status import PeriodStatus
from app.domain.events.event_names import DomainEventName
from app.core.logging import get_logger

logger = get_logger("use_case.period.update")


class UpdatePeriod(BasePeriodUseCase):
    def __init__(self, repo: PeriodRepository, **kwargs):
        super().__init__(**kwargs)
        self.repo = repo

    def validate(self, id: int = None, dto=None, **kwargs) -> Failure | None:
        if id is None:
            return Failure(error="ID required", code="VALIDATION_ERROR")
        return None

    def execute(self, id: int = None, dto=None, **kwargs) -> Success:
        period = self.repo.get_by_id(id)
        if not period:
            return Failure(
                error=PeriodErrorCode.PERIOD_NOT_FOUND,
                code=PeriodErrorCode.PERIOD_NOT_FOUND,
            )

        if not self._policy.can_edit(PeriodStatus(period.status)):
            return Failure(
                error=PeriodErrorCode.PERIOD_IMMUTABLE,
                code=PeriodErrorCode.PERIOD_IMMUTABLE,
            )

        if dto.year is not None:
            period.year = dto.year
        if dto.month is not None:
            period.month = dto.month

        updated = self.repo.update(period)

        self._queue_event(
            DomainEventName.PERIOD_UPDATED_V1,
            {"id": updated.id, "year": updated.year, "month": updated.month},
        )

        logger.info("period.updated.v1", extra={"period_id": updated.id})
        return Success(data=PeriodResponseDTO.model_validate(updated))
