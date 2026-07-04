from app.common.result import Success, Failure
from app.use_cases.assignments.base_assignment_use_case import BaseAssignmentUseCase
from app.models.shift_part import ShiftPart
from app.domain.constants.assignment_status import AssignmentStatus
from app.domain.events.event_names import DomainEventName
from app.domain.errors.assignment_errors import AssignmentErrorCode
from app.core.logging import get_logger

logger = get_logger("use_case.assignment.create")


class AssignDoctor(BaseAssignmentUseCase):
    def validate(self, **kwargs) -> Failure | None:
        shift_id = kwargs.get("shift_id")
        doctor_id = kwargs.get("doctor_id")
        start_time = kwargs.get("start_time")
        end_time = kwargs.get("end_time")

        if not shift_id or not doctor_id:
            return Failure(error="shift_id and doctor_id required", code="VALIDATION_ERROR")
        if not start_time or not end_time:
            return Failure(error="start_time and end_time required", code="VALIDATION_ERROR")

        if self.shift_repo:
            shift = self.shift_repo.get_by_id(shift_id)
            if not shift:
                return Failure(
                    error=f"Shift {shift_id} not found",
                    code=AssignmentErrorCode.ASSIGNMENT_SHIFT_NOT_FOUND,
                )

        if self.doctor_repo:
            doctor = self.doctor_repo.get_by_id(doctor_id)
            if not doctor:
                return Failure(
                    error=f"Doctor {doctor_id} not found",
                    code=AssignmentErrorCode.ASSIGNMENT_DOCTOR_NOT_FOUND,
                )

        return None

    def execute(self, **kwargs) -> Success:
        from datetime import time as time_type

        shift_id = kwargs["shift_id"]
        doctor_id = kwargs["doctor_id"]
        start_time = kwargs["start_time"]
        end_time = kwargs["end_time"]

        if isinstance(start_time, str):
            parts = start_time.split(":")
            start_time = time_type(int(parts[0]), int(parts[1]))
        if isinstance(end_time, str):
            parts = end_time.split(":")
            end_time = time_type(int(parts[0]), int(parts[1]))

        assignment = ShiftPart(
            shift_id=shift_id,
            doctor_id=doctor_id,
            start_time=start_time,
            end_time=end_time,
            status=AssignmentStatus.PLANNED,
        )
        created = self.repo.create(assignment)

        self._queue_event(
            DomainEventName.ASSIGNMENT_CREATED_V1,
            {"id": created.id, "shift_id": shift_id, "doctor_id": doctor_id},
        )

        logger.info("assignment.created.v1", extra={"assignment_id": created.id})
        return Success(data={"id": created.id, "status": created.status})
