from app.audit.events import AuditAction


def test_audit_action_values():
    values = AuditAction.values()
    assert "CREATE" in values
    assert "READ" in values
    assert "UPDATE" in values
    assert "DELETE" in values
    assert "LOGIN" in values
    assert "LOGOUT" in values
    assert "EXPORT" in values
    assert "IMPORT" in values


def test_audit_action_count():
    assert len(AuditAction.values()) == 8


def test_audit_action_is_str_enum():
    assert issubclass(AuditAction, str)
