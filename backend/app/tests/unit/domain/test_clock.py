import pytest
from datetime import datetime, timezone
from app.common.clock import SystemClock, FutureClock


class TestSystemClock:
    def test_now_returns_datetime(self):
        clock = SystemClock()
        now = clock.now()
        assert isinstance(now, datetime)
        assert now.tzinfo is not None

    def test_now_is_utc(self):
        clock = SystemClock()
        now = clock.now()
        assert now.tzinfo == timezone.utc


class TestFutureClock:
    def test_returns_fixed_time(self):
        fixed = datetime(2030, 1, 1, tzinfo=timezone.utc)
        clock = FutureClock(fixed)
        assert clock.now() == fixed

    def test_returns_same_time_each_call(self):
        fixed = datetime(2030, 6, 15, 12, 0, 0, tzinfo=timezone.utc)
        clock = FutureClock(fixed)
        assert clock.now() == clock.now()
