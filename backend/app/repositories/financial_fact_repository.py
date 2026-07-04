"""Financial Fact repository."""

from sqlalchemy.orm import Session

from app.models.financial_fact import FinancialFact
from app.repositories.base.base_repository import BaseRepository


class FinancialFactRepository(BaseRepository[FinancialFact]):
    def __init__(self, session: Session):
        super().__init__(FinancialFact, session)

    def list_by_period(self, period_id: int) -> list[FinancialFact]:
        return (
            self.session.query(FinancialFact)
            .filter(FinancialFact.period_id == period_id)
            .all()
        )

    def list_by_doctor(self, doctor_id: int) -> list[FinancialFact]:
        return (
            self.session.query(FinancialFact)
            .filter(FinancialFact.doctor_id == doctor_id)
            .all()
        )

    def list_active_by_period(self, period_id: int) -> list[FinancialFact]:
        return (
            self.session.query(FinancialFact)
            .filter(
                FinancialFact.period_id == period_id,
                FinancialFact.status == "active",
            )
            .all()
        )
