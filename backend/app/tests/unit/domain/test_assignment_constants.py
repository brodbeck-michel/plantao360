import pytest
from app.domain.constants.assignment_status import AssignmentStatus


def test_assignment_status_values():
    assert AssignmentStatus.PLANNED == "planned"
    assert AssignmentStatus.CONFIRMED == "confirmed"
    assert AssignmentStatus.STARTED == "started"
    assert AssignmentStatus.COMPLETED == "completed"
    assert AssignmentStatus.CANCELLED == "cancelled"
    assert set(AssignmentStatus.values()) == {"planned", "confirmed", "started", "completed", "cancelled"}


def test_assignment_status_choices():
    choices = AssignmentStatus.choices()
    assert len(choices) == 5
    assert ("planned", "PLANNED") in choices
