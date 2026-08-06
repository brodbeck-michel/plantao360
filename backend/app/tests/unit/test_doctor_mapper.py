from datetime import date

from app.mappers.doctor_mapper import DoctorMapper
from app.schemas.doctor.doctor_create import DoctorCreateDTO
from app.models.doctor import Doctor


def test_mapper_to_response():
    mapper = DoctorMapper()
    doctor = Doctor(id=1, name="Dr. Map", crm="12345", has_rqe=False, career_start_date=date(2020, 1, 1), active=True, specialty="Clinica Medica", doctor_type="plantonista")
    dto = mapper.to_response(doctor)
    assert dto.id == 1
    assert dto.name == "Dr. Map"
    assert dto.crm == "12345"


def test_mapper_to_model():
    mapper = DoctorMapper()
    dto = DoctorCreateDTO(name="Dr. Map", crm="12345", has_rqe=False, career_start_date=date(2020, 1, 1))
    model = mapper.to_model(dto)
    assert model.name == "Dr. Map"
    assert model.crm == "12345"


def test_mapper_to_response_list():
    mapper = DoctorMapper()
    doctors = [
        Doctor(id=1, name="Dr. A", crm="11111", has_rqe=False, career_start_date=date(2020, 1, 1), active=True, specialty="Clinica Medica", doctor_type="plantonista"),
        Doctor(id=2, name="Dr. B", crm="22222", has_rqe=False, career_start_date=date(2020, 1, 1), active=True, specialty="Clinica Medica", doctor_type="plantonista"),
    ]
    dtos = mapper.to_response_list(doctors)
    assert len(dtos) == 2
    assert dtos[0].name == "Dr. A"
    assert dtos[1].name == "Dr. B"


def test_mapper_update_model():
    mapper = DoctorMapper()
    doctor = Doctor(id=1, name="Dr. Old", crm="12345", has_rqe=False, career_start_date=date(2018, 1, 1), active=True, specialty="Clinica Medica", doctor_type="plantonista")
    dto = DoctorCreateDTO(name="Dr. New", crm="99999", has_rqe=True, career_start_date=date(2010, 1, 1))
    updated = mapper.update_model(doctor, dto)
    assert updated.name == "Dr. New"
    assert updated.crm == "99999"
    assert updated.has_rqe is True
    assert updated.career_start_date == date(2010, 1, 1)
    assert updated.hour_rate_tier.startswith("E-")


def test_mapper_to_summary():
    mapper = DoctorMapper()
    doctor = Doctor(id=1, name="Dr. Summary", crm="12345", has_rqe=False, career_start_date=date(2020, 1, 1), active=True, specialty="Clinica Medica", doctor_type="plantonista")
    summary = mapper.to_summary(doctor)
    assert summary["id"] == 1
    assert summary["name"] == "Dr. Summary"
    assert summary["crm"] == "12345"
    assert summary["active"] is True
