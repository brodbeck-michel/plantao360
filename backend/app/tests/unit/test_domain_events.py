from app.domain.events.event_names import DomainEventName


def test_domain_event_name_values():
    values = DomainEventName.values()
    assert "doctor.created.v1" in values
    assert "doctor.updated.v1" in values
    assert "doctor.deactivated.v1" in values
    assert "period.created.v1" in values
    assert "period.updated.v1" in values
    assert "period.closed.v1" in values
    assert "period.reopened.v1" in values
    assert "shift.created.v1" in values
    assert "shift.updated.v1" in values
    assert "shift.deleted.v1" in values
    assert "extra.created.v1" in values
    assert "extra.deleted.v1" in values


def test_domain_event_name_members():
    assert DomainEventName.DOCTOR_CREATED_V1 == "doctor.created.v1"
    assert DomainEventName.SHIFT_DELETED_V1 == "shift.deleted.v1"
    assert DomainEventName.EXTRA_CREATED_V1 == "extra.created.v1"


def test_domain_event_name_is_str_enum():
    assert issubclass(DomainEventName, str)
