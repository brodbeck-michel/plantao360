from app.common.result import Success, Failure
from app.use_cases.periods.base_period_use_case import BasePeriodUseCase
from app.repositories.period_repository import PeriodRepository
from app.schemas.period.period_response import PeriodResponseDTO
from app.domain.errors.period_errors import PeriodErrorCode
from app.domain.constants.period_status import PeriodStatus
from app.domain.events.event_names import DomainEventName
from app.core.logging import get_logger

logger = get_logger("use_case.period.reopen")


class ReopenPeriod(BasePeriodUseCase):
    def __init__(self, repo: PeriodRepository, **kwargs):
        super().__init__(**kwargs)
        self.repo = repo

    def validate(self, id: int = None, **kwargs) -> Failure | None:
        if id is None:
            return Failure(error="ID required", code="VALIDATION_ERROR")
        return None

    def execute(self, id: int = None, **kwargs) -> Success:
        period = self.repo.get_by_id(id)
        if not period:
            return Failure(
                error=PeriodErrorCode.PERIOD_NOT_FOUND,
                code=PeriodErrorCode.PERIOD_NOT_FOUND,
            )

        error = self._state_machine.validate_transition(
            PeriodStatus(period.status), PeriodStatus.DRAFT
        )
        if error:
            return Failure(error=error, code=error)

        period.status = PeriodStatus.DRAFT
        updated = self.repo.update(period)

        self._queue_event(
            DomainEventName.PERIOD_REOPENED_V1,
            {"id": updated.id, "year": updated.year, "month": updated.month},
        )

        logger.info("period.reopened.v1", extra={"period_id": updated.id})
        return Success(data=PeriodResponseDTO.model_validate(updated))
