from datetime import date, timedelta

from app.common.result import Success, Failure
from app.use_cases.periods.base_period_use_case import BasePeriodUseCase
from app.repositories.period_repository import PeriodRepository
from app.models.period import Period
from app.models.shift import Shift
from app.schemas.period.period_create import PeriodCreateDTO
from app.schemas.period.period_response import PeriodResponseDTO
from app.domain.errors.period_errors import PeriodErrorCode
from app.domain.events.event_names import DomainEventName
from app.domain.constants.shift_types import ShiftType
from app.domain.constants.shift_status import ShiftStatus
from app.domain.constants.competency_dates import get_competency_dates
from app.core.logging import get_logger

logger = get_logger("use_case.period.create")


class CreatePeriod(BasePeriodUseCase):
    def __init__(self, repo: PeriodRepository, **kwargs):
        super().__init__(**kwargs)
        self.repo = repo

    def validate(self, dto: PeriodCreateDTO = None, **kwargs) -> Failure | None:
        if dto is None:
            return Failure(error="DTO required", code="VALIDATION_ERROR")
        if self.repo.exists_by_year_month(dto.year, dto.month):
            return Failure(
                error=f"Periodo {dto.year}/{dto.month:02d} ja cadastrado",
                code=PeriodErrorCode.PERIOD_ALREADY_EXISTS,
            )
        return None

    def execute(self, dto: PeriodCreateDTO = None, **kwargs) -> Success:
        period = Period(year=dto.year, month=dto.month)
        created = self.repo.create(period)

        self._generate_base_shifts(created)

        self._queue_event(
            DomainEventName.PERIOD_CREATED_V1,
            {"id": created.id, "year": created.year, "month": created.month},
        )

        logger.info("period.created.v1", extra={"period_id": created.id})
        return Success(data=PeriodResponseDTO.model_validate(created))

    def _generate_base_shifts(self, period: Period) -> None:
        start_date, end_date = get_competency_dates(period.year, period.month)

        shift_types = [s.value for s in ShiftType]
        session = self.repo.session

        current = start_date
        while current <= end_date:
            for st in shift_types:
                existing = session.query(Shift).filter(
                    Shift.period_id == period.id,
                    Shift.shift_date == current,
                    Shift.shift_type == st,
                ).first()
                if not existing:
                    new_shift = Shift(
                        period_id=period.id,
                        shift_date=current,
                        shift_type=st,
                        status=ShiftStatus.DRAFT,
                    )
                    session.add(new_shift)
            current += timedelta(days=1)

        session.flush()
