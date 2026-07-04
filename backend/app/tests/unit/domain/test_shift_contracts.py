import pytest
from app.domain.contracts.shift_contracts import AssignDoctor, RemoveDoctor, ValidateCoverage, ValidateOverlap


def test_assign_doctor():
    contract = AssignDoctor(doctor_id=1, shift_id=1, start_time="08:00", end_time="20:00")
    assert contract.doctor_id == 1
    assert contract.shift_id == 1


def test_remove_doctor():
    contract = RemoveDoctor(doctor_id=1, shift_id=1)
    assert contract.doctor_id == 1
    assert contract.shift_id == 1


def test_validate_coverage():
    contract = ValidateCoverage(shift_id=1, min_doctors=2, max_doctors=5)
    assert contract.shift_id == 1
    assert contract.min_doctors == 2
    assert contract.max_doctors == 5


def test_validate_overlap():
    contract = ValidateOverlap(doctor_id=1, shift_id=1, start_time="08:00", end_time="20:00")
    assert contract.doctor_id == 1
    assert contract.shift_id == 1
