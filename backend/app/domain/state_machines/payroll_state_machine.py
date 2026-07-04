"""Payroll State Machine — controls competency lifecycle transitions."""

from app.domain.constants.payroll_status import PayrollStatus
from app.domain.base.aggregate_root import AggregateRoot


class PayrollStateMachine:
    """Controls payroll competency lifecycle transitions.

    Lifecycle: draft → calculated → reviewed → approved → locked → exported → paid → archived
    Special: any state → draft (reopening)
    Administrative: approved ↔ locked
    """

    TRANSITIONS: dict[PayrollStatus, set[PayrollStatus]] = {
        PayrollStatus.DRAFT: {PayrollStatus.CALCULATED},
        PayrollStatus.CALCULATED: {PayrollStatus.REVIEWED, PayrollStatus.DRAFT},
        PayrollStatus.REVIEWED: {PayrollStatus.APPROVED, PayrollStatus.CALCULATED},
        PayrollStatus.APPROVED: {PayrollStatus.LOCKED, PayrollStatus.EXPORTED, PayrollStatus.DRAFT},
        PayrollStatus.LOCKED: {PayrollStatus.APPROVED, PayrollStatus.EXPORTED, PayrollStatus.DRAFT},
        PayrollStatus.EXPORTED: {PayrollStatus.PAID, PayrollStatus.DRAFT},
        PayrollStatus.PAID: {PayrollStatus.ARCHIVED, PayrollStatus.DRAFT},
        PayrollStatus.ARCHIVED: set(),
    }

    def __init__(self, aggregate: AggregateRoot) -> None:
        self._aggregate = aggregate

    def can_transition(self, from_status: PayrollStatus, to_status: PayrollStatus) -> bool:
        return to_status in self.TRANSITIONS.get(from_status, set())

    def get_allowed_transitions(self, current_status: PayrollStatus) -> set[PayrollStatus]:
        return self.TRANSITIONS.get(current_status, set())

    def calculate(self) -> None:
        self._transition(PayrollStatus.DRAFT, PayrollStatus.CALCULATED)

    def review(self) -> None:
        self._transition(PayrollStatus.CALCULATED, PayrollStatus.REVIEWED)

    def approve(self) -> None:
        self._transition(PayrollStatus.REVIEWED, PayrollStatus.APPROVED)

    def lock(self) -> None:
        self._transition(PayrollStatus.APPROVED, PayrollStatus.LOCKED)

    def unlock(self) -> None:
        self._transition(PayrollStatus.LOCKED, PayrollStatus.APPROVED)

    def export(self) -> None:
        current = self._aggregate.status
        if current == PayrollStatus.APPROVED:
            self._transition(PayrollStatus.APPROVED, PayrollStatus.EXPORTED)
        elif current == PayrollStatus.LOCKED:
            self._transition(PayrollStatus.LOCKED, PayrollStatus.EXPORTED)
        else:
            raise ValueError(
                f"Cannot transition from '{current}' to '{PayrollStatus.EXPORTED}'"
            )

    def mark_paid(self) -> None:
        self._transition(PayrollStatus.EXPORTED, PayrollStatus.PAID)

    def archive(self) -> None:
        self._transition(PayrollStatus.PAID, PayrollStatus.ARCHIVED)

    def reopen(self) -> None:
        current = self._aggregate.status
        allowed_reopen = {
            PayrollStatus.CALCULATED,
            PayrollStatus.REVIEWED,
            PayrollStatus.APPROVED,
            PayrollStatus.LOCKED,
            PayrollStatus.EXPORTED,
            PayrollStatus.PAID,
        }
        if current not in allowed_reopen:
            raise ValueError(
                f"Cannot reopen payroll in status '{current}'"
            )
        self._transition(current, PayrollStatus.DRAFT)

    def _transition(self, from_status: PayrollStatus, to_status: PayrollStatus) -> None:
        current = self._aggregate.status
        if current != from_status:
            raise ValueError(
                f"Cannot transition from '{current}' to '{to_status}': "
                f"expected '{from_status}'"
            )
        self._aggregate.before_transition(current, to_status)
        self._aggregate.status = to_status
        self._aggregate.after_transition(current, to_status)
