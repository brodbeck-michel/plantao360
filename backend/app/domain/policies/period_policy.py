from app.domain.constants.period_status import PeriodStatus
from app.domain.state_machines.period_state_machine import PeriodStateMachine


class PeriodPolicy:
    def __init__(self, state_machine: PeriodStateMachine | None = None):
        self._state_machine = state_machine or PeriodStateMachine()

    def can_close(self, current_status: PeriodStatus) -> bool:
        return self._state_machine.can_transition(current_status, PeriodStatus.CLOSED)

    def can_reopen(self, current_status: PeriodStatus) -> bool:
        return self._state_machine.can_transition(current_status, PeriodStatus.DRAFT)

    def can_edit(self, current_status: PeriodStatus) -> bool:
        return current_status == PeriodStatus.DRAFT

    def can_pay(self, current_status: PeriodStatus) -> bool:
        return self._state_machine.can_transition(current_status, PeriodStatus.PAID)

    def allowed_transitions(self, current_status: PeriodStatus) -> set[PeriodStatus]:
        return self._state_machine.get_allowed_transitions(current_status)
