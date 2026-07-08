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

    COVERAGE_CONSOLIDATED_V1 = "coverage.consolidated.v1"
    FINANCIAL_SNAPSHOT_CREATED_V1 = "financial.snapshot.created.v1"
    FINANCIAL_FACT_GENERATED_V1 = "financial.fact.generated.v1"
    FINANCIAL_FACT_REVOKED_V1 = "financial.fact.revoked.v1"

    REMUNERATION_CALCULATED_V1 = "remuneration.calculated.v1"
    REMUNERATION_SIMULATED_V1 = "remuneration.simulated.v1"
    REMUNERATION_RECALCULATED_V1 = "remuneration.recalculated.v1"
    REMUNERATION_INVALIDATED_V1 = "remuneration.invalidated.v1"

    PAYROLL_CREATED_V1 = "payroll.created.v1"
    PAYROLL_CALCULATED_V1 = "payroll.calculated.v1"
    PAYROLL_REVIEWED_V1 = "payroll.reviewed.v1"
    PAYROLL_APPROVED_V1 = "payroll.approved.v1"
    PAYROLL_EXPORTED_V1 = "payroll.exported.v1"
    PAYROLL_PAID_V1 = "payroll.paid.v1"
    PAYROLL_ARCHIVED_V1 = "payroll.archived.v1"
    PAYROLL_REOPENED_V1 = "payroll.reopened.v1"

    PAYROLL_READY_V1 = "payroll.ready.v1"
    PAYROLL_CHECKLIST_COMPLETED_V1 = "payroll.checklist.completed.v1"
    PAYROLL_APPROVAL_REQUESTED_V1 = "payroll.approval.requested.v1"
    PAYROLL_LOCKED_V1 = "payroll.locked.v1"
    PAYROLL_UNLOCKED_V1 = "payroll.unlocked.v1"

    @classmethod
    def values(cls) -> list[str]:
        return [item.value for item in cls]
