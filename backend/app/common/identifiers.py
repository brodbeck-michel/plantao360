from uuid import UUID, uuid4


def generate_uuid() -> UUID:
    return uuid4()


def generate_uuid_str() -> str:
    return str(uuid4())


def parse_uuid(value: str) -> UUID:
    return UUID(value)


def is_valid_uuid(value: str) -> bool:
    try:
        UUID(value)
        return True
    except ValueError:
        return False
