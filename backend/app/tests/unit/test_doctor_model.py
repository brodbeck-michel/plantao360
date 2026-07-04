from app.models.doctor import Doctor


def test_doctor_repr(db_session):
    doctor = Doctor(name="Dr. João", crm="12345", hour_rate=150.0)
    db_session.add(doctor)
    db_session.commit()
    assert "Dr. João" in repr(doctor)
    assert "12345" in repr(doctor)
