from app.common.api_response import ApiResponse


def test_api_response_ok():
    resp = ApiResponse.ok(data={"id": 1})
    assert resp.success is True
    assert resp.data == {"id": 1}
    assert resp.errors == []


def test_api_response_fail():
    resp = ApiResponse.fail(errors=["error 1", "error 2"])
    assert resp.success is False
    assert len(resp.errors) == 2


def test_api_response_to_dict():
    resp = ApiResponse.ok(data="test", meta={"count": 1})
    d = resp.to_dict()
    assert d["success"] is True
    assert d["data"] == "test"
    assert d["meta"]["count"] == 1
    assert d["errors"] == []
