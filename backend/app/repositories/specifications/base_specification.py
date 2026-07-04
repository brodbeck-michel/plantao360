from sqlalchemy import and_, or_, not_
from sqlalchemy.sql import Select


class BaseSpecification:
    def __init__(self):
        self._conditions: list = []

    def and_(self, *specs: "BaseSpecification") -> "AndSpecification":
        return AndSpecification(*specs)

    def or_(self, *specs: "BaseSpecification") -> "OrSpecification":
        return OrSpecification(*specs)

    def not_(self, spec: "BaseSpecification") -> "NotSpecification":
        return NotSpecification(spec)

    def is_satisfied_by(self, query: Select) -> Select:
        return query


class AndSpecification(BaseSpecification):
    def __init__(self, *specs: BaseSpecification):
        self.specs = specs

    def is_satisfied_by(self, query: Select) -> Select:
        for spec in self.specs:
            query = spec.is_satisfied_by(query)
        return query


class OrSpecification(BaseSpecification):
    def __init__(self, *specs: BaseSpecification):
        self.specs = specs

    def is_satisfied_by(self, query: Select) -> Select:
        conditions = []
        for spec in self.specs:
            conditions.append(spec.is_satisfied_by(query).whereclause)
        if conditions:
            return query.where(or_(*conditions))
        return query


class NotSpecification(BaseSpecification):
    def __init__(self, spec: BaseSpecification):
        self.spec = spec

    def is_satisfied_by(self, query: Select) -> Select:
        inner = self.spec.is_satisfied_by(query)
        if inner.whereclause is not None:
            return query.where(not_(inner.whereclause))
        return query
