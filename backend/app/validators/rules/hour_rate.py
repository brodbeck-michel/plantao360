def validate_hour_rate(value: float | None) -> list[str]:
    errors = []
    if value is None:
        pass
    elif value <= 0:
        errors.append("Valor hora deve ser maior que zero")
    return errors
