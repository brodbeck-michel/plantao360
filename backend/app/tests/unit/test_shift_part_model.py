import pytest
from datetime import date, time
from app.models.shift_part import ShiftPart
from app.domain.constants.assignment_status import AssignmentStatus


def test_shift_part_model_defaults():
    sp = ShiftPart()
    sp.shift_id = 1
    sp.doctor_id = 1
    sp.start_time = time(8, 0)
    sp.end_time = time(20, 0)
    sp.status = AssignmentStatus.PLANNED
    assert sp.status == AssignmentStatus.PLANNED
    assert sp.is_planned is True
    assert sp.is_confirmed is False
    assert sp.is_started is False
    assert sp.is_completed is False
    assert sp.is_cancelled is False


def test_shift_part_model_status_transitions():
    sp = ShiftPart()
    sp.shift_id = 1
    sp.doctor_id = 1
    sp.start_time = time(8, 0)
    sp.end_time = time(20, 0)
    sp.status = AssignmentStatus.CONFIRMED
    assert sp.is_confirmed is True

    sp.status = AssignmentStatus.STARTED
    assert sp.is_started is True

    sp.status = AssignmentStatus.COMPLETED
    assert sp.is_completed is True
