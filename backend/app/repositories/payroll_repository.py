"""Payroll repository."""

from sqlalchemy.orm import Session

from app.models.payroll import Payroll
from app.domain.constants.payroll_status import PayrollStatus


class PayrollRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, payroll_id: int) -> Payroll | None:
        return self.session.query(Payroll).filter(Payroll.id == payroll_id).first()

    def get_by_period(self, period_id: int) -> Payroll | None:
        return self.session.query(Payroll).filter(Payroll.period_id == period_id).first()

    def get_active_by_period(self, period_id: int) -> Payroll | None:
        return (
            self.session.query(Payroll)
            .filter(
                Payroll.period_id == period_id,
                Payroll.status != PayrollStatus.ARCHIVED,
            )
            .order_by(Payroll.current_version.desc())
            .first()
        )

    def create(self, payroll: Payroll) -> Payroll:
        self.session.add(payroll)
        self.session.flush()
        return payroll

    def update(self, payroll: Payroll) -> Payroll:
        self.session.merge(payroll)
        self.session.flush()
        return payroll

    def list(
        self,
        skip: int = 0,
        limit: int = 20,
        period_id: int | None = None,
        year_month: str | None = None,
        status: str | None = None,
        sort_by: str = "created_at",
        sort_direction: str = "desc",
    ) -> list[Payroll]:
        query = self.session.query(Payroll)

        if period_id is not None:
            query = query.filter(Payroll.period_id == period_id)
        if year_month is not None:
            query = query.filter(Payroll.year_month == year_month)
        if status is not None:
            query = query.filter(Payroll.status == status)

        sort_column = getattr(Payroll, sort_by, Payroll.created_at)
        if sort_direction == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        return query.offset(skip).limit(limit).all()

    def count(
        self,
        period_id: int | None = None,
        year_month: str | None = None,
        status: str | None = None,
    ) -> int:
        query = self.session.query(Payroll)

        if period_id is not None:
            query = query.filter(Payroll.period_id == period_id)
        if year_month is not None:
            query = query.filter(Payroll.year_month == year_month)
        if status is not None:
            query = query.filter(Payroll.status == status)

        return query.count()
