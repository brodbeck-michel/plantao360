from typing import Optional

from sqlalchemy import String, or_, func

from app.models.doctor import Doctor
from app.repositories.base.base_repository import BaseRepository


class DoctorRepository(BaseRepository[Doctor]):
    def __init__(self, session):
        super().__init__(Doctor, session)

    def get_by_crm(self, crm: str) -> Optional[Doctor]:
        return (
            self.session.query(Doctor)
            .filter(Doctor.crm == crm)
            .first()
        )

    def exists_by_crm(self, crm: str, exclude_id: int | None = None) -> bool:
        query = self.session.query(Doctor).filter(Doctor.crm == crm)
        if exclude_id is not None:
            query = query.filter(Doctor.id != exclude_id)
        return query.first() is not None

    def search(
        self,
        name: str | None = None,
        crm: str | None = None,
        active: bool | None = None,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        sort_direction: str = "asc",
    ) -> list[Doctor]:
        query = self.session.query(Doctor)

        if name:
            query = query.filter(Doctor.name.ilike(f"%{name}%"))
        if crm:
            query = query.filter(Doctor.crm.ilike(f"%{crm}%"))
        if active is not None:
            query = query.filter(Doctor.active == active)

        sort_column = getattr(Doctor, sort_by, Doctor.id)
        if sort_direction == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        return query.offset(skip).limit(limit).all()

    def count_filtered(
        self,
        name: str | None = None,
        crm: str | None = None,
        active: bool | None = None,
    ) -> int:
        query = self.session.query(func.count(Doctor.id))

        if name:
            query = query.filter(Doctor.name.ilike(f"%{name}%"))
        if crm:
            query = query.filter(Doctor.crm.ilike(f"%{crm}%"))
        if active is not None:
            query = query.filter(Doctor.active == active)

        return query.scalar()

    def soft_delete(self, id: int) -> bool:
        doctor = self.get_by_id(id)
        if doctor:
            doctor.active = False
            self.session.flush()
            return True
        return False
