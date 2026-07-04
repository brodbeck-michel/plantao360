"""Payroll database model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, DateTime, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_mixins import TimestampMixin
from app.domain.constants.payroll_status import PayrollStatus

if TYPE_CHECKING:
    from app.models.period import Period


class Payroll(Base, TimestampMixin):
    __tablename__ = "payrolls"
    __table_args__ = (
        Index("ix_payrolls_period_id", "period_id"),
        Index("ix_payrolls_year_month", "year_month"),
        Index("ix_payrolls_status", "status"),
        Index("ix_payrolls_version", "current_version"),
        Index("ix_payrolls_period_version", "period_id", "current_version"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    period_id: Mapped[int] = mapped_column(
        ForeignKey("periods.id", ondelete="RESTRICT"),
        nullable=False,
    )
    year_month: Mapped[str] = mapped_column(String(6), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=PayrollStatus.DRAFT
    )
    current_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    created_by: Mapped[str] = mapped_column(String(100), nullable=False, default="system")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    reopen_count: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    reopen_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    period: Mapped["Period"] = relationship(
        back_populates="payrolls",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return (
            f"<Payroll(id={self.id}, year_month={self.year_month}, "
            f"status={self.status}, version={self.current_version})>"
        )
