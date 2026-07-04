import pytest
from datetime import datetime, timezone
from app.domain.transitions.period_transition import PeriodTransition
from app.domain.constants.period_status import PeriodStatus
from app.domain.events.event_names import DomainEventName


class TestPeriodTransition:
    def test_create_transition(self):
        ts = PeriodTransition(
            period_id=1,
            previous_status=PeriodStatus.DRAFT,
            new_status=PeriodStatus.CLOSED,
            user="admin",
            timestamp=datetime(2026, 6, 26, tzinfo=timezone.utc),
            reason="Month ended",
            event_name=DomainEventName.PERIOD_CLOSED_V1,
        )
        assert ts.period_id == 1
        assert ts.previous_status == PeriodStatus.DRAFT
        assert ts.new_status == PeriodStatus.CLOSED
        assert ts.user == "admin"
        assert ts.reason == "Month ended"

    def test_transition_is_frozen(self):
        ts = PeriodTransition(
            period_id=1,
            previous_status=PeriodStatus.DRAFT,
            new_status=PeriodStatus.CLOSED,
            user="admin",
            timestamp=datetime(2026, 6, 26, tzinfo=timezone.utc),
        )
        with pytest.raises(AttributeError):
            ts.period_id = 2

    def test_to_dict(self):
        ts = PeriodTransition(
            period_id=1,
            previous_status=PeriodStatus.DRAFT,
            new_status=PeriodStatus.CLOSED,
            user="admin",
            timestamp=datetime(2026, 6, 26, tzinfo=timezone.utc),
            event_name=DomainEventName.PERIOD_CLOSED_V1,
        )
        d = ts.to_dict()
        assert d["period_id"] == 1
        assert d["previous_status"] == PeriodStatus.DRAFT
        assert d["new_status"] == PeriodStatus.CLOSED
        assert d["user"] == "admin"
        assert d["event_name"] == DomainEventName.PERIOD_CLOSED_V1

    def test_to_dict_defaults(self):
        ts = PeriodTransition(
            period_id=1,
            previous_status=PeriodStatus.CLOSED,
            new_status=PeriodStatus.DRAFT,
            user="admin",
            timestamp=datetime(2026, 6, 26, tzinfo=timezone.utc),
        )
        d = ts.to_dict()
        assert d["reason"] == ""
        assert d["event_name"] is None
