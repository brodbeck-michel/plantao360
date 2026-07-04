import pytest
from app.domain.contracts.period_contract import PeriodContract
from app.domain.constants.period_status import PeriodStatus


class TestPeriodContract:
    def test_create_contract(self):
        contract = PeriodContract(
            period_id=1, year=2026, month=6, status=PeriodStatus.DRAFT,
        )
        assert contract.period_id == 1
        assert contract.year == 2026
        assert contract.month == 6
        assert contract.status == PeriodStatus.DRAFT

    def test_can_be_queried(self):
        contract = PeriodContract(
            period_id=1, year=2026, month=6, status=PeriodStatus.DRAFT,
        )
        assert contract.can_be_queried()

    def test_can_be_validated(self):
        contract = PeriodContract(
            period_id=1, year=2026, month=6, status=PeriodStatus.DRAFT,
        )
        assert contract.can_be_validated()

    def test_cannot_be_closed_by_external(self):
        contract = PeriodContract(
            period_id=1, year=2026, month=6, status=PeriodStatus.DRAFT,
        )
        assert not contract.can_be_closed_by_external()

    def test_cannot_change_status_by_external(self):
        contract = PeriodContract(
            period_id=1, year=2026, month=6, status=PeriodStatus.CLOSED,
        )
        assert not contract.can_status_be_changed_by_external()

    def test_cannot_reopen_by_external(self):
        contract = PeriodContract(
            period_id=1, year=2026, month=6, status=PeriodStatus.CLOSED,
        )
        assert not contract.can_be_reopened_by_external()

    def test_cannot_modify_dates_by_external(self):
        contract = PeriodContract(
            period_id=1, year=2026, month=6, status=PeriodStatus.DRAFT,
        )
        assert not contract.can_dates_be_modified_by_external()

    def test_to_dict(self):
        contract = PeriodContract(
            period_id=1, year=2026, month=6, status=PeriodStatus.DRAFT,
        )
        d = contract.to_dict()
        assert d["period_id"] == 1
        assert d["permissions"]["query"] is True
        assert d["permissions"]["close"] is False
        assert d["permissions"]["reopen"] is False
        assert d["permissions"]["modify_dates"] is False

    def test_contract_is_frozen(self):
        contract = PeriodContract(
            period_id=1, year=2026, month=6, status=PeriodStatus.DRAFT,
        )
        with pytest.raises(AttributeError):
            contract.period_id = 2
