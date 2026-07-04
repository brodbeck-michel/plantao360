"""Financial Fact model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, DateTime, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_mixins import TimestampMixin
from app.domain.constants.financial_fact_type import FinancialFactType
from app.domain.constants.financial_fact_status import FinancialFactStatus

if TYPE_CHECKING:
    from app.models.period import Period
    from app.models.doctor import Doctor


class FinancialFact(Base, TimestampMixin):
    __tablename__ = "financial_facts"
    __table_args__ = (
        Index("ix_financial_facts_period_id", "period_id"),
        Index("ix_financial_facts_doctor_id", "doctor_id"),
        Index("ix_financial_facts_fact_type", "fact_type"),
        Index("ix_financial_facts_status", "status"),
        Index("ix_financial_facts_source_event", "source_event"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    period_id: Mapped[int] = mapped_column(
        ForeignKey("periods.id", ondelete="RESTRICT"),
        nullable=False,
    )
    doctor_id: Mapped[int] = mapped_column(
        ForeignKey("doctors.id", ondelete="RESTRICT"),
        nullable=False,
    )
    fact_type: Mapped[str] = mapped_column(
        String(30), nullable=False,
    )
    duration_minutes: Mapped[int] = mapped_column(
        Integer, nullable=False,
    )
    source_event: Mapped[str] = mapped_column(
        String(100), nullable=False,
    )
    source_id: Mapped[int] = mapped_column(
        Integer, nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=FinancialFactStatus.ACTIVE,
    )
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    revoked_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    period: Mapped["Period"] = relationship(lazy="selectin")
    doctor: Mapped["Doctor"] = relationship(lazy="selectin")

    @property
    def is_active(self) -> bool:
        return self.status == FinancialFactStatus.ACTIVE

    @property
    def is_revoked(self) -> bool:
        return self.status == FinancialFactStatus.REVOKED

    @property
    def duration_hours(self) -> float:
        return self.duration_minutes / 60.0

    def __repr__(self) -> str:
        return (
            f"<FinancialFact(id={self.id}, type={self.fact_type}, "
            f"doctor={self.doctor_id}, duration={self.duration_minutes}min, "
            f"status={self.status})>"
        )
