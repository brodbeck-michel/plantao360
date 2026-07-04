from datetime import date, datetime

from app.domain.constants.shift_status import ShiftStatus
from app.domain.value_objects.shift_time_range import ShiftTimeRange


class ShiftRules:
    def __init__(self, shift) -> None:
        self._shift = shift

    def validate_date_within_period(self, period_start: date, period_end: date) -> list[str]:
        errors: list[str] = []
        if self._shift.shift_date < period_start:
            errors.append("Shift date is before period start")
        if self._shift.shift_date > period_end:
            errors.append("Shift date is after period end")
        return errors

    def validate_can_update(self) -> list[str]:
        errors: list[str] = []
        if self._shift.status == ShiftStatus.COMPLETED:
            errors.append("Cannot update a completed shift")
        if self._shift.status == ShiftStatus.CANCELLED:
            errors.append("Cannot update a cancelled shift")
        return errors

    def validate_can_start(self) -> list[str]:
        errors: list[str] = []
        if self._shift.status != ShiftStatus.SCHEDULED:
            errors.append(f"Cannot start shift in status '{self._shift.status}'")
        return errors

    def validate_can_complete(self) -> list[str]:
        errors: list[str] = []
        if self._shift.status != ShiftStatus.IN_PROGRESS:
            errors.append(f"Cannot complete shift in status '{self._shift.status}'")
        return errors

    def validate_can_cancel(self) -> list[str]:
        errors: list[str] = []
        if self._shift.status not in (ShiftStatus.DRAFT, ShiftStatus.SCHEDULED, ShiftStatus.IN_PROGRESS):
            errors.append(f"Cannot cancel shift in status '{self._shift.status}'")
        return errors

    def validate_time_range(self) -> list[str]:
        errors: list[str] = []
        if self._shift.scheduled_start and self._shift.scheduled_end:
            if self._shift.scheduled_end <= self._shift.scheduled_start:
                errors.append("scheduled_end must be after scheduled_start")
        return errors
