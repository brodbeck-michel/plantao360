from datetime import datetime

from sqlalchemy import String, Boolean, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base
from app.models.base_mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"
    __table_args__ = (
        CheckConstraint(
            "role IN ('ADMIN','COORDENADOR','FINANCEIRO','MEDICO','CONSULTA')",
            name="ck_users_role_valid",
        ),
        Index("ix_users_email", "email", unique=True),
        Index("ix_users_active", "active"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="CONSULTA")
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    last_login: Mapped[datetime | None] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}, email={self.email}, role={self.role})>"
