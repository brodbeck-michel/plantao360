from typing import Optional

from sqlalchemy import func

from app.models.user import User
from app.repositories.base.base_repository import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session):
        super().__init__(User, session)

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()

    def exists_by_email(self, email: str, exclude_id: int | None = None) -> bool:
        query = self.session.query(User).filter(User.email == email)
        if exclude_id is not None:
            query = query.filter(User.id != exclude_id)
        return query.first() is not None

    def search(
        self,
        name: str | None = None,
        email: str | None = None,
        role: str | None = None,
        active: bool | None = None,
        skip: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        sort_direction: str = "asc",
    ) -> list[User]:
        query = self.session.query(User)

        if name:
            query = query.filter(User.name.ilike(f"%{name}%"))
        if email:
            query = query.filter(User.email.ilike(f"%{email}%"))
        if role:
            query = query.filter(User.role == role)
        if active is not None:
            query = query.filter(User.active == active)

        sort_column = getattr(User, sort_by, User.id)
        if sort_direction == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        return query.offset(skip).limit(limit).all()

    def count_filtered(
        self,
        name: str | None = None,
        email: str | None = None,
        role: str | None = None,
        active: bool | None = None,
    ) -> int:
        query = self.session.query(func.count(User.id))

        if name:
            query = query.filter(User.name.ilike(f"%{name}%"))
        if email:
            query = query.filter(User.email.ilike(f"%{email}%"))
        if role:
            query = query.filter(User.role == role)
        if active is not None:
            query = query.filter(User.active == active)

        return query.scalar()
