from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, String, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_mixins import TimestampMixin
from app.domain.constants.shift_types import ShiftType
from app.domain.constants.shift_status import ShiftStatus

if TYPE_CHECKING:
    from app.models.period import Period
    from app.models.shift_part import ShiftPart
    from app.models.shift_extra import ShiftExtra


class Shift(Base, TimestampMixin):
    __tablename__ = "shifts"
    __table_args__ = (
        UniqueConstraint("period_id", "shift_date", "shift_type", name="uq_shift_period_date_type"),
        Index("ix_shifts_period_id", "period_id"),
        Index("ix_shifts_shift_date", "shift_date"),
        Index("ix_shifts_status", "status"),
        Index("ix_shifts_period_date", "period_id", "shift_date"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    period_id: Mapped[int] = mapped_column(
        ForeignKey("periods.id", ondelete="CASCADE"),
        nullable=False,
    )
    shift_date: Mapped[date] = mapped_column(Date, nullable=False)
    shift_type: Mapped[str] = mapped_column(String(5), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=ShiftStatus.SCHEDULED)

    scheduled_start: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    scheduled_end: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    actual_start: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    actual_end: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    total_duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    doctor_count: Mapped[int | None] = mapped_column(Integer, nullable=True)

    period: Mapped["Period"] = relationship(
        back_populates="shifts",
        lazy="selectin",
    )
    shift_parts: Mapped[list["ShiftPart"]] = relationship(
        back_populates="shift",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    shift_extras: Mapped[list["ShiftExtra"]] = relationship(
        back_populates="shift",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    @property
    def is_scheduled(self) -> bool:
        return self.status == ShiftStatus.SCHEDULED

    @property
    def is_in_progress(self) -> bool:
        return self.status == ShiftStatus.IN_PROGRESS

    @property
    def is_completed(self) -> bool:
        return self.status == ShiftStatus.COMPLETED

    @property
    def is_cancelled(self) -> bool:
        return self.status == ShiftStatus.CANCELLED

    def __repr__(self) -> str:
        return f"<Shift(id={self.id}, date={self.shift_date}, type={self.shift_type}, status={self.status})>"
