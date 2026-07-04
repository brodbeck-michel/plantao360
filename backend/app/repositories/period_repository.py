from typing import Optional

from sqlalchemy import func

from app.models.period import Period
from app.repositories.base.base_repository import BaseRepository


class PeriodRepository(BaseRepository[Period]):
    def __init__(self, session):
        super().__init__(Period, session)

    def get_by_year_month(self, year: int, month: int) -> Optional[Period]:
        return (
            self.session.query(Period)
            .filter(Period.year == year, Period.month == month)
            .first()
        )

    def get_current_period(self) -> Optional[Period]:
        from app.domain.constants.period_status import PeriodStatus
        return (
            self.session.query(Period)
            .filter(Period.status != PeriodStatus.PAID)
            .order_by(Period.year.desc(), Period.month.desc())
            .first()
        )

    def exists_by_year_month(self, year: int, month: int, exclude_id: int | None = None) -> bool:
        query = self.session.query(Period).filter(
            Period.year == year, Period.month == month
        )
        if exclude_id is not None:
            query = query.filter(Period.id != exclude_id)
        return query.first() is not None

    def search(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        sort_direction: str = "asc",
        **filters,
    ) -> list[Period]:
        query = self.session.query(Period)

        for key, value in filters.items():
            if value is not None and hasattr(Period, key):
                column = getattr(Period, key)
                if isinstance(value, str):
                    query = query.filter(column.ilike(f"%{value}%"))
                else:
                    query = query.filter(column == value)

        sort_column = getattr(Period, sort_by, Period.id)
        if sort_direction == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        return query.offset(skip).limit(limit).all()

    def count_filtered(self, **filters) -> int:
        query = self.session.query(func.count(Period.id))

        for key, value in filters.items():
            if value is not None and hasattr(Period, key):
                column = getattr(Period, key)
                if isinstance(value, str):
                    query = query.filter(column.ilike(f"%{value}%"))
                else:
                    query = query.filter(column == value)

        return query.scalar()
