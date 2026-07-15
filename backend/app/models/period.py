from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, CheckConstraint, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_mixins import TimestampMixin
from app.domain.constants.period_status import PeriodStatus

if TYPE_CHECKING:
    from app.models.shift import Shift


class Period(Base, TimestampMixin):
    __tablename__ = "periods"
    __table_args__ = (
        UniqueConstraint("year", "month", name="uq_period_year_month"),
        CheckConstraint("month BETWEEN 1 AND 12", name="ck_period_month_range"),
        CheckConstraint("year BETWEEN 2000 AND 2100", name="ck_period_year_range"),
        Index("ix_periods_status", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    month: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default=PeriodStatus.DRAFT,
        server_default=PeriodStatus.DRAFT,
    )

    shifts: Mapped[list["Shift"]] = relationship(
        back_populates="period",
        lazy="selectin",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Period(id={self.id}, year={self.year}, month={self.month}, status={self.status})>"
