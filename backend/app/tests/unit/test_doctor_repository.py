from datetime import date

from app.repositories.doctor_repository import DoctorRepository
from app.models.doctor import Doctor


def test_repository_create(db_session):
    repo = DoctorRepository(db_session)
    doctor = Doctor(name="Dr. Teste", crm="99999", has_rqe=False, career_start_date=date(2020, 1, 1))
    created = repo.create(doctor)
    db_session.commit()
    assert created.id is not None
    assert created.name == "Dr. Teste"


def test_repository_get_by_id(db_session):
    repo = DoctorRepository(db_session)
    doctor = Doctor(name="Dr. Busca", crm="88888", has_rqe=False, career_start_date=date(2020, 1, 1))
    db_session.add(doctor)
    db_session.commit()
    db_session.expire_all()
    found = repo.get_by_id(doctor.id)
    assert found is not None
    assert found.name == "Dr. Busca"


def test_repository_get_by_crm(db_session):
    repo = DoctorRepository(db_session)
    doctor = Doctor(name="Dr. CRM", crm="77777", has_rqe=False, career_start_date=date(2020, 1, 1))
    db_session.add(doctor)
    db_session.commit()
    db_session.expire_all()
    found = repo.get_by_crm("77777")
    assert found is not None
    assert found.crm == "77777"


def test_repository_exists_by_crm(db_session):
    repo = DoctorRepository(db_session)
    doctor = Doctor(name="Dr. Exists", crm="66666", has_rqe=False, career_start_date=date(2020, 1, 1))
    db_session.add(doctor)
    db_session.commit()
    assert repo.exists_by_crm("66666") is True
    assert repo.exists_by_crm("00000") is False


def test_repository_exists_by_crm_exclude_id(db_session):
    repo = DoctorRepository(db_session)
    doctor = Doctor(name="Dr. Exclude", crm="55555", has_rqe=False, career_start_date=date(2020, 1, 1))
    db_session.add(doctor)
    db_session.commit()
    assert repo.exists_by_crm("55555", exclude_id=doctor.id) is False
    assert repo.exists_by_crm("55555", exclude_id=999) is True


def test_repository_list(db_session):
    repo = DoctorRepository(db_session)
    db_session.add(Doctor(name="Dr. A", crm="11111", has_rqe=False, career_start_date=date(2020, 1, 1)))
    db_session.add(Doctor(name="Dr. B", crm="22222", has_rqe=False, career_start_date=date(2020, 1, 1)))
    db_session.commit()
    db_session.expire_all()
    doctors = repo.list()
    assert len(doctors) >= 2


def test_repository_search(db_session):
    repo = DoctorRepository(db_session)
    db_session.add(Doctor(name="Dr. Silva", crm="33333", has_rqe=False, career_start_date=date(2020, 1, 1)))
    db_session.commit()
    db_session.expire_all()
    results = repo.search(name="Silva")
    assert len(results) >= 1
    assert any(d.name == "Dr. Silva" for d in results)


def test_repository_count_filtered(db_session):
    repo = DoctorRepository(db_session)
    db_session.add(Doctor(name="Dr. Active", crm="AA111", has_rqe=False, career_start_date=date(2020, 1, 1), active=True))
    db_session.add(Doctor(name="Dr. Inactive", crm="BB222", has_rqe=False, career_start_date=date(2020, 1, 1), active=False))
    db_session.commit()
    assert repo.count_filtered(active=True) >= 1
    assert repo.count_filtered(active=False) >= 1


def test_repository_soft_delete(db_session):
    repo = DoctorRepository(db_session)
    doctor = Doctor(name="Dr. SoftDel", crm="SD111", has_rqe=False, career_start_date=date(2020, 1, 1))
    db_session.add(doctor)
    db_session.commit()
    db_session.expire_all()
    result = repo.soft_delete(doctor.id)
    assert result is True
    db_session.expire_all()
    updated = repo.get_by_id(doctor.id)
    assert updated.active is False


def test_repository_delete(db_session):
    repo = DoctorRepository(db_session)
    doctor = Doctor(name="Dr. Real Delete", crm="RD111", has_rqe=False, career_start_date=date(2020, 1, 1))
    db_session.add(doctor)
    db_session.commit()
    result = repo.delete(doctor.id)
    assert result is True
    assert repo.get_by_id(doctor.id) is None


def test_repository_count(db_session):
    repo = DoctorRepository(db_session)
    initial_count = repo.count()
    db_session.add(Doctor(name="Dr. Count", crm="CT111", has_rqe=False, career_start_date=date(2020, 1, 1)))
    db_session.commit()
    assert repo.count() == initial_count + 1
