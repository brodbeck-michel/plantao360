from enum import StrEnum


class DomainEventName(StrEnum):
    DOCTOR_CREATED_V1 = "doctor.created.v1"
    DOCTOR_UPDATED_V1 = "doctor.updated.v1"
    DOCTOR_DEACTIVATED_V1 = "doctor.deactivated.v1"

    PERIOD_CREATED_V1 = "period.created.v1"
    PERIOD_UPDATED_V1 = "period.updated.v1"
    PERIOD_CLOSED_V1 = "period.closed.v1"
    PERIOD_REOPENED_V1 = "period.reopened.v1"

    SHIFT_CREATED_V1 = "shift.created.v1"
    SHIFT_UPDATED_V1 = "shift.updated.v1"
    SHIFT_STARTED_V1 = "shift.started.v1"
    SHIFT_COMPLETED_V1 = "shift.completed.v1"
    SHIFT_CANCELLED_V1 = "shift.cancelled.v1"
    SHIFT_DELETED_V1 = "shift.deleted.v1"
    SHIFT_STARTED_AUTOMATICALLY_V1 = "shift.started.automatically.v1"
    SHIFT_COMPLETED_AUTOMATICALLY_V1 = "shift.completed.automatically.v1"

    EXTRA_CREATED_V1 = "extra.created.v1"
    EXTRA_DELETED_V1 = "extra.deleted.v1"

    ASSIGNMENT_CREATED_V1 = "assignment.created.v1"
    ASSIGNMENT_UPDATED_V1 = "assignment.updated.v1"
    ASSIGNMENT_CONFIRMED_V1 = "assignment.confirmed.v1"
    ASSIGNMENT_STARTED_V1 = "assignment.started.v1"
    ASSIGNMENT_COMPLETED_V1 = "assignment.completed.v1"
    ASSIGNMENT_CANCELLED_V1 = "assignment.cancelled.v1"
    ASSIGNMENT_REMOVED_V1 = "assignment.removed.v1"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]
