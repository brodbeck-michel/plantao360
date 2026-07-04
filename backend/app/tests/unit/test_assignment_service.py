import pytest
from datetime import date, time
from unittest.mock import MagicMock, patch
from app.services.assignment_service import AssignmentService
from app.schemas.assignment.assignment_create import AssignmentCreateDTO
from app.schemas.assignment.assignment_update import AssignmentUpdateDTO
from app.schemas.assignment.assignment_filters import AssignmentFilterDTO
from app.domain.constants.assignment_status import AssignmentStatus


@pytest.fixture
def service():
    uow = MagicMock()
    uow.session = MagicMock()
    return AssignmentService(uow)


def _make_mock_assignment(**overrides):
    defaults = {
        "id": 1,
        "shift_id": 1,
        "doctor_id": 1,
        "start_time": time(8, 0),
        "end_time": time(20, 0),
        "status": AssignmentStatus.PLANNED,
        "duration_minutes": None,
    }
    defaults.update(overrides)
    entity = MagicMock()
    for k, v in defaults.items():
        setattr(entity, k, v)
    return entity


@patch("app.services.assignment_service.EventDispatcher")
@patch("app.services.assignment_service.ShiftPartRepository")
def test_create_assignment(mock_repo_cls, mock_ed_cls, service):
    mock_repo = mock_repo_cls.return_value
    created = _make_mock_assignment()
    mock_repo.create.return_value = created

    dto = AssignmentCreateDTO(
        shift_id=1, doctor_id=1, start_time="08:00", end_time="20:00"
    )
    result = service.create(dto)
    assert result.is_success
    assert result.data.id == 1


@patch("app.services.assignment_service.EventDispatcher")
@patch("app.services.assignment_service.ShiftPartRepository")
def test_confirm_assignment(mock_repo_cls, mock_ed_cls, service):
    mock_repo = mock_repo_cls.return_value
    entity = _make_mock_assignment(status=AssignmentStatus.PLANNED)
    confirmed = _make_mock_assignment(status=AssignmentStatus.CONFIRMED)
    mock_repo.get_by_id.return_value = entity
    mock_repo.update.return_value = confirmed

    result = service.confirm(1)
    assert result.is_success


@patch("app.services.assignment_service.EventDispatcher")
@patch("app.services.assignment_service.ShiftPartRepository")
def test_start_assignment(mock_repo_cls, mock_ed_cls, service):
    mock_repo = mock_repo_cls.return_value
    entity = _make_mock_assignment(status=AssignmentStatus.CONFIRMED)
    started = _make_mock_assignment(status=AssignmentStatus.STARTED)
    mock_repo.get_by_id.return_value = entity
    mock_repo.update.return_value = started

    result = service.start(1)
    assert result.is_success


@patch("app.services.assignment_service.EventDispatcher")
@patch("app.services.assignment_service.ShiftPartRepository")
def test_complete_assignment(mock_repo_cls, mock_ed_cls, service):
    mock_repo = mock_repo_cls.return_value
    entity = _make_mock_assignment(status=AssignmentStatus.STARTED)
    completed = _make_mock_assignment(status=AssignmentStatus.COMPLETED)
    mock_repo.get_by_id.return_value = entity
    mock_repo.update.return_value = completed

    result = service.complete(1)
    assert result.is_success


@patch("app.services.assignment_service.EventDispatcher")
@patch("app.services.assignment_service.ShiftPartRepository")
def test_cancel_assignment(mock_repo_cls, mock_ed_cls, service):
    mock_repo = mock_repo_cls.return_value
    entity = _make_mock_assignment(status=AssignmentStatus.PLANNED)
    cancelled = _make_mock_assignment(status=AssignmentStatus.CANCELLED)
    mock_repo.get_by_id.return_value = entity
    mock_repo.update.return_value = cancelled

    result = service.cancel(1)
    assert result.is_success


@patch("app.services.assignment_service.ShiftPartRepository")
def test_cancel_completed_fails(mock_repo_cls, service):
    mock_repo = mock_repo_cls.return_value
    entity = _make_mock_assignment(status=AssignmentStatus.COMPLETED)
    mock_repo.get_by_id.return_value = entity

    result = service.cancel(1)
    assert result.is_failure


@patch("app.services.assignment_service.ShiftPartRepository")
def test_get_not_found(mock_repo_cls, service):
    mock_repo = mock_repo_cls.return_value
    mock_repo.get_by_id.return_value = None

    result = service.get_by_id(999)
    assert result.is_failure


@patch("app.services.assignment_service.ShiftPartRepository")
def test_remove_assignment(mock_repo_cls, service):
    mock_repo = mock_repo_cls.return_value
    entity = _make_mock_assignment(status=AssignmentStatus.PLANNED)
    mock_repo.get_by_id.return_value = entity
    mock_repo.update.return_value = entity

    result = service.remove(1)
    assert result.is_success


@patch("app.services.assignment_service.ShiftPartRepository")
def test_remove_started_fails(mock_repo_cls, service):
    mock_repo = mock_repo_cls.return_value
    entity = _make_mock_assignment(status=AssignmentStatus.STARTED)
    mock_repo.get_by_id.return_value = entity

    result = service.remove(1)
    assert result.is_failure
