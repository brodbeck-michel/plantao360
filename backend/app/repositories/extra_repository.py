"""Extra repository implementation."""

from app.models.shift_extra import ShiftExtra
from app.repositories.base.base_repository import BaseRepository


class ExtraRepository(BaseRepository[ShiftExtra]):
    def __init__(self, session):
        super().__init__(ShiftExtra, session)

    def list_by_shift(self, shift_id: int) -> list[ShiftExtra]:
        return (
            self.session.query(ShiftExtra)
            .filter(ShiftExtra.shift_id == shift_id)
            .all()
        )

    def list_by_doctor(self, doctor_id: int) -> list[ShiftExtra]:
        return (
            self.session.query(ShiftExtra)
            .filter(ShiftExtra.doctor_id == doctor_id)
            .all()
        )
