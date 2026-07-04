from app.common.result import Success
from app.use_cases.periods.base_period_use_case import BasePeriodUseCase
from app.repositories.period_repository import PeriodRepository
from app.schemas.period.period_response import PeriodResponseDTO
from app.schemas.period.period_filters import PeriodFilterDTO
from app.common.pagination import Page


class ListPeriods(BasePeriodUseCase):
    def __init__(self, repo: PeriodRepository):
        super().__init__()
        self.repo = repo

    def execute(self, filter_dto: PeriodFilterDTO = None, **kwargs) -> Success:
        if filter_dto is None:
            filter_dto = PeriodFilterDTO()

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
        page = Page(
            items=dtos,
            page=filter_dto.page,
            size=filter_dto.size,
            total=total,
        )
        return Success(data=page)
