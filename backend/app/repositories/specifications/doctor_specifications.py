from sqlalchemy.sql import Select
from app.models.doctor import Doctor
from app.repositories.specifications.base_specification import BaseSpecification


class NameContains(BaseSpecification):
    def __init__(self, name: str):
        self.name = name

    def is_satisfied_by(self, query: Select) -> Select:
        return query.filter(Doctor.name.ilike(f"%{self.name}%"))


class CRMEquals(BaseSpecification):
    def __init__(self, crm: str):
        self.crm = crm

    def is_satisfied_by(self, query: Select) -> Select:
        return query.filter(Doctor.crm == self.crm)


class ActiveEquals(BaseSpecification):
    def __init__(self, active: bool):
        self.active = active

    def is_satisfied_by(self, query: Select) -> Select:
        return query.filter(Doctor.active == self.active)


class HourRateBetween(BaseSpecification):
    def __init__(self, min_rate: float | None = None, max_rate: float | None = None):
        self.min_rate = min_rate
        self.max_rate = max_rate

    def is_satisfied_by(self, query: Select) -> Select:
        if self.min_rate is not None:
            query = query.filter(Doctor.hour_rate >= self.min_rate)
        if self.max_rate is not None:
            query = query.filter(Doctor.hour_rate <= self.max_rate)
        return query
