from app.common.result import Success, Failure


def test_success():
    result = Success(data="test")
    assert result.is_success is True
    assert result.is_failure is False
    assert result.data == "test"


def test_failure():
    result = Failure(error="error occurred", code="ERR_001")
    assert result.is_success is False
    assert result.is_failure is True
    assert result.error == "error occurred"
    assert result.code == "ERR_001"
