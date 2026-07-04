"""Tests for remuneration domain events."""

from app.domain.events.event_names import DomainEventName


class TestRemunerationEvents:
    def test_remuneration_calculated_event(self):
        assert DomainEventName.REMUNERATION_CALCULATED_V1 == "remuneration.calculated.v1"

    def test_remuneration_simulated_event(self):
        assert DomainEventName.REMUNERATION_SIMULATED_V1 == "remuneration.simulated.v1"

    def test_remuneration_recalculated_event(self):
        assert DomainEventName.REMUNERATION_RECALCULATED_V1 == "remuneration.recalculated.v1"

    def test_remuneration_invalidated_event(self):
        assert DomainEventName.REMUNERATION_INVALIDATED_V1 == "remuneration.invalidated.v1"

    def test_remuneration_events_are_versioned(self):
        events = DomainEventName.values()
        rem_events = [e for e in events if e.startswith("remuneration.")]
        for event in rem_events:
            assert ".v1" in event

    def test_total_events_count(self):
        events = DomainEventName.values()
        assert len(events) == 38
