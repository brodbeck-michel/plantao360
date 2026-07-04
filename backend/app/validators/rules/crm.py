import re


def validate_crm(value: str | None) -> list[str]:
    errors = []
    if not value or not value.strip():
        errors.append("CRM é obrigatório")
    elif not re.match(r"^\d{4,10}$", value.replace(".", "").replace("/", "")):
        errors.append("CRM inválido (formato: apenas dígitos, 4-10 caracteres)")
    return errors
