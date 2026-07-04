import pytest
from app.domain.events.event_collector import EventCollector


class TestEventCollector:
    def test_add_event(self):
        collector = EventCollector()
        collector.add("test.v1", {"key": "value"})
        assert len(collector) == 1
        assert collector.events[0]["name"] == "test.v1"
        assert collector.events[0]["data"] == {"key": "value"}

    def test_add_event_default_empty_data(self):
        collector = EventCollector()
        collector.add("test.v1")
        assert collector.events[0]["data"] == {}

    def test_clear(self):
        collector = EventCollector()
        collector.add("e1")
        collector.add("e2")
        collector.clear()
        assert len(collector) == 0

    def test_events_returns_copy(self):
        collector = EventCollector()
        collector.add("e1")
        events = collector.events
        events.clear()
        assert len(collector) == 1

    def test_len(self):
        collector = EventCollector()
        assert len(collector) == 0
        collector.add("e1")
        assert len(collector) == 1

    def test_bool_empty(self):
        collector = EventCollector()
        assert not bool(collector)

    def test_bool_with_events(self):
        collector = EventCollector()
        collector.add("e1")
        assert bool(collector)

    def test_multiple_events(self):
        collector = EventCollector()
        collector.add("e1")
        collector.add("e2")
        collector.add("e3")
        names = [e["name"] for e in collector.events]
        assert names == ["e1", "e2", "e3"]
