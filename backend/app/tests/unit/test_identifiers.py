from uuid import UUID

from app.common.identifiers import (
    generate_uuid,
    generate_uuid_str,
    parse_uuid,
    is_valid_uuid,
)


def test_generate_uuid_returns_uuid():
    result = generate_uuid()
    assert isinstance(result, UUID)


def test_generate_uuid_returns_unique():
    uuid1 = generate_uuid()
    uuid2 = generate_uuid()
    assert uuid1 != uuid2


def test_generate_uuid_str_returns_string():
    result = generate_uuid_str()
    assert isinstance(result, str)


def test_generate_uuid_str_is_valid_uuid():
    result = generate_uuid_str()
    assert is_valid_uuid(result)


def test_generate_uuid_str_returns_unique():
    str1 = generate_uuid_str()
    str2 = generate_uuid_str()
    assert str1 != str2


def test_parse_uuid_valid():
    value = "12345678-1234-5678-1234-567812345678"
    result = parse_uuid(value)
    assert isinstance(result, UUID)
    assert str(result) == value


def test_parse_uuid_invalid():
    import pytest

    with pytest.raises(ValueError):
        parse_uuid("not-a-uuid")


def test_is_valid_uuid_true():
    value = "12345678-1234-5678-1234-567812345678"
    assert is_valid_uuid(value) is True


def test_is_valid_uuid_false():
    assert is_valid_uuid("not-a-uuid") is False
    assert is_valid_uuid("") is False
    assert is_valid_uuid("123") is False


def test_is_valid_uuid_empty_string():
    assert is_valid_uuid("") is False
