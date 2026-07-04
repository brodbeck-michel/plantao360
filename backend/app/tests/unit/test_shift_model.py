import pytest
from app.models.shift import Shift
from app.domain.constants.shift_status import ShiftStatus
from datetime import date, datetime


def test_shift_model_defaults():
    shift = Shift()
    shift.period_id = 1
    shift.shift_date = date(2025, 1, 15)
    shift.shift_type = "T1"
    shift.status = ShiftStatus.SCHEDULED
    assert shift.status == ShiftStatus.SCHEDULED
    assert shift.is_scheduled is True
    assert shift.is_in_progress is False
    assert shift.is_completed is False
    assert shift.is_cancelled is False


def test_shift_model_status_transitions():
    shift = Shift()
    shift.period_id = 1
    shift.shift_date = date(2025, 1, 15)
    shift.shift_type = "T1"
    shift.status = ShiftStatus.IN_PROGRESS
    assert shift.is_in_progress is True

    shift.status = ShiftStatus.COMPLETED
    assert shift.is_completed is True

    shift.status = ShiftStatus.CANCELLED
    assert shift.is_cancelled is True
