import pytest
from datetime import datetime, timezone
from app.domain.snapshots.period_snapshot import PeriodSnapshot
from app.domain.constants.period_status import PeriodStatus


class TestPeriodSnapshot:
    def test_create_snapshot(self):
        snap = PeriodSnapshot(
            id=1, year=2026, month=6, status=PeriodStatus.DRAFT,
            created_at=datetime(2026, 6, 1, tzinfo=timezone.utc),
            updated_at=datetime(2026, 6, 26, tzinfo=timezone.utc),
        )
        assert snap.id == 1
        assert snap.year == 2026
        assert snap.month == 6
        assert snap.status == PeriodStatus.DRAFT

    def test_snapshot_is_frozen(self):
        snap = PeriodSnapshot(
            id=1, year=2026, month=6, status=PeriodStatus.DRAFT,
            created_at=None, updated_at=None,
        )
        with pytest.raises(AttributeError):
            snap.id = 2

    def test_to_dict(self):
        snap = PeriodSnapshot(
            id=1, year=2026, month=6, status=PeriodStatus.CLOSED,
            created_at=datetime(2026, 6, 1, tzinfo=timezone.utc),
            updated_at=datetime(2026, 6, 26, tzinfo=timezone.utc),
            number_of_shifts=5,
            number_of_doctors=3,
            total_hours=120.5,
        )
        d = snap.to_dict()
        assert d["id"] == 1
        assert d["number_of_shifts"] == 5
        assert d["total_hours"] == 120.5
        assert d["created_at"] is not None

    def test_to_dict_none_dates(self):
        snap = PeriodSnapshot(
            id=1, year=2026, month=6, status=PeriodStatus.DRAFT,
            created_at=None, updated_at=None,
        )
        d = snap.to_dict()
        assert d["created_at"] is None
        assert d["updated_at"] is None

    def test_defaults(self):
        snap = PeriodSnapshot(
            id=1, year=2026, month=6, status=PeriodStatus.DRAFT,
            created_at=None, updated_at=None,
        )
        assert snap.number_of_shifts == 0
        assert snap.number_of_doctors == 0
        assert snap.total_hours == 0.0
