import pytest
from app.services.doctor_service import DoctorService
from app.schemas.doctor.doctor_create import DoctorCreateDTO
from app.schemas.doctor.doctor_update import DoctorUpdateDTO
from app.schemas.doctor.doctor_filters import DoctorFilterDTO
from app.database.unit_of_work import UnitOfWork


@pytest.fixture
def service(uow):
    return DoctorService(uow)


def test_service_list(service):
    filter_dto = DoctorFilterDTO(page=1, size=10)
    result = service.list(filter_dto)
    assert result.items == []
    assert result.total == 0


def test_service_create(service):
    dto = DoctorCreateDTO(name="Dr. Criado", crm="11111", hour_rate=150.0)
    result = service.create(dto)
    assert result.is_success
    assert result.data.name == "Dr. Criado"
    assert result.data.crm == "11111"


def test_service_create_duplicate_crm(service):
    dto = DoctorCreateDTO(name="Dr. First", crm="11111", hour_rate=150.0)
    service.create(dto)
    dto2 = DoctorCreateDTO(name="Dr. Second", crm="11111", hour_rate=200.0)
    result = service.create(dto2)
    assert result.is_failure
    assert "DOCTOR_ALREADY_EXISTS" in result.code


def test_service_get_by_id(service):
    dto = DoctorCreateDTO(name="Dr. Find", crm="22222", hour_rate=160.0)
    created = service.create(dto)
    result = service.get_by_id(created.data.id)
    assert result.is_success
    assert result.data.name == "Dr. Find"


def test_service_get_by_id_not_found(service):
    result = service.get_by_id(999)
    assert result.is_failure
    assert "DOCTOR_NOT_FOUND" in result.code


def test_service_update(service):
    dto = DoctorCreateDTO(name="Dr. Update", crm="33333", hour_rate=170.0)
    created = service.create(dto)
    update_dto = DoctorUpdateDTO(name="Dr. Updated")
    result = service.update(created.data.id, update_dto)
    assert result.is_success
    assert result.data.name == "Dr. Updated"


def test_service_update_not_found(service):
    update_dto = DoctorUpdateDTO(name="Dr. Ghost")
    result = service.update(999, update_dto)
    assert result.is_failure
    assert "DOCTOR_NOT_FOUND" in result.code


def test_service_update_duplicate_crm(service):
    dto1 = DoctorCreateDTO(name="Dr. First", crm="44444", hour_rate=150.0)
    service.create(dto1)
    dto2 = DoctorCreateDTO(name="Dr. Second", crm="55555", hour_rate=200.0)
    created2 = service.create(dto2)
    update_dto = DoctorUpdateDTO(crm="44444")
    result = service.update(created2.data.id, update_dto)
    assert result.is_failure
    assert "DOCTOR_ALREADY_EXISTS" in result.code


def test_service_delete(service):
    dto = DoctorCreateDTO(name="Dr. Delete", crm="66666", hour_rate=180.0)
    created = service.create(dto)
    result = service.delete(created.data.id)
    assert result.is_success
    assert result.data is True


def test_service_delete_not_found(service):
    result = service.delete(999)
    assert result.is_failure
    assert "DOCTOR_NOT_FOUND" in result.code
