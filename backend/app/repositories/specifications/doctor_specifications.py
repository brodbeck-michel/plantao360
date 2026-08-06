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
