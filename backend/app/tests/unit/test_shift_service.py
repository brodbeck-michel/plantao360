import pytest
from datetime import date, datetime
from unittest.mock import MagicMock, patch
from app.services.shift_service import ShiftService
from app.schemas.shift.shift_create import ShiftCreateDTO
from app.schemas.shift.shift_update import ShiftUpdateDTO
from app.domain.constants.shift_status import ShiftStatus


@pytest.fixture
def service():
    uow = MagicMock()
    uow.session = MagicMock()
    return ShiftService(uow)


def _make_mock_shift(**overrides):
    defaults = {
        "id": 1,
        "period_id": 1,
        "shift_date": date(2025, 1, 15),
        "shift_type": "T1",
        "status": ShiftStatus.SCHEDULED,
        "scheduled_start": None,
        "scheduled_end": None,
        "actual_start": None,
        "actual_end": None,
        "total_duration_minutes": None,
        "doctor_count": None,
        "created_at": None,
        "updated_at": None,
    }
    defaults.update(overrides)
    entity = MagicMock()
    for k, v in defaults.items():
        setattr(entity, k, v)
    return entity


@patch("app.services.shift_service.EventDispatcher")
@patch("app.services.shift_service.ShiftRepository")
def test_create_shift(mock_repo_cls, mock_ed_cls, service):
    mock_repo = mock_repo_cls.return_value
    created = _make_mock_shift()
    mock_repo.create.return_value = created

    dto = ShiftCreateDTO(
        period_id=1,
        shift_date=date(2025, 1, 15),
        shift_type="T1",
    )
    # O serviço valida a data dentro da competência do período. A competência do mês M
    # vai do dia 26 de M ao dia 25 de M+1; logo 15/01/2025 pertence à competência de
    # dez/2024 (26/12/2024 a 25/01/2025). Mocka o período correspondente.
    from app.models.period import Period
    service.uow.session.query.return_value.filter.return_value.first.return_value = Period(
        id=1, year=2024, month=12
    )
    result = service.create(dto)
    assert result.is_success
    assert result.data.id == 1
    mock_repo.create.assert_called_once()


@patch("app.services.shift_service.EventDispatcher")
@patch("app.services.shift_service.ShiftRepository")
def test_start_shift(mock_repo_cls, mock_ed_cls, service):
    mock_repo = mock_repo_cls.return_value
    entity = _make_mock_shift(status=ShiftStatus.SCHEDULED)
    started = _make_mock_shift(status=ShiftStatus.IN_PROGRESS)
    mock_repo.get_by_id.return_value = entity
    mock_repo.update.return_value = started

    result = service.start(1)
    assert result.is_success
    assert mock_repo.update.called


@patch("app.services.shift_service.EventDispatcher")
@patch("app.services.shift_service.ShiftRepository")
def test_complete_shift(mock_repo_cls, mock_ed_cls, service):
    mock_repo = mock_repo_cls.return_value
    entity = _make_mock_shift(status=ShiftStatus.IN_PROGRESS)
    completed = _make_mock_shift(status=ShiftStatus.COMPLETED)
    mock_repo.get_by_id.return_value = entity
    mock_repo.update.return_value = completed

    result = service.complete(1)
    assert result.is_success


@patch("app.services.shift_service.EventDispatcher")
@patch("app.services.shift_service.ShiftRepository")
def test_cancel_shift(mock_repo_cls, mock_ed_cls, service):
    mock_repo = mock_repo_cls.return_value
    entity = _make_mock_shift(status=ShiftStatus.SCHEDULED)
    cancelled = _make_mock_shift(status=ShiftStatus.CANCELLED)
    mock_repo.get_by_id.return_value = entity
    mock_repo.update.return_value = cancelled

    result = service.cancel(1)
    assert result.is_success


@patch("app.services.shift_service.ShiftRepository")
def test_cancel_completed_shift_fails(mock_repo_cls, service):
    mock_repo = mock_repo_cls.return_value
    entity = _make_mock_shift(status=ShiftStatus.COMPLETED)
    mock_repo.get_by_id.return_value = entity

    result = service.cancel(1)
    assert result.is_failure


@patch("app.services.shift_service.ShiftRepository")
def test_get_shift_not_found(mock_repo_cls, service):
    mock_repo = mock_repo_cls.return_value
    mock_repo.get_by_id.return_value = None

    result = service.get_by_id(999)
    assert result.is_failure


@patch("app.services.shift_service.ShiftRepository")
def test_update_shift_immutable(mock_repo_cls, service):
    mock_repo = mock_repo_cls.return_value
    entity = _make_mock_shift(status=ShiftStatus.COMPLETED)
    mock_repo.get_by_id.return_value = entity

    dto = ShiftUpdateDTO(shift_type="T3")
    result = service.update(1, dto)
    assert result.is_failure
