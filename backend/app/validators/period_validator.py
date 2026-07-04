from app.validators.base_validator import BaseValidator, ValidationResult
from app.schemas.period.period_create import PeriodCreateDTO
from app.schemas.period.period_update import PeriodUpdateDTO


class PeriodValidator(BaseValidator):
    def _validate(self, data: PeriodCreateDTO | PeriodUpdateDTO, result: ValidationResult) -> None:
        if isinstance(data, PeriodCreateDTO):
            self._validate_create(data, result)
        elif isinstance(data, PeriodUpdateDTO):
            self._validate_update(data, result)

    def _validate_create(self, data: PeriodCreateDTO, result: ValidationResult) -> None:
        if data.month < 1 or data.month > 12:
            result.add_error("Mes deve ser entre 1 e 12")
        if data.year < 2000 or data.year > 2100:
            result.add_error("Ano deve ser entre 2000 e 2100")

    def _validate_update(self, data: PeriodUpdateDTO, result: ValidationResult) -> None:
        if data.month is not None and (data.month < 1 or data.month > 12):
            result.add_error("Mes deve ser entre 1 e 12")
        if data.year is not None and (data.year < 2000 or data.year > 2100):
            result.add_error("Ano deve ser entre 2000 e 2100")
