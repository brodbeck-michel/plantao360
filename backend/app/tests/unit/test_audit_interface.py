from app.audit.context import AuditContext


def test_audit_context_exists():
    ctx = AuditContext(user="test_user")
    assert ctx.user == "test_user"
    assert ctx.request_id is None
    assert ctx.correlation_id is None


def test_audit_context_optional_fields():
    ctx = AuditContext(user="test_user", ip="127.0.0.1")
    assert ctx.user == "test_user"
    assert ctx.ip == "127.0.0.1"
    assert ctx.user_agent is None
