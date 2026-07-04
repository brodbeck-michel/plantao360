from app.common.result import Success, Failure
from app.use_cases.assignments.base_assignment_use_case import BaseAssignmentUseCase
from app.domain.errors.assignment_errors import AssignmentErrorCode
from app.core.logging import get_logger

logger = get_logger("use_case.assignment.get")


class GetAssignment(BaseAssignmentUseCase):
    def validate(self, **kwargs) -> Failure | None:
        assignment_id = kwargs.get("assignment_id")
        if not assignment_id:
            return Failure(error="assignment_id required", code="VALIDATION_ERROR")
        return None

    def execute(self, **kwargs) -> Success:
        assignment_id = kwargs["assignment_id"]
        entity = self.repo.get_by_id(assignment_id)
        if not entity:
            return Failure(
                error=f"Assignment {assignment_id} not found",
                code=AssignmentErrorCode.ASSIGNMENT_NOT_FOUND,
            )

        return Success(data={
            "id": entity.id,
            "shift_id": entity.shift_id,
            "doctor_id": entity.doctor_id,
            "start_time": str(entity.start_time),
            "end_time": str(entity.end_time),
            "status": entity.status,
            "duration_minutes": entity.duration_minutes,
        })
