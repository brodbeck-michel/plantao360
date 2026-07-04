from app.common.context import (
    set_request_id,
    get_request_id,
    set_correlation_id,
    get_correlation_id,
)


def test_set_and_get_request_id():
    set_request_id("req-123")
    assert get_request_id() == "req-123"


def test_set_and_get_correlation_id():
    set_correlation_id("corr-456")
    assert get_correlation_id() == "corr-456"


def test_request_id_default_none():
    from app.common.context import request_id_context

    token = request_id_context.set(None)
    assert get_request_id() is None
    request_id_context.reset(token)


def test_correlation_id_default_none():
    from app.common.context import correlation_id_context

    token = correlation_id_context.set(None)
    assert get_correlation_id() is None
    correlation_id_context.reset(token)


def test_context_isolation():
    set_request_id("req-1")
    set_correlation_id("corr-1")
    assert get_request_id() == "req-1"
    assert get_correlation_id() == "corr-1"
