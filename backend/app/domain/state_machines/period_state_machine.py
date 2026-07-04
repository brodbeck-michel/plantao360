from app.domain.constants.period_status import PeriodStatus
from app.domain.errors.period_errors import PeriodErrorCode


class PeriodStateMachine:
    _TRANSITIONS: dict[PeriodStatus, set[PeriodStatus]] = {
        PeriodStatus.DRAFT: {PeriodStatus.CLOSED},
        PeriodStatus.CLOSED: {PeriodStatus.DRAFT, PeriodStatus.PAID},
        PeriodStatus.PAID: set(),
    }

    def can_transition(self, current: PeriodStatus, target: PeriodStatus) -> bool:
        return target in self._TRANSITIONS.get(current, set())

    def get_allowed_transitions(self, current: PeriodStatus) -> set[PeriodStatus]:
        return self._TRANSITIONS.get(current, set()).copy()

    def validate_transition(self, current: PeriodStatus, target: PeriodStatus) -> str | None:
        if self.can_transition(current, target):
            return None
        if current == PeriodStatus.CLOSED and target == PeriodStatus.CLOSED:
            return PeriodErrorCode.PERIOD_ALREADY_CLOSED
        if current == PeriodStatus.PAID:
            if target == PeriodStatus.CLOSED:
                return PeriodErrorCode.PERIOD_IMMUTABLE
            if target == PeriodStatus.DRAFT:
                return PeriodErrorCode.PERIOD_CANNOT_BE_REOPENED
        if current == PeriodStatus.DRAFT and target == PeriodStatus.PAID:
            return PeriodErrorCode.PERIOD_INVALID_STATUS_TRANSITION
        return PeriodErrorCode.PERIOD_INVALID_STATUS_TRANSITION
