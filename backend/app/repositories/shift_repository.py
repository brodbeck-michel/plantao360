from typing import Optional

from sqlalchemy import func

from app.models.shift import Shift
from app.repositories.base.base_repository import BaseRepository


class ShiftRepository(BaseRepository[Shift]):
    def __init__(self, session):
        super().__init__(Shift, session)

    def search(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        sort_direction: str = "asc",
        **filters,
    ) -> list[Shift]:
        query = self.session.query(Shift)

        for key, value in filters.items():
            if value is not None:
                if " >=" in key:
                    col_name = key.replace(" >=", "").strip()
                    if hasattr(Shift, col_name):
                        column = getattr(Shift, col_name)
                        query = query.filter(column >= value)
                elif " <=" in key:
                    col_name = key.replace(" <=", "").strip()
                    if hasattr(Shift, col_name):
                        column = getattr(Shift, col_name)
                        query = query.filter(column <= value)
                elif hasattr(Shift, key):
                    column = getattr(Shift, key)
                    if isinstance(value, str):
                        query = query.filter(column.ilike(f"%{value}%"))
                    else:
                        query = query.filter(column == value)

        sort_column = getattr(Shift, sort_by, Shift.id)
        if sort_direction == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        return query.offset(skip).limit(limit).all()

    def count_filtered(self, **filters) -> int:
        query = self.session.query(func.count(Shift.id))

        for key, value in filters.items():
            if value is not None:
                if " >=" in key:
                    col_name = key.replace(" >=", "").strip()
                    if hasattr(Shift, col_name):
                        column = getattr(Shift, col_name)
                        query = query.filter(column >= value)
                elif " <=" in key:
                    col_name = key.replace(" <=", "").strip()
                    if hasattr(Shift, col_name):
                        column = getattr(Shift, col_name)
                        query = query.filter(column <= value)
                elif hasattr(Shift, key):
                    column = getattr(Shift, key)
                    if isinstance(value, str):
                        query = query.filter(column.ilike(f"%{value}%"))
                    else:
                        query = query.filter(column == value)

        return query.scalar()

    def soft_delete(self, id: int) -> bool:
        entity = self.get_by_id(id)
        if entity:
            entity.status = "cancelled"
            self.session.flush()
            return True
        return False
