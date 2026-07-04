from app.common.result import Success, Failure
from app.use_cases.assignments.base_assignment_use_case import BaseAssignmentUseCase
from app.domain.state_machines.assignment_state_machine import AssignmentStateMachine
from app.domain.rules.assignment_rules import AssignmentRules
from app.domain.events.event_names import DomainEventName
from app.domain.errors.assignment_errors import AssignmentErrorCode
from app.core.logging import get_logger

logger = get_logger("use_case.assignment.cancel")


class CancelAssignment(BaseAssignmentUseCase):
    def validate(self, **kwargs) -> Failure | None:
        assignment_id = kwargs.get("assignment_id")
        if not assignment_id:
            return Failure(error="assignment_id required", code="VALIDATION_ERROR")

        entity = self.repo.get_by_id(assignment_id)
        if not entity:
            return Failure(
                error=f"Assignment {assignment_id} not found",
                code=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
            )

        rules = AssignmentRules(entity)
        errors = rules.validate_can_cancel()
        if errors:
            return Failure(error=errors[0], code=AssignmentErrorCode.ASSIGNMENT_CANNOT_BE_CANCELLED)

        return None

    def execute(self, **kwargs) -> Success:
        assignment_id = kwargs["assignment_id"]
        entity = self.repo.get_by_id(assignment_id)

        sm = AssignmentStateMachine(entity)
        sm.cancel()

        updated = self.repo.update(entity)

        self._queue_event(
            DomainEventName.ASSIGNMENT_CANCELLED_V1,
            {"id": updated.id},
        )

        logger.info("assignment.cancelled.v1", extra={"assignment_id": updated.id})
        return Success(data={"id": updated.id, "status": updated.status})
