import pytest
from app.domain.base.aggregate_root import AggregateRoot


class TestLifecycleHooks:
    def test_before_transition_default_is_noop(self):
        agg = AggregateRoot()
        agg.before_transition("draft", "closed")

    def test_after_transition_default_is_noop(self):
        agg = AggregateRoot()
        agg.after_transition("closed", "draft")

    def test_hooks_can_be_overridden(self):
        class CustomAggregate(AggregateRoot):
            def __init__(self):
                super().__init__()
                self.transitions = []

            def before_transition(self, from_status, to_status):
                self.transitions.append(f"before:{from_status}->{to_status}")

            def after_transition(self, from_status, to_status):
                self.transitions.append(f"after:{from_status}->{to_status}")

        agg = CustomAggregate()
        agg.before_transition("draft", "closed")
        agg.after_transition("draft", "closed")
        assert agg.transitions == ["before:draft->closed", "after:draft->closed"]
