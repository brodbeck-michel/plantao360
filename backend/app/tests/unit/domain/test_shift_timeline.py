import pytest
from datetime import datetime
from app.domain.value_objects.shift_timeline import ShiftTimeline


def test_shift_timeline_empty():
    tl = ShiftTimeline()
    assert tl.has_schedule is False
    assert tl.has_actual is False
    assert tl.is_active is False
    assert tl.planned_duration_minutes() is None
    assert tl.actual_duration_minutes() is None


def test_shift_timeline_with_schedule():
    tl = ShiftTimeline(
        scheduled_start=datetime(2025, 1, 1, 8, 0),
        scheduled_end=datetime(2025, 1, 1, 20, 0),
    )
    assert tl.has_schedule is True
    assert tl.has_actual is False
    assert tl.planned_duration_minutes() == 720


def test_shift_timeline_record_start():
    tl = ShiftTimeline()
    now = datetime(2025, 1, 1, 8, 0)
    tl.record_start(now)
    assert tl.is_active is True
    assert tl.has_actual is False


def test_shift_timeline_record_end():
    tl = ShiftTimeline()
    start = datetime(2025, 1, 1, 8, 0)
    end = datetime(2025, 1, 1, 20, 0)
    tl.record_start(start)
    tl.record_end(end)
    assert tl.has_actual is True
    assert tl.is_active is False
    assert tl.actual_duration_minutes() == 720


def test_shift_timeline_end_without_start():
    tl = ShiftTimeline()
    with pytest.raises(ValueError, match="never started"):
        tl.record_end(datetime(2025, 1, 1, 20, 0))
