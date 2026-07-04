from app.repositories.period_repository import PeriodRepository
from app.models.period import Period
from app.domain.constants.period_status import PeriodStatus


def test_repository_create(db_session):
    repo = PeriodRepository(db_session)
    period = Period(year=2026, month=6, status=PeriodStatus.DRAFT)
    created = repo.create(period)
    db_session.commit()
    assert created.id is not None
    assert created.year == 2026
    assert created.month == 6


def test_repository_get_by_id(db_session):
    repo = PeriodRepository(db_session)
    period = Period(year=2026, month=6, status=PeriodStatus.DRAFT)
    db_session.add(period)
    db_session.commit()
    db_session.expire_all()
    found = repo.get_by_id(period.id)
    assert found is not None
    assert found.year == 2026


def test_repository_get_by_year_month(db_session):
    repo = PeriodRepository(db_session)
    period = Period(year=2026, month=6, status=PeriodStatus.DRAFT)
    db_session.add(period)
    db_session.commit()
    db_session.expire_all()
    found = repo.get_by_year_month(2026, 6)
    assert found is not None
    assert found.year == 2026
    assert found.month == 6


def test_repository_get_by_year_month_not_found(db_session):
    repo = PeriodRepository(db_session)
    found = repo.get_by_year_month(2099, 12)
    assert found is None


def test_repository_get_current_period(db_session):
    repo = PeriodRepository(db_session)
    period = Period(year=2026, month=6, status=PeriodStatus.DRAFT)
    db_session.add(period)
    db_session.commit()
    db_session.expire_all()
    current = repo.get_current_period()
    assert current is not None
    assert current.status != PeriodStatus.PAID


def test_repository_exists_by_year_month(db_session):
    repo = PeriodRepository(db_session)
    period = Period(year=2026, month=6, status=PeriodStatus.DRAFT)
    db_session.add(period)
    db_session.commit()
    assert repo.exists_by_year_month(2026, 6) is True
    assert repo.exists_by_year_month(2099, 12) is False


def test_repository_exists_by_year_month_exclude_id(db_session):
    repo = PeriodRepository(db_session)
    period = Period(year=2026, month=6, status=PeriodStatus.DRAFT)
    db_session.add(period)
    db_session.commit()
    assert repo.exists_by_year_month(2026, 6, exclude_id=period.id) is False
    assert repo.exists_by_year_month(2026, 6, exclude_id=999) is True


def test_repository_search(db_session):
    repo = PeriodRepository(db_session)
    db_session.add(Period(year=2026, month=6, status=PeriodStatus.DRAFT))
    db_session.commit()
    db_session.expire_all()
    results = repo.search(year=2026)
    assert len(results) >= 1


def test_repository_count_filtered(db_session):
    repo = PeriodRepository(db_session)
    db_session.add(Period(year=2026, month=6, status=PeriodStatus.DRAFT))
    db_session.add(Period(year=2026, month=7, status=PeriodStatus.CLOSED))
    db_session.commit()
    assert repo.count_filtered(status="draft") >= 1
    assert repo.count_filtered(status="closed") >= 1


def test_repository_update(db_session):
    repo = PeriodRepository(db_session)
    period = Period(year=2026, month=6, status=PeriodStatus.DRAFT)
    db_session.add(period)
    db_session.commit()
    db_session.expire_all()
    period.status = PeriodStatus.CLOSED
    updated = repo.update(period)
    db_session.commit()
    assert updated.status == PeriodStatus.CLOSED


def test_repository_count(db_session):
    repo = PeriodRepository(db_session)
    initial_count = repo.count()
    db_session.add(Period(year=2099, month=12, status=PeriodStatus.DRAFT))
    db_session.commit()
    assert repo.count() == initial_count + 1
