import re


def validate_year_month(value: str | None) -> list[str]:
    errors = []
    if not value or not value.strip():
        errors.append("Periodo é obrigatório")
    return errors
