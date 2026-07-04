import pytest
from app.domain.state_machines.period_state_machine import PeriodStateMachine
from app.domain.constants.period_status import PeriodStatus
from app.domain.errors.period_errors import PeriodErrorCode


class TestPeriodStateMachine:
    def setup_method(self):
        self.sm = PeriodStateMachine()

    def test_draft_to_closed(self):
        assert self.sm.can_transition(PeriodStatus.DRAFT, PeriodStatus.CLOSED)

    def test_closed_to_draft(self):
        assert self.sm.can_transition(PeriodStatus.CLOSED, PeriodStatus.DRAFT)

    def test_closed_to_paid(self):
        assert self.sm.can_transition(PeriodStatus.CLOSED, PeriodStatus.PAID)

    def test_draft_to_paid_not_allowed(self):
        assert not self.sm.can_transition(PeriodStatus.DRAFT, PeriodStatus.PAID)

    def test_paid_to_closed_not_allowed(self):
        assert not self.sm.can_transition(PeriodStatus.PAID, PeriodStatus.CLOSED)

    def test_paid_to_draft_not_allowed(self):
        assert not self.sm.can_transition(PeriodStatus.PAID, PeriodStatus.DRAFT)

    def test_paid_no_transitions(self):
        assert self.sm.get_allowed_transitions(PeriodStatus.PAID) == set()

    def test_draft_allowed_transitions(self):
        assert self.sm.get_allowed_transitions(PeriodStatus.DRAFT) == {PeriodStatus.CLOSED}

    def test_closed_allowed_transitions(self):
        assert self.sm.get_allowed_transitions(PeriodStatus.CLOSED) == {
            PeriodStatus.DRAFT, PeriodStatus.PAID
        }

    def test_validate_transition_valid(self):
        assert self.sm.validate_transition(PeriodStatus.DRAFT, PeriodStatus.CLOSED) is None

    def test_validate_transition_invalid(self):
        error = self.sm.validate_transition(PeriodStatus.PAID, PeriodStatus.CLOSED)
        assert error == PeriodErrorCode.PERIOD_IMMUTABLE

    def test_validate_transition_wrong_target(self):
        error = self.sm.validate_transition(PeriodStatus.DRAFT, PeriodStatus.PAID)
        assert error == PeriodErrorCode.PERIOD_INVALID_STATUS_TRANSITION
