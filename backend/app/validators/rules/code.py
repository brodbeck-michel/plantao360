import re


def validate_code(value: str | None) -> list[str]:
    errors = []
    if not value or not value.strip():
        errors.append("Código é obrigatório")
    return errors
