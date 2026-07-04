import pytest
from datetime import datetime, timedelta
from app.domain.value_objects.shift_time_range import ShiftTimeRange


def test_shift_time_range_valid():
    start = datetime(2025, 1, 1, 8, 0)
    end = datetime(2025, 1, 1, 20, 0)
    tr = ShiftTimeRange(start=start, end=end)
    assert tr.duration_minutes == 720
    assert tr.duration_hours == 12.0


def test_shift_time_range_invalid():
    start = datetime(2025, 1, 1, 20, 0)
    end = datetime(2025, 1, 1, 8, 0)
    with pytest.raises(ValueError, match="must be after"):
        ShiftTimeRange(start=start, end=end)


def test_shift_time_range_equal():
    start = datetime(2025, 1, 1, 8, 0)
    with pytest.raises(ValueError, match="must be after"):
        ShiftTimeRange(start=start, end=start)
