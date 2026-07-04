from app.common.result import Success, Failure
from app.use_cases.periods.base_period_use_case import BasePeriodUseCase
from app.repositories.period_repository import PeriodRepository
from app.schemas.period.period_response import PeriodResponseDTO
from app.domain.errors.period_errors import PeriodErrorCode


class GetPeriod(BasePeriodUseCase):
    def __init__(self, repo: PeriodRepository):
        super().__init__()
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
        return Success(data=PeriodResponseDTO.model_validate(period))
