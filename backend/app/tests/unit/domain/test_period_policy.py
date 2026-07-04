import pytest
from app.domain.policies.period_policy import PeriodPolicy
from app.domain.constants.period_status import PeriodStatus


class TestPeriodPolicy:
    def setup_method(self):
        self.policy = PeriodPolicy()

    def test_can_close_draft(self):
        assert self.policy.can_close(PeriodStatus.DRAFT)

    def test_can_close_closed(self):
        assert not self.policy.can_close(PeriodStatus.CLOSED)

    def test_can_close_paid(self):
        assert not self.policy.can_close(PeriodStatus.PAID)

    def test_can_reopen_closed(self):
        assert self.policy.can_reopen(PeriodStatus.CLOSED)

    def test_can_reopen_draft(self):
        assert not self.policy.can_reopen(PeriodStatus.DRAFT)

    def test_can_reopen_paid(self):
        assert not self.policy.can_reopen(PeriodStatus.PAID)

    def test_can_edit_draft(self):
        assert self.policy.can_edit(PeriodStatus.DRAFT)

    def test_can_edit_closed(self):
        assert not self.policy.can_edit(PeriodStatus.CLOSED)

    def test_can_edit_paid(self):
        assert not self.policy.can_edit(PeriodStatus.PAID)

    def test_can_pay_closed(self):
        assert self.policy.can_pay(PeriodStatus.CLOSED)

    def test_can_pay_draft(self):
        assert not self.policy.can_pay(PeriodStatus.DRAFT)

    def test_can_pay_paid(self):
        assert not self.policy.can_pay(PeriodStatus.PAID)

    def test_allowed_transitions_draft(self):
        assert self.policy.allowed_transitions(PeriodStatus.DRAFT) == {PeriodStatus.CLOSED}

    def test_allowed_transitions_closed(self):
        assert self.policy.allowed_transitions(PeriodStatus.CLOSED) == {
            PeriodStatus.DRAFT, PeriodStatus.PAID
        }

    def test_allowed_transitions_paid(self):
        assert self.policy.allowed_transitions(PeriodStatus.PAID) == set()
