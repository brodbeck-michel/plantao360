import pytest
from datetime import date, time, datetime, timedelta
from app.domain.constants.shift_types import ShiftType
from app.domain.constants.shift_status import ShiftStatus


def test_shift_status_values():
    assert ShiftStatus.SCHEDULED == "scheduled"
    assert ShiftStatus.IN_PROGRESS == "in_progress"
    assert ShiftStatus.COMPLETED == "completed"
    assert ShiftStatus.CANCELLED == "cancelled"
    assert set(ShiftStatus.values()) == {"scheduled", "in_progress", "completed", "cancelled"}


def test_shift_type_values():
    assert ShiftType.T1 == "T1"
    assert ShiftType.T2 == "T2"
    assert ShiftType.T3 == "T3"
    assert ShiftType.R1 == "R1"
    assert ShiftType.R2 == "R2"
    assert set(ShiftType.values()) == {"T1", "T2", "T3", "R1", "R2"}
