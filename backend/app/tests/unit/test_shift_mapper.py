import pytest
from datetime import date, datetime
from unittest.mock import MagicMock
from app.mappers.shift_mapper import ShiftMapper


def test_shift_mapper_to_response():
    mapper = ShiftMapper()
    entity = MagicMock()
    entity.id = 1
    entity.period_id = 1
    entity.shift_date = date(2025, 1, 15)
    entity.shift_type = "T1"
    entity.status = "scheduled"
    entity.scheduled_start = None
    entity.scheduled_end = None
    entity.actual_start = None
    entity.actual_end = None
    entity.total_duration_minutes = None
    entity.doctor_count = None
    entity.created_at = None
    entity.updated_at = None

    response = mapper.to_response(entity)
    assert response.id == 1
    assert response.shift_type == "T1"
    assert response.status == "scheduled"
