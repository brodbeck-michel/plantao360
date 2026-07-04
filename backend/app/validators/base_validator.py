from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    def add_error(self, error: str) -> None:
        self.errors.append(error)


class BaseValidator:
    def validate(self, data: any) -> ValidationResult:
        result = ValidationResult()
        self._validate(data, result)
        return result

    def _validate(self, data: any, result: ValidationResult) -> None:
        pass
