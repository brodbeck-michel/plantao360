from app.validators.base_validator import BaseValidator, ValidationResult
from app.validators.rules import validate_crm, validate_hour_rate, validate_doctor_name
from app.schemas.doctor.doctor_create import DoctorCreateDTO
from app.schemas.doctor.doctor_update import DoctorUpdateDTO


class DoctorValidator(BaseValidator):
    def _validate(self, data: DoctorCreateDTO | DoctorUpdateDTO, result: ValidationResult) -> None:
        if isinstance(data, DoctorCreateDTO):
            self._validate_create(data, result)
        elif isinstance(data, DoctorUpdateDTO):
            self._validate_update(data, result)

    def _validate_create(self, data: DoctorCreateDTO, result: ValidationResult) -> None:
        for error in validate_doctor_name(data.name):
            result.add_error(error)
        for error in validate_crm(data.crm):
            result.add_error(error)
        for error in validate_hour_rate(data.hour_rate):
            result.add_error(error)

    def _validate_update(self, data: DoctorUpdateDTO, result: ValidationResult) -> None:
        if data.name is not None:
            for error in validate_doctor_name(data.name, required=False):
                result.add_error(error)
        if data.crm is not None:
            for error in validate_crm(data.crm):
                result.add_error(error)
        if data.hour_rate is not None:
            for error in validate_hour_rate(data.hour_rate):
                result.add_error(error)
