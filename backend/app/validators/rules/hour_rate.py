from datetime import date


def validate_career_start_date(value: date | None) -> list[str]:
    errors = []
    if value is None:
        pass
    elif value > date.today():
        errors.append("Data de inicio de carreira nao pode ser no futuro")
    return errors
