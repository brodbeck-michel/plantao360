from app.common.result import Success, Failure
from app.use_cases.assignments.base_assignment_use_case import BaseAssignmentUseCase
from app.domain.state_machines.assignment_state_machine import AssignmentStateMachine
from app.domain.rules.assignment_rules import AssignmentRules
from app.domain.events.event_names import DomainEventName
from app.domain.errors.assignment_errors import AssignmentErrorCode
from app.core.logging import get_logger

logger = get_logger("use_case.assignment.complete")


class CompleteAssignment(BaseAssignmentUseCase):
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
        errors = rules.validate_can_complete()
        if errors:
            return Failure(error=errors[0], code=AssignmentErrorCode.ASSIGNMENT_INVALID_TRANSITION)

        return None

    def execute(self, **kwargs) -> Success:
        assignment_id = kwargs["assignment_id"]
        entity = self.repo.get_by_id(assignment_id)

        sm = AssignmentStateMachine(entity)
        sm.complete()

        if entity.start_time and entity.end_time:
            from datetime import datetime, timedelta
            start_dt = datetime(2000, 1, 1, entity.start_time.hour, entity.start_time.minute)
            end_dt = datetime(2000, 1, 1, entity.end_time.hour, entity.end_time.minute)
            entity.duration_minutes = int((end_dt - start_dt).total_seconds() / 60)

        updated = self.repo.update(entity)

        self._queue_event(
            DomainEventName.ASSIGNMENT_COMPLETED_V1,
            {"id": updated.id, "duration_minutes": updated.duration_minutes},
        )

        logger.info("assignment.completed.v1", extra={"assignment_id": updated.id})
        return Success(data={"id": updated.id, "status": updated.status, "duration_minutes": updated.duration_minutes})
