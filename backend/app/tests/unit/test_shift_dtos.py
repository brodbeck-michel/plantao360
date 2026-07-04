import pytest
from app.schemas.shift.shift_create import ShiftCreateDTO
from app.schemas.shift.shift_update import ShiftUpdateDTO
from app.schemas.shift.shift_response import ShiftResponseDTO
from app.schemas.shift.shift_summary import ShiftSummaryDTO
from app.schemas.shift.shift_filters import ShiftFilterDTO
from datetime import date, datetime


def test_shift_create_dto():
    dto = ShiftCreateDTO(
        period_id=1,
        shift_date=date(2025, 1, 15),
        shift_type="T1",
    )
    assert dto.period_id == 1
    assert dto.shift_type == "T1"


def test_shift_create_dto_with_times():
    dto = ShiftCreateDTO(
        period_id=1,
        shift_date=date(2025, 1, 15),
        shift_type="T2",
        scheduled_start=datetime(2025, 1, 15, 8, 0),
        scheduled_end=datetime(2025, 1, 15, 20, 0),
    )
    assert dto.scheduled_start is not None


def test_shift_update_dto():
    dto = ShiftUpdateDTO(shift_type="T3")
    assert dto.shift_type == "T3"


def test_shift_response_dto():
    dto = ShiftResponseDTO(
        id=1,
        period_id=1,
        shift_date=date(2025, 1, 15),
        shift_type="T1",
        status="scheduled",
    )
    assert dto.id == 1
    assert dto.status == "scheduled"


def test_shift_summary_dto():
    dto = ShiftSummaryDTO(
        id=1,
        shift_date=date(2025, 1, 15),
        shift_type="T1",
        status="scheduled",
    )
    assert dto.id == 1


def test_shift_filter_dto_defaults():
    dto = ShiftFilterDTO()
    assert dto.page == 1
    assert dto.size == 20
    assert dto.to_filters() == {}


def test_shift_filter_dto_with_filters():
    dto = ShiftFilterDTO(period_id=1, status="scheduled")
    filters = dto.to_filters()
    assert filters["period_id"] == 1
    assert filters["status"] == "scheduled"
