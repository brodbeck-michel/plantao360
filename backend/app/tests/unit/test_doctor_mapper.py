from app.mappers.doctor_mapper import DoctorMapper
from app.schemas.doctor.doctor_create import DoctorCreateDTO
from app.models.doctor import Doctor


def test_mapper_to_response():
    mapper = DoctorMapper()
    doctor = Doctor(id=1, name="Dr. Map", crm="12345", hour_rate=150.0, active=True)
    dto = mapper.to_response(doctor)
    assert dto.id == 1
    assert dto.name == "Dr. Map"
    assert dto.crm == "12345"


def test_mapper_to_model():
    mapper = DoctorMapper()
    dto = DoctorCreateDTO(name="Dr. Map", crm="12345", hour_rate=150.0)
    model = mapper.to_model(dto)
    assert model.name == "Dr. Map"
    assert model.crm == "12345"


def test_mapper_to_response_list():
    mapper = DoctorMapper()
    doctors = [
        Doctor(id=1, name="Dr. A", crm="11111", hour_rate=100.0, active=True),
        Doctor(id=2, name="Dr. B", crm="22222", hour_rate=200.0, active=True),
    ]
    dtos = mapper.to_response_list(doctors)
    assert len(dtos) == 2
    assert dtos[0].name == "Dr. A"
    assert dtos[1].name == "Dr. B"


def test_mapper_update_model():
    mapper = DoctorMapper()
    doctor = Doctor(id=1, name="Dr. Old", crm="12345", hour_rate=100.0, active=True)
    dto = DoctorCreateDTO(name="Dr. New", crm="99999", hour_rate=200.0)
    updated = mapper.update_model(doctor, dto)
    assert updated.name == "Dr. New"
    assert updated.crm == "99999"
    assert updated.hour_rate == 200.0


def test_mapper_to_summary():
    mapper = DoctorMapper()
    doctor = Doctor(id=1, name="Dr. Summary", crm="12345", hour_rate=150.0, active=True)
    summary = mapper.to_summary(doctor)
    assert summary["id"] == 1
    assert summary["name"] == "Dr. Summary"
    assert summary["crm"] == "12345"
    assert summary["active"] is True
