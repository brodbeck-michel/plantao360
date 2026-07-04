from app.common.result import Success, Failure
from app.use_cases.assignments.base_assignment_use_case import BaseAssignmentUseCase
from app.domain.constants.assignment_status import AssignmentStatus
from app.domain.rules.assignment_rules import AssignmentRules
from app.domain.events.event_names import DomainEventName
from app.domain.errors.assignment_errors import AssignmentErrorCode
from app.core.logging import get_logger

logger = get_logger("use_case.assignment.update")


class UpdateAssignment(BaseAssignmentUseCase):
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
        errors = rules.validate_can_change_time()
        if errors:
            return Failure(error=errors[0], code=AssignmentErrorCode.ASSIGNMENT_IMMUTABLE)

        return None

    def execute(self, **kwargs) -> Success:
        from datetime import time as time_type

        assignment_id = kwargs["assignment_id"]
        entity = self.repo.get_by_id(assignment_id)

        start_time = kwargs.get("start_time")
        end_time = kwargs.get("end_time")

        if start_time:
            if isinstance(start_time, str):
                parts = start_time.split(":")
                start_time = time_type(int(parts[0]), int(parts[1]))
            entity.start_time = start_time

        if end_time:
            if isinstance(end_time, str):
                parts = end_time.split(":")
                end_time = time_type(int(parts[0]), int(parts[1]))
            entity.end_time = end_time

        updated = self.repo.update(entity)

        self._queue_event(
            DomainEventName.ASSIGNMENT_UPDATED_V1,
            {"id": updated.id},
        )

        logger.info("assignment.updated.v1", extra={"assignment_id": updated.id})
        return Success(data={"id": updated.id, "status": updated.status})
