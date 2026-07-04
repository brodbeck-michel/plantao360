from app.models.period import Period
from app.schemas.period.period_create import PeriodCreateDTO
from app.schemas.period.period_response import PeriodResponseDTO
from app.mappers.base_mapper import BaseMapper


class PeriodMapper(BaseMapper[Period, PeriodCreateDTO, PeriodResponseDTO]):
    def __init__(self):
        super().__init__(Period, PeriodCreateDTO, PeriodResponseDTO)

    def to_summary(self, model: Period) -> dict:
        return {
            "id": model.id,
            "year": model.year,
            "month": model.month,
            "status": model.status,
        }
