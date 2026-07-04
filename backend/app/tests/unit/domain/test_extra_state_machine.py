"""Tests for Extra State Machine."""

import pytest
from app.domain.state_machines.extra_state_machine import ExtraStateMachine
from app.domain.constants.extra_status import ExtraStatus


class FakeExtra:
    def __init__(self, status: str):
        self.status = status


class TestExtraStateMachine:
    def test_approve_from_pending(self):
        extra = FakeExtra(ExtraStatus.PENDING)
        sm = ExtraStateMachine(extra)
        sm.approve()
        assert extra.status == ExtraStatus.APPROVED

    def test_reject_from_pending(self):
        extra = FakeExtra(ExtraStatus.PENDING)
        sm = ExtraStateMachine(extra)
        sm.reject()
        assert extra.status == ExtraStatus.REJECTED

    def test_cancel_from_pending(self):
        extra = FakeExtra(ExtraStatus.PENDING)
        sm = ExtraStateMachine(extra)
        sm.cancel()
        assert extra.status == ExtraStatus.CANCELLED

    def test_cancel_from_approved(self):
        extra = FakeExtra(ExtraStatus.APPROVED)
        sm = ExtraStateMachine(extra)
        sm.cancel()
        assert extra.status == ExtraStatus.CANCELLED

    def test_approve_from_approved_fails(self):
        extra = FakeExtra(ExtraStatus.APPROVED)
        sm = ExtraStateMachine(extra)
        with pytest.raises(ValueError, match="Cannot transition"):
            sm.approve()

    def test_reject_from_approved_fails(self):
        extra = FakeExtra(ExtraStatus.APPROVED)
        sm = ExtraStateMachine(extra)
        with pytest.raises(ValueError, match="Cannot transition"):
            sm.reject()

    def test_approve_from_rejected_fails(self):
        extra = FakeExtra(ExtraStatus.REJECTED)
        sm = ExtraStateMachine(extra)
        with pytest.raises(ValueError, match="Cannot transition"):
            sm.approve()

    def test_cancel_from_rejected_fails(self):
        extra = FakeExtra(ExtraStatus.REJECTED)
        sm = ExtraStateMachine(extra)
        with pytest.raises(ValueError, match="Cannot cancel extra"):
            sm.cancel()

    def test_approve_from_cancelled_fails(self):
        extra = FakeExtra(ExtraStatus.CANCELLED)
        sm = ExtraStateMachine(extra)
        with pytest.raises(ValueError, match="Cannot transition"):
            sm.approve()
