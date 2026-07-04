from app.domain.constants.shift_status import ShiftStatus
from app.domain.base.aggregate_root import AggregateRoot


class ShiftStateMachine:
    def __init__(self, aggregate: AggregateRoot) -> None:
        self._aggregate = aggregate

    def activate(self) -> None:
        self._transition(ShiftStatus.DRAFT, ShiftStatus.SCHEDULED)

    def start(self) -> None:
        self._transition(ShiftStatus.SCHEDULED, ShiftStatus.IN_PROGRESS)

    def complete(self) -> None:
        self._transition(ShiftStatus.IN_PROGRESS, ShiftStatus.COMPLETED)

    def cancel(self) -> None:
        current = self._aggregate.status
        allowed = {ShiftStatus.DRAFT, ShiftStatus.SCHEDULED, ShiftStatus.IN_PROGRESS}
        if current not in allowed:
            raise ValueError(f"Cannot cancel shift in status '{current}'")
        self._transition(current, ShiftStatus.CANCELLED)

    def _transition(self, from_status: str, to_status: str) -> None:
        current = self._aggregate.status
        if current != from_status:
            raise ValueError(
                f"Cannot transition from '{current}' to '{to_status}': "
                f"expected '{from_status}'"
            )
        self._aggregate.before_transition(current, to_status)
        self._aggregate.status = to_status
        self._aggregate.after_transition(current, to_status)
