from typing import TYPE_CHECKING

from sqlalchemy import String, Numeric, Boolean, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_mixins import TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.shift_part import ShiftPart
    from app.models.shift_extra import ShiftExtra


class Doctor(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "doctors"
    __table_args__ = (
        CheckConstraint("hour_rate >= 0", name="ck_doctor_hour_rate_positive"),
        Index("ix_doctors_crm", "crm", unique=True),
        Index("ix_doctors_active", "active"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    crm: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    hour_rate: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    specialty: Mapped[str] = mapped_column(String(100), nullable=False, default="Clinica Medica")
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    doctor_type: Mapped[str] = mapped_column(String(30), nullable=False, default="plantonista")
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

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
