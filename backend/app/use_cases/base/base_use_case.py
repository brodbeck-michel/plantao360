from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from app.common.result import Result
from app.audit.context import AuditContext
from app.events.event_dispatcher import EventDispatcher, Event

InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class BaseUseCase(ABC, Generic[InputType, OutputType]):
    """
    Base class for all use cases in Plantão 360.

    Follows the Command pattern with built-in:
    - Validation
    - Authorization
    - Audit logging
    - Event emission

    Subclasses must implement:
    - execute(): Core business logic
    - validate(): Input validation
    - authorize(): Permission checks
    """

    def __init__(self):
        self._events: list[Event] = []
        self._audit_context: AuditContext | None = None

    def __call__(self, input_data: InputType, audit: AuditContext | None = None) -> Result[OutputType]:
        """
        Main entry point. Orchestrates the use case lifecycle.
        """
        self._audit_context = audit

        # 1. Validate
        validation_result = self.validate(input_data)
        if validation_result is not None:
            return validation_result

        # 2. Authorize
        auth_result = self.authorize(input_data)
        if auth_result is not None:
            return auth_result

        # 3. Execute
        try:
            result = self.execute(input_data)
        except Exception as e:
            return self._handle_error(e)

        # 4. Emit events
        self.emit_events()

        # 5. Audit
        self.audit(input_data, result)

        return result

    @abstractmethod
    def execute(self, input_data: InputType) -> Result[OutputType]:
        """
        Core business logic. Must be implemented by subclasses.
        """
        ...

    def validate(self, input_data: InputType) -> Result[OutputType] | None:
        """
        Input validation. Override to add validation logic.
        Return None if valid, or a Failure result if invalid.
        """
        return None

    def authorize(self, input_data: InputType) -> Result[OutputType] | None:
        """
        Authorization checks. Override to add permission logic.
        Return None if authorized, or a Failure result if not.
        """
        return None

    def audit(self, input_data: InputType, result: Result[OutputType]) -> None:
        """
        Audit logging. Override to customize audit behavior.
        Called after execution, even if execution fails.
        """
        pass

    def emit_events(self) -> None:
        """
        Emit all queued events via the event dispatcher.
        """
        dispatcher = EventDispatcher()
        for event in self._events:
            dispatcher.dispatch(event)
        self._events.clear()

    def _queue_event(self, name: str, data: dict[str, Any]) -> None:
        """Queue an event for emission after successful execution."""
        self._events.append(Event(name=name, data=data))

    def _handle_error(self, error: Exception) -> Result[OutputType]:
        """Handle unexpected errors."""
        from app.common.result import Failure
        return Failure(
            error=f"Unexpected error: {str(error)}",
            code="INTERNAL_ERROR",
        )
