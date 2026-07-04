from app.common.result import Success, Failure
from app.use_cases.assignments.base_assignment_use_case import BaseAssignmentUseCase
from app.domain.constants.assignment_status import AssignmentStatus
from app.domain.events.event_names import DomainEventName
from app.domain.errors.assignment_errors import AssignmentErrorCode
from app.core.logging import get_logger

logger = get_logger("use_case.assignment.remove")


class RemoveAssignment(BaseAssignmentUseCase):
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

        if entity.status == AssignmentStatus.STARTED:
            return Failure(
                error="Cannot remove a started assignment",
                code=AssignmentErrorCode.ASSIGNMENT_IMMUTABLE,
            )

        return None

    def execute(self, **kwargs) -> Success:
        assignment_id = kwargs["assignment_id"]
        entity = self.repo.get_by_id(assignment_id)

        entity.status = AssignmentStatus.CANCELLED
        self.repo.update(entity)

        self._queue_event(
            DomainEventName.ASSIGNMENT_REMOVED_V1,
            {"id": assignment_id, "shift_id": entity.shift_id, "doctor_id": entity.doctor_id},
        )

        logger.info("assignment.removed.v1", extra={"assignment_id": assignment_id})
        return Success(data={"id": assignment_id, "status": entity.status})
