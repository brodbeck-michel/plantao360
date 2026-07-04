"""Financial Snapshot repository."""

from sqlalchemy.orm import Session

from app.models.financial_snapshot import FinancialSnapshot
from app.repositories.base.base_repository import BaseRepository


class FinancialSnapshotRepository(BaseRepository[FinancialSnapshot]):
    def __init__(self, session: Session):
        super().__init__(FinancialSnapshot, session)

    def get_active_by_period(self, period_id: int) -> FinancialSnapshot | None:
        return (
            self.session.query(FinancialSnapshot)
            .filter(
                FinancialSnapshot.period_id == period_id,
                FinancialSnapshot.status == "active",
            )
            .first()
        )

    def list_by_period(self, period_id: int) -> list[FinancialSnapshot]:
        return (
            self.session.query(FinancialSnapshot)
            .filter(FinancialSnapshot.period_id == period_id)
            .all()
        )
