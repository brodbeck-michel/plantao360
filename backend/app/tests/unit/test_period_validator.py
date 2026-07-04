from app.validators.period_validator import PeriodValidator
from app.schemas.period.period_create import PeriodCreateDTO
from app.schemas.period.period_update import PeriodUpdateDTO


def test_validator_valid_create():
    validator = PeriodValidator()
    dto = PeriodCreateDTO(year=2026, month=6)
    result = validator.validate(dto)
    assert result.is_valid


def test_validator_valid_update():
    validator = PeriodValidator()
    dto = PeriodUpdateDTO(month=7)
    result = validator.validate(dto)
    assert result.is_valid


def test_validator_update_all_fields():
    validator = PeriodValidator()
    dto = PeriodUpdateDTO(year=2027, month=12)
    result = validator.validate(dto)
    assert result.is_valid
