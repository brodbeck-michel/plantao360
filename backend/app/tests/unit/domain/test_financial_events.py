"""Tests for financial domain events."""

from app.domain.events.event_names import DomainEventName


class TestFinancialEvents:
    def test_coverage_consolidated_event_exists(self):
        assert DomainEventName.COVERAGE_CONSOLIDATED_V1 == "coverage.consolidated.v1"

    def test_financial_snapshot_created_event_exists(self):
        assert DomainEventName.FINANCIAL_SNAPSHOT_CREATED_V1 == "financial.snapshot.created.v1"

    def test_financial_fact_generated_event_exists(self):
        assert DomainEventName.FINANCIAL_FACT_GENERATED_V1 == "financial.fact.generated.v1"

    def test_financial_fact_revoked_event_exists(self):
        assert DomainEventName.FINANCIAL_FACT_REVOKED_V1 == "financial.fact.revoked.v1"

    def test_financial_events_are_versioned(self):
        events = DomainEventName.values()
        financial_events = [e for e in events if e.startswith("financial.") or e.startswith("coverage.")]
        for event in financial_events:
            assert ".v1" in event, f"Event {event} is not versioned"

