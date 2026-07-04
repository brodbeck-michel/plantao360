import pytest
from datetime import time
from app.domain.value_objects.assignment_timeline import AssignmentTimeline


def test_assignment_timeline_valid():
    tl = AssignmentTimeline(start_time=time(8, 0), end_time=time(20, 0))
    assert tl.duration_minutes == 720
    assert tl.duration_hours == 12.0


def test_assignment_timeline_invalid():
    with pytest.raises(ValueError, match="must be after"):
        AssignmentTimeline(start_time=time(20, 0), end_time=time(8, 0))


def test_assignment_timeline_equal():
    with pytest.raises(ValueError, match="must be after"):
        AssignmentTimeline(start_time=time(8, 0), end_time=time(8, 0))


def test_assignment_timeline_overlaps():
    tl1 = AssignmentTimeline(start_time=time(8, 0), end_time=time(20, 0))
    tl2 = AssignmentTimeline(start_time=time(14, 0), end_time=time(22, 0))
    assert tl1.overlaps(tl2) is True


def test_assignment_timeline_no_overlap():
    tl1 = AssignmentTimeline(start_time=time(8, 0), end_time=time(14, 0))
    tl2 = AssignmentTimeline(start_time=time(14, 0), end_time=time(20, 0))
    assert tl1.overlaps(tl2) is False
