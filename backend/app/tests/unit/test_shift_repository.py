from datetime import date

from app.repositories.shift_repository import ShiftRepository
from app.models.shift import Shift
from app.domain.constants.shift_status import ShiftStatus


def _make_shift():
    return Shift(
        period_id=1,
        shift_date=date(2025, 1, 15),
        shift_type="T1",
        status=ShiftStatus.SCHEDULED,
    )


def test_repository_create(db_session):
    repo = ShiftRepository(db_session)
    entity = _make_shift()
    created = repo.create(entity)
    db_session.commit()
    assert created.id is not None


def test_repository_get_by_id(db_session):
    repo = ShiftRepository(db_session)
    entity = _make_shift()
    db_session.add(entity)
    db_session.commit()
    db_session.expire_all()
    found = repo.get_by_id(entity.id)
    assert found is not None


def test_repository_list(db_session):
    repo = ShiftRepository(db_session)
    db_session.add(_make_shift())
    db_session.commit()
    db_session.expire_all()
    items = repo.list()
    assert len(items) >= 1


def test_repository_search(db_session):
    repo = ShiftRepository(db_session)
    db_session.add(_make_shift())
    db_session.commit()
    db_session.expire_all()
    results = repo.search()
    assert len(results) >= 1


def test_repository_count_filtered(db_session):
    repo = ShiftRepository(db_session)
    db_session.add(_make_shift())
    db_session.commit()
    assert repo.count_filtered() >= 1


def test_repository_soft_delete(db_session):
    repo = ShiftRepository(db_session)
    entity = _make_shift()
    db_session.add(entity)
    db_session.commit()
    db_session.expire_all()
    result = repo.soft_delete(entity.id)
    assert result is True
    db_session.expire_all()
    updated = repo.get_by_id(entity.id)
    assert updated.status == ShiftStatus.CANCELLED


def test_repository_count(db_session):
    repo = ShiftRepository(db_session)
    initial_count = repo.count()
    db_session.add(_make_shift())
    db_session.commit()
    assert repo.count() == initial_count + 1
