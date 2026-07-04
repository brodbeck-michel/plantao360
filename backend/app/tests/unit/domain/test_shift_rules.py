import pytest
from unittest.mock import MagicMock
from app.domain.rules.shift_rules import ShiftRules
from app.domain.constants.shift_status import ShiftStatus


def _make_shift(**kwargs):
    shift = MagicMock()
    shift.status = kwargs.get("status", ShiftStatus.SCHEDULED)
    shift.shift_date = kwargs.get("shift_date")
    shift.scheduled_start = kwargs.get("scheduled_start")
    shift.scheduled_end = kwargs.get("scheduled_end")
    return shift


def test_validate_can_update_scheduled():
    shift = _make_shift(status=ShiftStatus.SCHEDULED)
    rules = ShiftRules(shift)
    assert rules.validate_can_update() == []


def test_validate_can_update_in_progress():
    shift = _make_shift(status=ShiftStatus.IN_PROGRESS)
    rules = ShiftRules(shift)
    assert rules.validate_can_update() == []


def test_validate_can_update_completed_fails():
    shift = _make_shift(status=ShiftStatus.COMPLETED)
    rules = ShiftRules(shift)
    errors = rules.validate_can_update()
    assert len(errors) == 1
    assert "completed" in errors[0].lower()


def test_validate_can_update_cancelled_fails():
    shift = _make_shift(status=ShiftStatus.CANCELLED)
    rules = ShiftRules(shift)
    errors = rules.validate_can_update()
    assert len(errors) == 1
    assert "cancelled" in errors[0].lower()


def test_validate_can_start_scheduled():
    shift = _make_shift(status=ShiftStatus.SCHEDULED)
    rules = ShiftRules(shift)
    assert rules.validate_can_start() == []


def test_validate_can_start_wrong_status_fails():
    shift = _make_shift(status=ShiftStatus.IN_PROGRESS)
    rules = ShiftRules(shift)
    errors = rules.validate_can_start()
    assert len(errors) == 1


def test_validate_can_complete_in_progress():
    shift = _make_shift(status=ShiftStatus.IN_PROGRESS)
    rules = ShiftRules(shift)
    assert rules.validate_can_complete() == []


def test_validate_can_complete_wrong_status_fails():
    shift = _make_shift(status=ShiftStatus.SCHEDULED)
    rules = ShiftRules(shift)
    errors = rules.validate_can_complete()
    assert len(errors) == 1


def test_validate_can_cancel_scheduled():
    shift = _make_shift(status=ShiftStatus.SCHEDULED)
    rules = ShiftRules(shift)
    assert rules.validate_can_cancel() == []


def test_validate_can_cancel_in_progress():
    shift = _make_shift(status=ShiftStatus.IN_PROGRESS)
    rules = ShiftRules(shift)
    assert rules.validate_can_cancel() == []


def test_validate_can_cancel_completed_fails():
    shift = _make_shift(status=ShiftStatus.COMPLETED)
    rules = ShiftRules(shift)
    errors = rules.validate_can_cancel()
    assert len(errors) == 1


def test_validate_can_cancel_cancelled_fails():
    shift = _make_shift(status=ShiftStatus.CANCELLED)
    rules = ShiftRules(shift)
    errors = rules.validate_can_cancel()
    assert len(errors) == 1


def test_validate_date_within_period():
    from datetime import date
    shift = _make_shift(shift_date=date(2025, 1, 15))
    rules = ShiftRules(shift)
    errors = rules.validate_date_within_period(date(2025, 1, 1), date(2025, 1, 31))
    assert errors == []


def test_validate_date_before_period():
    from datetime import date
    shift = _make_shift(shift_date=date(2024, 12, 31))
    rules = ShiftRules(shift)
    errors = rules.validate_date_within_period(date(2025, 1, 1), date(2025, 1, 31))
    assert len(errors) == 1
    assert "before" in errors[0].lower()


def test_validate_date_after_period():
    from datetime import date
    shift = _make_shift(shift_date=date(2025, 2, 1))
    rules = ShiftRules(shift)
    errors = rules.validate_date_within_period(date(2025, 1, 1), date(2025, 1, 31))
    assert len(errors) == 1
    assert "after" in errors[0].lower()
