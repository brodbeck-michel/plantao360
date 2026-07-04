def validate_doctor_name(value: str | None, required: bool = True) -> list[str]:
    errors = []
    if not value or not value.strip():
        if required:
            errors.append("Nome é obrigatório")
        else:
            errors.append("Nome não pode ser vazio")
    elif len(value.strip()) > 255:
        errors.append("Nome não pode exceder 255 caracteres")
    return errors
