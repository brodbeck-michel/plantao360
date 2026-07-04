"""Financial Snapshot model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_mixins import TimestampMixin
from app.domain.constants.snapshot_status import SnapshotStatus

if TYPE_CHECKING:
    from app.models.period import Period


class FinancialSnapshot(Base, TimestampMixin):
    __tablename__ = "financial_snapshots"
    __table_args__ = (
        Index("ix_financial_snapshots_period_id", "period_id"),
        Index("ix_financial_snapshots_status", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    period_id: Mapped[int] = mapped_column(
        ForeignKey("periods.id", ondelete="RESTRICT"),
        nullable=False,
    )
    coverage_snapshot_id: Mapped[int] = mapped_column(
        ForeignKey("coverage_snapshots.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=SnapshotStatus.ACTIVE,
    )
    total_facts: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at_snapshot: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    period: Mapped["Period"] = relationship(lazy="selectin")
    coverage_snapshot: Mapped["CoverageSnapshot"] = relationship(lazy="selectin")

    @property
    def is_active(self) -> bool:
        return self.status == SnapshotStatus.ACTIVE

    @property
    def is_invalidated(self) -> bool:
        return self.status == SnapshotStatus.INVALIDATED

    def __repr__(self) -> str:
        return (
            f"<FinancialSnapshot(id={self.id}, period={self.period_id}, "
            f"facts={self.total_facts}, "
            f"duration={self.total_duration_minutes}min, "
            f"status={self.status})>"
        )
