import pytest
from unittest.mock import MagicMock
from app.services.assignment_service import AssignmentRules
from app.domain.constants.assignment_status import AssignmentStatus


def _make_assignment(**kwargs):
    a = MagicMock()
    a.status = kwargs.get("status", AssignmentStatus.PLANNED)
    a.start_time = kwargs.get("start_time")
    a.end_time = kwargs.get("end_time")
    return a


def test_validate_can_confirm_planned():
    a = _make_assignment(status=AssignmentStatus.PLANNED)
    rules = AssignmentRules(a)
    assert rules.validate_can_confirm() == []


def test_validate_can_confirm_wrong_status():
    a = _make_assignment(status=AssignmentStatus.CONFIRMED)
    rules = AssignmentRules(a)
    errors = rules.validate_can_confirm()
    assert len(errors) == 1


def test_validate_can_start_confirmed():
    a = _make_assignment(status=AssignmentStatus.CONFIRMED)
    rules = AssignmentRules(a)
    assert rules.validate_can_start() == []


def test_validate_can_start_wrong_status():
    a = _make_assignment(status=AssignmentStatus.PLANNED)
    rules = AssignmentRules(a)
    errors = rules.validate_can_start()
    assert len(errors) == 1


def test_validate_can_complete_started():
    a = _make_assignment(status=AssignmentStatus.STARTED)
    rules = AssignmentRules(a)
    assert rules.validate_can_complete() == []


def test_validate_can_complete_wrong_status():
    a = _make_assignment(status=AssignmentStatus.CONFIRMED)
    rules = AssignmentRules(a)
    errors = rules.validate_can_complete()
    assert len(errors) == 1


def test_validate_can_cancel_planned():
    a = _make_assignment(status=AssignmentStatus.PLANNED)
    rules = AssignmentRules(a)
    assert rules.validate_can_cancel() == []


def test_validate_can_cancel_confirmed():
    a = _make_assignment(status=AssignmentStatus.CONFIRMED)
    rules = AssignmentRules(a)
    assert rules.validate_can_cancel() == []


def test_validate_can_cancel_started_fails():
    a = _make_assignment(status=AssignmentStatus.STARTED)
    rules = AssignmentRules(a)
    errors = rules.validate_can_cancel()
    assert len(errors) == 1


def test_validate_can_cancel_completed_fails():
    a = _make_assignment(status=AssignmentStatus.COMPLETED)
    rules = AssignmentRules(a)
    errors = rules.validate_can_cancel()
    assert len(errors) == 1


def test_validate_can_change_doctor_planned():
    a = _make_assignment(status=AssignmentStatus.PLANNED)
    rules = AssignmentRules(a)
    assert rules.validate_can_change_doctor() == []


def test_validate_can_change_doctor_started_fails():
    a = _make_assignment(status=AssignmentStatus.STARTED)
    rules = AssignmentRules(a)
    errors = rules.validate_can_change_doctor()
    assert len(errors) == 1


def test_validate_can_change_time_planned():
    a = _make_assignment(status=AssignmentStatus.PLANNED)
    rules = AssignmentRules(a)
    assert rules.validate_can_change_time() == []


def test_validate_can_change_time_started_fails():
    a = _make_assignment(status=AssignmentStatus.STARTED)
    rules = AssignmentRules(a)
    errors = rules.validate_can_change_time()
    assert len(errors) == 1
