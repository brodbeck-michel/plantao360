from typing import TYPE_CHECKING

from sqlalchemy import Text, Integer, String, ForeignKey, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_mixins import TimestampMixin
from app.domain.constants.extra_status import ExtraStatus

if TYPE_CHECKING:
    from app.models.shift import Shift
    from app.models.doctor import Doctor


class ShiftExtra(Base, TimestampMixin):
    __tablename__ = "shift_extras"
    __table_args__ = (
        CheckConstraint(
            "duration_minutes > 0", name="ck_shift_extra_duration_positive"
        ),
        Index("ix_shift_extras_shift_id", "shift_id"),
        Index("ix_shift_extras_doctor_id", "doctor_id"),
        Index("ix_shift_extras_status", "status"),
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
    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    justification: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=ExtraStatus.PENDING
    )

    shift: Mapped["Shift"] = relationship(
        back_populates="shift_extras",
        lazy="selectin",
    )
    doctor: Mapped["Doctor"] = relationship(
        back_populates="shift_extras",
        lazy="selectin",
    )

    @property
    def duration_hours(self) -> float:
        return self.duration_minutes / 60.0

    @property
    def is_pending(self) -> bool:
        return self.status == ExtraStatus.PENDING

    @property
    def is_approved(self) -> bool:
        return self.status == ExtraStatus.APPROVED

    @property
    def is_rejected(self) -> bool:
        return self.status == ExtraStatus.REJECTED

    @property
    def is_cancelled(self) -> bool:
        return self.status == ExtraStatus.CANCELLED

    def __repr__(self) -> str:
        return f"<ShiftExtra(id={self.id}, duration={self.duration_minutes}min, status={self.status})>"
