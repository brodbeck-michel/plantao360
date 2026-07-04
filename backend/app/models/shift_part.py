from datetime import time
from typing import TYPE_CHECKING

from sqlalchemy import Time, String, Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_mixins import TimestampMixin
from app.domain.constants.assignment_status import AssignmentStatus

if TYPE_CHECKING:
    from app.models.shift import Shift
    from app.models.doctor import Doctor


class ShiftPart(Base, TimestampMixin):
    __tablename__ = "shift_parts"
    __table_args__ = (
        Index("ix_shift_parts_shift_id", "shift_id"),
        Index("ix_shift_parts_doctor_id", "doctor_id"),
        Index("ix_shift_parts_doctor_date", "doctor_id", "shift_id"),
        Index("ix_shift_parts_status", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    shift_id: Mapped[int] = mapped_column(
        ForeignKey("shifts.id", ondelete="CASCADE"),
        nullable=False,
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id", ondelete="RESTRICT"),
        nullable=False,
    )
    start_time: Mapped[time] = mapped_column(Time, nullable=False)
    end_time: Mapped[time] = mapped_column(Time, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=AssignmentStatus.PLANNED
    )
    duration_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)

    shift: Mapped["Shift"] = relationship(
        back_populates="shift_parts",
        lazy="selectin",
    )
    doctor: Mapped["Doctor"] = relationship(
        back_populates="shift_parts",
        lazy="selectin",
    )

    @property
    def is_planned(self) -> bool:
        return self.status == AssignmentStatus.PLANNED

    @property
    def is_confirmed(self) -> bool:
        return self.status == AssignmentStatus.CONFIRMED

    @property
    def is_started(self) -> bool:
        return self.status == AssignmentStatus.STARTED

    @property
    def is_completed(self) -> bool:
        return self.status == AssignmentStatus.COMPLETED

    @property
    def is_cancelled(self) -> bool:
        return self.status == AssignmentStatus.CANCELLED

    def before_transition(self, from_status: str, to_status: str) -> None:
        pass

    def after_transition(self, from_status: str, to_status: str) -> None:
        pass

    def __repr__(self) -> str:
        return f"<ShiftPart(id={self.id}, doctor_id={self.doctor_id}, start={self.start_time}, end={self.end_time}, status={self.status})>"
