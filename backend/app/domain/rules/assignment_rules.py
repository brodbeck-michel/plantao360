from app.domain.constants.assignment_status import AssignmentStatus


class AssignmentRules:
    def __init__(self, assignment) -> None:
        self._assignment = assignment

    def validate_can_confirm(self) -> list[str]:
        errors: list[str] = []
        if self._assignment.status != AssignmentStatus.PLANNED:
            errors.append(f"Cannot confirm assignment in status '{self._assignment.status}'")
        return errors

    def validate_can_start(self) -> list[str]:
        errors: list[str] = []
        if self._assignment.status != AssignmentStatus.CONFIRMED:
            errors.append(f"Cannot start assignment in status '{self._assignment.status}'")
        return errors

    def validate_can_complete(self) -> list[str]:
        errors: list[str] = []
        if self._assignment.status != AssignmentStatus.STARTED:
            errors.append(f"Cannot complete assignment in status '{self._assignment.status}'")
        return errors

    def validate_can_cancel(self) -> list[str]:
        errors: list[str] = []
        if self._assignment.status not in (AssignmentStatus.PLANNED, AssignmentStatus.CONFIRMED):
            errors.append(f"Cannot cancel assignment in status '{self._assignment.status}'")
        return errors

    def validate_can_change_doctor(self) -> list[str]:
        errors: list[str] = []
        if self._assignment.status not in (AssignmentStatus.PLANNED, AssignmentStatus.CONFIRMED):
            errors.append(f"Cannot change doctor in status '{self._assignment.status}'")
        return errors

    def validate_can_change_time(self) -> list[str]:
        errors: list[str] = []
        if self._assignment.status not in (AssignmentStatus.PLANNED, AssignmentStatus.CONFIRMED):
            errors.append(f"Cannot change time in status '{self._assignment.status}'")
        return errors

    def validate_time_range(self) -> list[str]:
        errors: list[str] = []
        if self._assignment.start_time and self._assignment.end_time:
            if self._assignment.end_time <= self._assignment.start_time:
                errors.append("end_time must be after start_time")
        return errors
