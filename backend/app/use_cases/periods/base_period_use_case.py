from app.common.result import Result, Success, Failure
from app.audit.context import AuditContext
from app.events.event_dispatcher import EventDispatcher, Event
from app.domain.events.event_names import DomainEventName
from app.domain.state_machines.period_state_machine import PeriodStateMachine
from app.domain.policies.period_policy import PeriodPolicy
from app.common.clock import ClockProvider, SystemClock
from app.core.logging import get_logger

logger = get_logger("use_case.period")


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
