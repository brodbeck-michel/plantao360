import pytest
from app.domain.base.aggregate_root import AggregateRoot


class TestAggregateVersion:
    def test_version_starts_at_1(self):
        agg = AggregateRoot()
        assert agg.version == 1

    def test_version_is_int(self):
        agg = AggregateRoot()
        assert isinstance(agg.version, int)
