import pytest
from unittest.mock import MagicMock
from app.services.assignment_service import AssignmentStateMachine
from app.domain.constants.assignment_status import AssignmentStatus


def _make_assignment(status: str):
    a = MagicMock()
    a.status = status
    a.before_transition = MagicMock()
    a.after_transition = MagicMock()
    return a


def test_assignment_state_machine_confirm():
    a = _make_assignment(AssignmentStatus.PLANNED)
    sm = AssignmentStateMachine(a)
    sm.confirm()
    assert a.status == AssignmentStatus.CONFIRMED


def test_assignment_state_machine_start():
    a = _make_assignment(AssignmentStatus.CONFIRMED)
    sm = AssignmentStateMachine(a)
    sm.start()
    assert a.status == AssignmentStatus.STARTED


def test_assignment_state_machine_complete():
    a = _make_assignment(AssignmentStatus.STARTED)
    sm = AssignmentStateMachine(a)
    sm.complete()
    assert a.status == AssignmentStatus.COMPLETED


def test_assignment_state_machine_cancel_planned():
    a = _make_assignment(AssignmentStatus.PLANNED)
    sm = AssignmentStateMachine(a)
    sm.cancel()
    assert a.status == AssignmentStatus.CANCELLED


def test_assignment_state_machine_cancel_confirmed():
    a = _make_assignment(AssignmentStatus.CONFIRMED)
    sm = AssignmentStateMachine(a)
    sm.cancel()
    assert a.status == AssignmentStatus.CANCELLED


def test_assignment_state_machine_cancel_completed_fails():
    a = _make_assignment(AssignmentStatus.COMPLETED)
    sm = AssignmentStateMachine(a)
    with pytest.raises(ValueError, match="Cannot cancel"):
        sm.cancel()


def test_assignment_state_machine_confirm_wrong_status_fails():
    a = _make_assignment(AssignmentStatus.CONFIRMED)
    sm = AssignmentStateMachine(a)
    with pytest.raises(ValueError, match="Cannot transition"):
        sm.confirm()


def test_assignment_state_machine_start_wrong_status_fails():
    a = _make_assignment(AssignmentStatus.PLANNED)
    sm = AssignmentStateMachine(a)
    with pytest.raises(ValueError, match="Cannot transition"):
        sm.start()


def test_assignment_state_machine_complete_wrong_status_fails():
    a = _make_assignment(AssignmentStatus.CONFIRMED)
    sm = AssignmentStateMachine(a)
    with pytest.raises(ValueError, match="Cannot transition"):
        sm.complete()
