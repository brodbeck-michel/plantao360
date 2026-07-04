from app.models.period import Period
from app.domain.constants.period_status import PeriodStatus


def test_period_repr(db_session):
    period = Period(year=2026, month=6, status=PeriodStatus.DRAFT)
    db_session.add(period)
    db_session.commit()
    assert "2026" in repr(period)
    assert "6" in repr(period)
    assert "draft" in repr(period)


def test_period_default_status(db_session):
    period = Period(year=2026, month=7)
    db_session.add(period)
    db_session.commit()
    assert period.status == PeriodStatus.DRAFT


def test_period_status_values():
    assert PeriodStatus.DRAFT == "draft"
    assert PeriodStatus.CLOSED == "closed"
    assert PeriodStatus.PAID == "paid"
    assert len(PeriodStatus.values()) == 3
