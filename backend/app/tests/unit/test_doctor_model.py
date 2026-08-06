from datetime import date

import pytest

from app.models.doctor import Doctor


def test_doctor_repr(db_session):
    doctor = Doctor(name="Dr. João", crm="12345", has_rqe=False, career_start_date=date(2020, 1, 1))
    db_session.add(doctor)
    db_session.commit()
    assert "Dr. João" in repr(doctor)
    assert "12345" in repr(doctor)


def test_doctor_hour_rate_is_computed_from_career_start_date():
    doctor = Doctor(name="Dr. Rate", crm="99999", has_rqe=False, career_start_date=date(2020, 1, 1))
    assert isinstance(doctor.hour_rate, float)
    assert doctor.hour_rate > 0
    assert doctor.hour_rate_tier.startswith("M-")


def test_doctor_hour_rate_cannot_be_set_directly():
    doctor = Doctor(name="Dr. Rate", crm="88888", has_rqe=False, career_start_date=date(2020, 1, 1))
    with pytest.raises(AttributeError):
        doctor.hour_rate = 150.0
