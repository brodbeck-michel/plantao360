import pytest
from app.domain.value_objects.assignment_duration import AssignmentDuration


def test_assignment_duration_valid():
    d = AssignmentDuration(minutes=480)
    assert d.hours == 8.0


def test_assignment_duration_invalid():
    with pytest.raises(ValueError, match="positive"):
        AssignmentDuration(minutes=0)


def test_assignment_duration_negative():
    with pytest.raises(ValueError, match="positive"):
        AssignmentDuration(minutes=-30)
