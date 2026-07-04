import pytest
from app.validators.shift_validator import ShiftValidator
from app.schemas.shift.shift_create import ShiftCreateDTO
from datetime import date


def test_validate_create_valid():
    validator = ShiftValidator()
    dto = ShiftCreateDTO(
        period_id=1,
        shift_date=date(2025, 1, 15),
        shift_type="T1",
    )
    result = validator.validate(dto)
    assert result.is_valid


def test_validate_create_invalid_type():
    validator = ShiftValidator()
    dto = ShiftCreateDTO(
        period_id=1,
        shift_date=date(2025, 1, 15),
        shift_type="INVALID",
    )
    result = validator.validate(dto)
    assert not result.is_valid
