import pytest
from app.schemas.assignment.assignment_create import AssignmentCreateDTO
from app.schemas.assignment.assignment_update import AssignmentUpdateDTO
from app.schemas.assignment.assignment_response import AssignmentResponseDTO
from app.schemas.assignment.assignment_filters import AssignmentFilterDTO


def test_assignment_create_dto():
    dto = AssignmentCreateDTO(
        shift_id=1, doctor_id=1, start_time="08:00", end_time="20:00"
    )
    assert dto.shift_id == 1
    assert dto.start_time == "08:00"


def test_assignment_update_dto():
    dto = AssignmentUpdateDTO(start_time="09:00")
    assert dto.start_time == "09:00"


def test_assignment_response_dto():
    dto = AssignmentResponseDTO(
        id=1, shift_id=1, doctor_id=1,
        start_time="08:00", end_time="20:00", status="planned"
    )
    assert dto.id == 1
    assert dto.status == "planned"


def test_assignment_filter_dto_defaults():
    dto = AssignmentFilterDTO()
    assert dto.page == 1
    assert dto.size == 20
    assert dto.to_filters() == {}


def test_assignment_filter_dto_with_filters():
    dto = AssignmentFilterDTO(shift_id=1, status="confirmed")
    filters = dto.to_filters()
    assert filters["shift_id"] == 1
    assert filters["status"] == "confirmed"
