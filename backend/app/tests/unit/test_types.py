from app.common.types import (
    UUIDStr,
    RequestID,
    CorrelationID,
    AuditID,
    EventID,
    JSON,
    Headers,
    QueryParams,
)


def test_type_aliases_exist():
    assert UUIDStr is str
    assert RequestID is str
    assert CorrelationID is str
    assert AuditID is str
    assert EventID is str


def test_json_type():
    data: JSON = {"key": "value"}
    assert isinstance(data, dict)


def test_headers_type():
    headers: Headers = {"Content-Type": "application/json"}
    assert isinstance(headers, dict)


def test_query_params_type():
    params: QueryParams = {"page": 1, "size": 20}
    assert isinstance(params, dict)
