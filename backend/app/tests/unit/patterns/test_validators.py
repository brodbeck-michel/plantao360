from app.validators.base_validator import BaseValidator, ValidationResult


def test_validation_result_valid():
    result = ValidationResult()
    assert result.is_valid is True
    assert result.errors == []


def test_validation_result_invalid():
    result = ValidationResult()
    result.add_error("field is required")
    assert result.is_valid is False
    assert len(result.errors) == 1


def test_validator_passes():
    class MyValidator(BaseValidator):
        pass

    validator = MyValidator()
    result = validator.validate(None)
    assert result.is_valid is True
