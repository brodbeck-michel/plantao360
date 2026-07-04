"""Tests for payroll domain events."""

from app.domain.events.event_names import DomainEventName


class TestPayrollEvents:
    def test_payroll_created_event(self):
        assert DomainEventName.PAYROLL_CREATED_V1 == "payroll.created.v1"

    def test_payroll_calculated_event(self):
        assert DomainEventName.PAYROLL_CALCULATED_V1 == "payroll.calculated.v1"

    def test_payroll_reviewed_event(self):
        assert DomainEventName.PAYROLL_REVIEWED_V1 == "payroll.reviewed.v1"

    def test_payroll_approved_event(self):
        assert DomainEventName.PAYROLL_APPROVED_V1 == "payroll.approved.v1"

    def test_payroll_exported_event(self):
        assert DomainEventName.PAYROLL_EXPORTED_V1 == "payroll.exported.v1"

    def test_payroll_paid_event(self):
        assert DomainEventName.PAYROLL_PAID_V1 == "payroll.paid.v1"

    def test_payroll_archived_event(self):
        assert DomainEventName.PAYROLL_ARCHIVED_V1 == "payroll.archived.v1"

    def test_payroll_reopened_event(self):
        assert DomainEventName.PAYROLL_REOPENED_V1 == "payroll.reopened.v1"

    def test_all_payroll_events_are_versioned(self):
        events = DomainEventName.values()
        payroll_events = [e for e in events if e.startswith("payroll.")]
        for event in payroll_events:
            assert ".v1" in event, f"Event {event} is not versioned"

    def test_payroll_events_count(self):
        events = DomainEventName.values()
        payroll_events = [e for e in events if e.startswith("payroll.")]
        assert len(payroll_events) == 13

    def test_total_event_count(self):
        events = DomainEventName.values()
        assert len(events) == 43
