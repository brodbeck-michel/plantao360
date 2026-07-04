import pytest
from datetime import datetime, timezone
from app.domain.metrics.period_metrics import PeriodMetrics


class TestPeriodMetrics:
    def test_create_metrics(self):
        m = PeriodMetrics(
            period_id=1, year=2026, month=6, status="draft",
        )
        assert m.period_id == 1
        assert m.number_of_shifts == 0
        assert m.total_hours == 0.0
        assert m.total_amount == 0.0

    def test_to_dict(self):
        m = PeriodMetrics(
            period_id=1, year=2026, month=6, status="closed",
            number_of_shifts=10,
            number_of_doctors=5,
            number_of_extras=2,
            total_hours=240.0,
            total_amount=15000.0,
            opened_at=datetime(2026, 6, 1, tzinfo=timezone.utc),
            closed_at=datetime(2026, 6, 30, tzinfo=timezone.utc),
        )
        d = m.to_dict()
        assert d["period_id"] == 1
        assert d["number_of_shifts"] == 10
        assert d["number_of_doctors"] == 5
        assert d["number_of_extras"] == 2
        assert d["total_hours"] == 240.0
        assert d["total_amount"] == 15000.0
        assert d["opened_at"] is not None
        assert d["closed_at"] is not None

    def test_to_dict_none_dates(self):
        m = PeriodMetrics(
            period_id=1, year=2026, month=6, status="draft",
        )
        d = m.to_dict()
        assert d["opened_at"] is None
        assert d["closed_at"] is None

    def test_metrics_is_mutable(self):
        m = PeriodMetrics(
            period_id=1, year=2026, month=6, status="draft",
        )
        m.number_of_shifts = 5
        assert m.number_of_shifts == 5
