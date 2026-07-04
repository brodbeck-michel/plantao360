from sqlalchemy.sql import Select
from app.models.period import Period
from app.repositories.specifications.base_specification import BaseSpecification


class PeriodByYear(BaseSpecification):
    def __init__(self, year: int):
        self.year = year

    def is_satisfied_by(self, query: Select) -> Select:
        return query.filter(Period.year == self.year)


class PeriodByStatus(BaseSpecification):
    def __init__(self, status: str):
        self.status = status

    def is_satisfied_by(self, query: Select) -> Select:
        return query.filter(Period.status == self.status)


class CurrentPeriod(BaseSpecification):
    def is_satisfied_by(self, query: Select) -> Select:
        from app.domain.constants.period_status import PeriodStatus
        return query.filter(Period.status != PeriodStatus.PAID)


class PeriodBetweenDates(BaseSpecification):
    def __init__(self, start_year: int, start_month: int, end_year: int, end_month: int):
        self.start_year = start_year
        self.start_month = start_month
        self.end_year = end_year
        self.end_month = end_month

    def is_satisfied_by(self, query: Select) -> Select:
        return query.filter(
            Period.year >= self.start_year,
            Period.year <= self.end_year,
        )
