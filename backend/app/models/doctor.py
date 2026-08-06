from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import String, Boolean, Date, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_mixins import TimestampMixin, SoftDeleteMixin
from app.domain.constants.hour_rate_table import compute_hour_rate

if TYPE_CHECKING:
    from app.models.shift_part import ShiftPart
    from app.models.shift_extra import ShiftExtra


class Doctor(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "doctors"
    __table_args__ = (
        Index("ix_doctors_crm", "crm", unique=True),
        Index("ix_doctors_active", "active"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    crm: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    has_rqe: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    career_start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    specialty: Mapped[str] = mapped_column(String(100), nullable=False, default="Clinica Medica")
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    doctor_type: Mapped[str] = mapped_column(String(30), nullable=False, default="plantonista")
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    @property
    def hour_rate_tier(self) -> str:
        return compute_hour_rate(self.has_rqe, self.career_start_date).tier

    @property
    def hour_rate(self) -> float:
        return compute_hour_rate(self.has_rqe, self.career_start_date).rate

    shift_parts: Mapped[list["ShiftPart"]] = relationship(
        back_populates="doctor",
        lazy="selectin",
    )
    shift_extras: Mapped[list["ShiftExtra"]] = relationship(
        back_populates="doctor",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Doctor(id={self.id}, name={self.name}, crm={self.crm})>"
