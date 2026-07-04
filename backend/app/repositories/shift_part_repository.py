from typing import Optional

from sqlalchemy import func

from app.models.shift_part import ShiftPart
from app.repositories.base.base_repository import BaseRepository


class ShiftPartRepository(BaseRepository[ShiftPart]):
    def __init__(self, session):
        super().__init__(ShiftPart, session)

    def search(
        self,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        sort_direction: str = "asc",
        **filters,
    ) -> list[ShiftPart]:
        query = self.session.query(ShiftPart)

        for key, value in filters.items():
            if value is not None and hasattr(ShiftPart, key):
                column = getattr(ShiftPart, key)
                if isinstance(value, str):
                    query = query.filter(column.ilike(f"%{value}%"))
                else:
                    query = query.filter(column == value)

        sort_column = getattr(ShiftPart, sort_by, ShiftPart.id)
        if sort_direction == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        return query.offset(skip).limit(limit).all()

    def count_filtered(self, **filters) -> int:
        query = self.session.query(func.count(ShiftPart.id))

        for key, value in filters.items():
            if value is not None and hasattr(ShiftPart, key):
                column = getattr(ShiftPart, key)
                if isinstance(value, str):
                    query = query.filter(column.ilike(f"%{value}%"))
                else:
                    query = query.filter(column == value)

        return query.scalar()

    def find_same_date_assignments(
        self, doctor_id: int, shift_date, exclude_id: Optional[int] = None
    ) -> list[ShiftPart]:
        from app.models.shift import Shift
        query = self.session.query(ShiftPart).join(Shift).filter(
            ShiftPart.doctor_id == doctor_id,
            Shift.shift_date == shift_date,
            ShiftPart.status.in_(["planned", "confirmed"]),
        )
        if exclude_id:
            query = query.filter(ShiftPart.id != exclude_id)
        return query.all()

    def find_overlapping(
        self, doctor_id: int, start_time, end_time, exclude_id: Optional[int] = None
    ) -> list[ShiftPart]:
        query = self.session.query(ShiftPart).filter(
            ShiftPart.doctor_id == doctor_id,
            ShiftPart.start_time < end_time,
            ShiftPart.end_time > start_time,
        )
        if exclude_id:
            query = query.filter(ShiftPart.id != exclude_id)
        return query.all()
