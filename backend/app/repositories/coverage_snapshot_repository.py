"""Coverage Snapshot repository."""

from sqlalchemy.orm import Session

from app.models.coverage_snapshot import CoverageSnapshot
from app.repositories.base.base_repository import BaseRepository


class CoverageSnapshotRepository(BaseRepository[CoverageSnapshot]):
    def __init__(self, session: Session):
        super().__init__(CoverageSnapshot, session)

    def get_active_by_period(self, period_id: int) -> CoverageSnapshot | None:
        return (
            self.session.query(CoverageSnapshot)
            .filter(
                CoverageSnapshot.period_id == period_id,
                CoverageSnapshot.status == "active",
            )
            .first()
        )

    def list_by_period(self, period_id: int) -> list[CoverageSnapshot]:
        return (
            self.session.query(CoverageSnapshot)
            .filter(CoverageSnapshot.period_id == period_id)
            .all()
        )
