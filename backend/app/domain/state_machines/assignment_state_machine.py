from app.domain.constants.assignment_status import AssignmentStatus
from app.domain.base.aggregate_root import AggregateRoot


class AssignmentStateMachine:
    def __init__(self, aggregate: AggregateRoot) -> None:
        self._aggregate = aggregate

    def confirm(self) -> None:
        self._transition(AssignmentStatus.PLANNED, AssignmentStatus.CONFIRMED)

    def start(self) -> None:
        self._transition(AssignmentStatus.CONFIRMED, AssignmentStatus.STARTED)

    def complete(self) -> None:
        self._transition(AssignmentStatus.STARTED, AssignmentStatus.COMPLETED)

    def cancel(self) -> None:
        current = self._aggregate.status
        allowed = {AssignmentStatus.PLANNED, AssignmentStatus.CONFIRMED}
        if current not in allowed:
            raise ValueError(f"Cannot cancel assignment in status '{current}'")
        self._transition(current, AssignmentStatus.CANCELLED)

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
