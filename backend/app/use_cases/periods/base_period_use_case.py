from app.common.result import Result, Success, Failure
from app.audit.context import AuditContext
from app.events.event_dispatcher import EventDispatcher, Event
from app.domain.events.event_names import DomainEventName
from app.domain.constants.period_status import PeriodStatus
from app.domain.errors.period_errors import PeriodErrorCode
from app.common.clock import ClockProvider, SystemClock
from app.core.logging import get_logger

logger = get_logger("use_case.period")


# PeriodStateMachine — antes em domain/state_machines (consumidor único: este use_case).
# Inlinada no colapso da domain/ (spec 005, Grupo D). Transições e códigos de erro preservados.
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


# PeriodPolicy — antes em domain/policies (consumidor único: este use_case).
# Inlinada aqui no colapso da domain/ (spec 004, Grupo B).
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


class BasePeriodUseCase:
    def __init__(
        self,
        state_machine: PeriodStateMachine | None = None,
        policy: PeriodPolicy | None = None,
        clock: ClockProvider | None = None,
    ):
        self._events: list[Event] = []
        self._audit_context: AuditContext | None = None
        self._state_machine = state_machine or PeriodStateMachine()
        self._policy = policy or PeriodPolicy(self._state_machine)
        self._clock = clock or SystemClock()

    def __call__(self, **kwargs) -> Result:
        self._audit_context = kwargs.pop("audit", None)

        validation = self.validate(**kwargs)
        if validation is not None:
            return validation

        auth = self.authorize(**kwargs)
        if auth is not None:
            return auth

        try:
            result = self.execute(**kwargs)
        except Exception as e:
            return Failure(error=f"Unexpected error: {str(e)}", code="INTERNAL_ERROR")

        if isinstance(result, Failure):
            return result

        self.emit_events()
        self.audit(result=result)
        return result

    def validate(self, **kwargs) -> Result | None:
        return None

    def authorize(self, **kwargs) -> Result | None:
        return None

    def execute(self, **kwargs) -> Result:
        raise NotImplementedError

    def audit(self, result: Result = None) -> None:
        pass

    def emit_events(self) -> None:
        dispatcher = EventDispatcher()
        for event in self._events:
            dispatcher.dispatch(event)
        self._events.clear()

    def _queue_event(self, name: str, data: dict) -> None:
        self._events.append(Event(name=name, data=data))
