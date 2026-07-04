from datetime import datetime

from app.common.events import DomainEvent
from app.common.identifiers import is_valid_uuid


def test_domain_event_has_event_id():
    event = DomainEvent(event_name="TestEvent")
    assert event.event_id is not None
    assert is_valid_uuid(event.event_id)


def test_domain_event_has_event_name():
    event = DomainEvent(event_name="UserCreated")
    assert event.event_name == "UserCreated"


def test_domain_event_has_created_at():
    event = DomainEvent(event_name="Test")
    assert isinstance(event.created_at, datetime)


def test_domain_event_has_correlation_id():
    event = DomainEvent(
        event_name="Test", correlation_id="corr-123"
    )
    assert event.correlation_id == "corr-123"


def test_domain_event_correlation_id_optional():
    event = DomainEvent(event_name="Test")
    assert event.correlation_id is None


def test_domain_event_unique_ids():
    event1 = DomainEvent(event_name="A")
    event2 = DomainEvent(event_name="B")
    assert event1.event_id != event2.event_id
