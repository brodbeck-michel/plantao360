from app.audit.models import AuditLog
from app.common.identifiers import is_valid_uuid


def test_audit_log_has_audit_id():
    log = AuditLog(action="CREATE", resource="User")
    assert log.audit_id is not None
    assert is_valid_uuid(log.audit_id)


def test_audit_log_has_timestamp():
    log = AuditLog(action="CREATE", resource="User")
    assert log.timestamp is not None


def test_audit_log_action():
    log = AuditLog(action="UPDATE", resource="Doctor")
    assert log.action == "UPDATE"


def test_audit_log_resource():
    log = AuditLog(action="DELETE", resource="Schedule")
    assert log.resource == "Schedule"


def test_audit_log_optional_fields():
    log = AuditLog(
        action="READ",
        resource="User",
        user_id="user-1",
        resource_id="123",
        details={"key": "value"},
        ip_address="127.0.0.1",
        correlation_id="corr-abc",
    )
    assert log.user_id == "user-1"
    assert log.resource_id == "123"
    assert log.details == {"key": "value"}
    assert log.ip_address == "127.0.0.1"
    assert log.correlation_id == "corr-abc"


def test_audit_log_unique_ids():
    log1 = AuditLog(action="A", resource="R")
    log2 = AuditLog(action="B", resource="S")
    assert log1.audit_id != log2.audit_id
