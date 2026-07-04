import pytest
from app.domain.value_objects.doctor_reference import DoctorReference


def test_doctor_reference_valid():
    ref = DoctorReference(doctor_id=1, doctor_name="Dr. Silva", crm="12345")
    assert ref.doctor_id == 1


def test_doctor_reference_invalid():
    with pytest.raises(ValueError, match="Invalid"):
        DoctorReference(doctor_id=0)
