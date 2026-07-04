"""Extra state machine."""

from app.domain.constants.extra_status import ExtraStatus


class ExtraStateMachine:
    def __init__(self, aggregate) -> None:
        self._aggregate = aggregate

    def approve(self) -> None:
        self._transition(ExtraStatus.PENDING, ExtraStatus.APPROVED)

    def reject(self) -> None:
        self._transition(ExtraStatus.PENDING, ExtraStatus.REJECTED)

    def cancel(self) -> None:
        current = self._aggregate.status
        allowed = {ExtraStatus.PENDING, ExtraStatus.APPROVED}
        if current not in allowed:
            raise ValueError(f"Cannot cancel extra in status '{current}'")
        self._transition(current, ExtraStatus.CANCELLED)

    def _transition(self, from_status: str, to_status: str) -> None:
        current = self._aggregate.status
        if current != from_status:
            raise ValueError(
                f"Cannot transition from '{current}' to '{to_status}': "
                f"expected '{from_status}'"
            )
        self._aggregate.status = to_status
