from datetime import date, time
from app.validators.base_validator import BaseValidator, ValidationResult
from app.schemas.shift.shift_create import ShiftCreateDTO
from app.schemas.shift.shift_update import ShiftUpdateDTO


class ShiftValidator(BaseValidator):
    def _validate(self, data: ShiftCreateDTO | ShiftUpdateDTO, result: ValidationResult) -> None:
        if isinstance(data, ShiftCreateDTO):
            self._validate_create(data, result)
        elif isinstance(data, ShiftUpdateDTO):
            self._validate_update(data, result)

    def _validate_create(self, data: ShiftCreateDTO, result: ValidationResult) -> None:
        if not data.shift_date:
            result.add_error("shift_date is required")
        if not data.shift_type:
            result.add_error("shift_type is required")
        if data.shift_type and data.shift_type not in ("T1", "T2", "T3", "R1", "R2"):
            result.add_error(f"Invalid shift_type: {data.shift_type}")
        if data.scheduled_start and data.scheduled_end:
            if data.scheduled_end <= data.scheduled_start:
                result.add_error("scheduled_end must be after scheduled_start")

    def _validate_update(self, data: ShiftUpdateDTO, result: ValidationResult) -> None:
        if data.shift_type is not None:
            if data.shift_type not in ("T1", "T2", "T3", "R1", "R2"):
                result.add_error(f"Invalid shift_type: {data.shift_type}")
        if data.scheduled_start is not None and data.scheduled_end is not None:
            if data.scheduled_end <= data.scheduled_start:
                result.add_error("scheduled_end must be after scheduled_start")
