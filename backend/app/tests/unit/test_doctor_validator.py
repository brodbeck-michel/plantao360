from app.validators.doctor_validator import DoctorValidator
from app.schemas.doctor.doctor_create import DoctorCreateDTO
from app.schemas.doctor.doctor_update import DoctorUpdateDTO


def test_validator_valid_create():
    validator = DoctorValidator()
    dto = DoctorCreateDTO(name="Dr. Valid", crm="12345", hour_rate=150.0)
    result = validator.validate(dto)
    assert result.is_valid


def test_validator_invalid_crm_format():
    validator = DoctorValidator()
    dto = DoctorCreateDTO(name="Dr. Invalid", crm="abc", hour_rate=150.0)
    result = validator.validate(dto)
    assert result.is_valid is False


def test_validator_valid_update():
    validator = DoctorValidator()
    dto = DoctorUpdateDTO(name="Dr. Updated")
    result = validator.validate(dto)
    assert result.is_valid


def test_validator_update_empty_name():
    validator = DoctorValidator()
    dto = DoctorUpdateDTO(name="  ")
    result = validator.validate(dto)
    assert result.is_valid is False


def test_validator_update_empty_crm():
    validator = DoctorValidator()
    dto = DoctorUpdateDTO(crm="  ")
    result = validator.validate(dto)
    assert result.is_valid is False


def test_validator_update_invalid_crm_format():
    validator = DoctorValidator()
    dto = DoctorUpdateDTO(crm="abc")
    result = validator.validate(dto)
    assert result.is_valid is False
