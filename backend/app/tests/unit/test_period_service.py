import pytest
from app.use_cases.periods import (
    CreatePeriod, UpdatePeriod, ClosePeriod, ReopenPeriod,
    GetPeriod, ListPeriods,
)
from app.repositories.period_repository import PeriodRepository
from app.schemas.period.period_create import PeriodCreateDTO
from app.schemas.period.period_update import PeriodUpdateDTO
from app.schemas.period.period_filters import PeriodFilterDTO
from app.models.period import Period
from app.domain.constants.period_status import PeriodStatus


@pytest.fixture
def repo(db_session):
    return PeriodRepository(db_session)


class TestCreatePeriod:
    def test_create_success(self, repo):
        dto = PeriodCreateDTO(year=2026, month=6)
        use_case = CreatePeriod(repo)
        result = use_case(dto=dto)
        assert result.is_success
        assert result.data.year == 2026
        assert result.data.month == 6
        assert result.data.status == "draft"

    def test_create_duplicate(self, repo):
        dto = PeriodCreateDTO(year=2026, month=6)
        use_case = CreatePeriod(repo)
        use_case(dto=dto)
        result = use_case(dto=dto)
        assert result.is_failure
        assert "PERIOD_ALREADY_EXISTS" in result.code


class TestGetPeriod:
    def test_get_success(self, repo):
        dto = PeriodCreateDTO(year=2026, month=6)
        created = CreatePeriod(repo)(dto=dto)
        use_case = GetPeriod(repo)
        result = use_case(id=created.data.id)
        assert result.is_success
        assert result.data.year == 2026

    def test_get_not_found(self, repo):
        use_case = GetPeriod(repo)
        result = use_case(id=999)
        assert result.is_failure
        assert "PERIOD_NOT_FOUND" in result.code


class TestUpdatePeriod:
    def test_update_success(self, repo):
        dto = PeriodCreateDTO(year=2026, month=6)
        created = CreatePeriod(repo)(dto=dto)
        update_dto = PeriodUpdateDTO(month=7)
        use_case = UpdatePeriod(repo)
        result = use_case(id=created.data.id, dto=update_dto)
        assert result.is_success
        assert result.data.month == 7

    def test_update_not_found(self, repo):
        update_dto = PeriodUpdateDTO(month=7)
        use_case = UpdatePeriod(repo)
        result = use_case(id=999, dto=update_dto)
        assert result.is_failure
        assert "PERIOD_NOT_FOUND" in result.code

    def test_update_closed_period(self, repo):
        dto = PeriodCreateDTO(year=2026, month=6)
        created = CreatePeriod(repo)(dto=dto)
        ClosePeriod(repo)(id=created.data.id)
        update_dto = PeriodUpdateDTO(month=7)
        use_case = UpdatePeriod(repo)
        result = use_case(id=created.data.id, dto=update_dto)
        assert result.is_failure
        assert "PERIOD_IMMUTABLE" in result.code


class TestClosePeriod:
    def test_close_success(self, repo):
        dto = PeriodCreateDTO(year=2026, month=6)
        created = CreatePeriod(repo)(dto=dto)
        use_case = ClosePeriod(repo)
        result = use_case(id=created.data.id)
        assert result.is_success
        assert result.data.status == "closed"

    def test_close_not_found(self, repo):
        use_case = ClosePeriod(repo)
        result = use_case(id=999)
        assert result.is_failure
        assert "PERIOD_NOT_FOUND" in result.code

    def test_close_already_closed(self, repo):
        dto = PeriodCreateDTO(year=2026, month=6)
        created = CreatePeriod(repo)(dto=dto)
        ClosePeriod(repo)(id=created.data.id)
        use_case = ClosePeriod(repo)
        result = use_case(id=created.data.id)
        assert result.is_failure
        assert "PERIOD_ALREADY_CLOSED" in result.code


class TestReopenPeriod:
    def test_reopen_success(self, repo):
        dto = PeriodCreateDTO(year=2026, month=6)
        created = CreatePeriod(repo)(dto=dto)
        ClosePeriod(repo)(id=created.data.id)
        use_case = ReopenPeriod(repo)
        result = use_case(id=created.data.id)
        assert result.is_success
        assert result.data.status == "draft"

    def test_reopen_not_found(self, repo):
        use_case = ReopenPeriod(repo)
        result = use_case(id=999)
        assert result.is_failure
        assert "PERIOD_NOT_FOUND" in result.code

    def test_reopen_already_draft(self, repo):
        dto = PeriodCreateDTO(year=2026, month=6)
        created = CreatePeriod(repo)(dto=dto)
        use_case = ReopenPeriod(repo)
        result = use_case(id=created.data.id)
        assert result.is_failure


class TestListPeriods:
    def test_list_empty(self, repo):
        use_case = ListPeriods(repo)
        result = use_case(filter_dto=PeriodFilterDTO(page=1, size=10))
        assert result.is_success
        assert result.data.items == []
        assert result.data.total == 0

    def test_list_with_data(self, repo):
        CreatePeriod(repo)(dto=PeriodCreateDTO(year=2026, month=6))
        CreatePeriod(repo)(dto=PeriodCreateDTO(year=2026, month=7))
        use_case = ListPeriods(repo)
        result = use_case(filter_dto=PeriodFilterDTO(page=1, size=10))
        assert result.is_success
        assert result.data.total == 2

    def test_list_filter_by_status(self, repo):
        CreatePeriod(repo)(dto=PeriodCreateDTO(year=2026, month=6))
        created = CreatePeriod(repo)(dto=PeriodCreateDTO(year=2026, month=7))
        ClosePeriod(repo)(id=created.data.id)
        use_case = ListPeriods(repo)
        result = use_case(filter_dto=PeriodFilterDTO(page=1, size=10, status="draft"))
        assert result.is_success
        assert result.data.total == 1
