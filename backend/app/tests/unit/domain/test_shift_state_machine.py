import pytest
from unittest.mock import MagicMock
from app.services.shift_service import ShiftStateMachine
from app.domain.constants.shift_status import ShiftStatus


def _make_shift(status: str):
    shift = MagicMock()
    shift.status = status
    shift.before_transition = MagicMock()
    shift.after_transition = MagicMock()
    return shift


def test_shift_state_machine_start():
    shift = _make_shift(ShiftStatus.SCHEDULED)
    sm = ShiftStateMachine(shift)
    sm.start()
    assert shift.status == ShiftStatus.IN_PROGRESS
    shift.before_transition.assert_called_once()
    shift.after_transition.assert_called_once()


def test_shift_state_machine_complete():
    shift = _make_shift(ShiftStatus.IN_PROGRESS)
    sm = ShiftStateMachine(shift)
    sm.complete()
    assert shift.status == ShiftStatus.COMPLETED


def test_shift_state_machine_cancel_scheduled():
    shift = _make_shift(ShiftStatus.SCHEDULED)
    sm = ShiftStateMachine(shift)
    sm.cancel()
    assert shift.status == ShiftStatus.CANCELLED


def test_shift_state_machine_cancel_in_progress():
    shift = _make_shift(ShiftStatus.IN_PROGRESS)
    sm = ShiftStateMachine(shift)
    sm.cancel()
    assert shift.status == ShiftStatus.CANCELLED


def test_shift_state_machine_cancel_completed_fails():
    shift = _make_shift(ShiftStatus.COMPLETED)
    sm = ShiftStateMachine(shift)
    with pytest.raises(ValueError, match="Cannot cancel"):
        sm.cancel()


def test_shift_state_machine_cancel_cancelled_fails():
    shift = _make_shift(ShiftStatus.CANCELLED)
    sm = ShiftStateMachine(shift)
    with pytest.raises(ValueError, match="Cannot cancel"):
        sm.cancel()


def test_shift_state_machine_start_wrong_status_fails():
    shift = _make_shift(ShiftStatus.IN_PROGRESS)
    sm = ShiftStateMachine(shift)
    with pytest.raises(ValueError, match="Cannot transition"):
        sm.start()


def test_shift_state_machine_complete_wrong_status_fails():
    shift = _make_shift(ShiftStatus.SCHEDULED)
    sm = ShiftStateMachine(shift)
    with pytest.raises(ValueError, match="Cannot transition"):
        sm.complete()
