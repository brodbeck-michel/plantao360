"""Coverage Snapshot model."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, DateTime, ForeignKey, Index, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_mixins import TimestampMixin
from app.domain.constants.snapshot_status import SnapshotStatus

if TYPE_CHECKING:
    from app.models.period import Period


class CoverageSnapshot(Base, TimestampMixin):
    __tablename__ = "coverage_snapshots"
    __table_args__ = (
        Index("ix_coverage_snapshots_period_id", "period_id"),
        Index("ix_coverage_snapshots_status", "status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    period_id: Mapped[int] = mapped_column(
        ForeignKey("periods.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default=SnapshotStatus.ACTIVE,
    )
    total_assignments_completed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_extras_approved: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    total_duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    inconsistencies: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    consolidated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    period: Mapped["Period"] = relationship(lazy="selectin")

    @property
    def is_active(self) -> bool:
        return self.status == SnapshotStatus.ACTIVE

    @property
    def is_invalidated(self) -> bool:
        return self.status == SnapshotStatus.INVALIDATED

    @property
    def has_inconsistencies(self) -> bool:
        return bool(self.inconsistencies)

    def __repr__(self) -> str:
        return (
            f"<CoverageSnapshot(id={self.id}, period={self.period_id}, "
            f"assignments={self.total_assignments_completed}, "
            f"extras={self.total_extras_approved}, "
            f"status={self.status})>"
        )
