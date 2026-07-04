import pytest
from app.domain.base.aggregate_root import AggregateRoot


class TestAggregateRoot:
    def test_version_starts_at_1(self):
        agg = AggregateRoot()
        assert agg.version == 1

    def test_aggregate_id_returns_none_without_model(self):
        agg = AggregateRoot()
        assert agg.aggregate_id is None

    def test_aggregate_id_returns_model_id(self):
        class FakeModel:
            id = 42
        agg = AggregateRoot()
        agg.id = 42
        assert agg.aggregate_id == 42

    def test_add_event_stores_event(self):
        agg = AggregateRoot()
        agg.add_event("test.event.v1", {"key": "value"})
        assert len(agg.pending_events) == 1
        assert agg.pending_events[0]["name"] == "test.event.v1"
        assert agg.pending_events[0]["data"] == {"key": "value"}

    def test_add_event_default_empty_data(self):
        agg = AggregateRoot()
        agg.add_event("test.event.v1")
        assert agg.pending_events[0]["data"] == {}

    def test_clear_events(self):
        agg = AggregateRoot()
        agg.add_event("e1")
        agg.add_event("e2")
        agg.clear_events()
        assert len(agg.pending_events) == 0

    def test_pending_events_returns_copy(self):
        agg = AggregateRoot()
        agg.add_event("e1")
        events = agg.pending_events
        events.clear()
        assert len(agg.pending_events) == 1

    def test_before_transition_is_noop(self):
        agg = AggregateRoot()
        agg.before_transition("a", "b")

    def test_after_transition_is_noop(self):
        agg = AggregateRoot()
        agg.after_transition("a", "b")

    def test_multiple_events(self):
        agg = AggregateRoot()
        agg.add_event("e1")
        agg.add_event("e2")
        agg.add_event("e3")
        assert len(agg.pending_events) == 3
