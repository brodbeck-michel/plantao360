import pytest
from datetime import date, time
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import Session

from app.database.base import Base
from app.models import Doctor, Period, Shift, ShiftPart, ShiftExtra
from app.domain.constants.shift_types import ShiftType
from app.domain.constants.period_status import PeriodStatus


@pytest.fixture(scope="function")
def engine():
    eng = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)


@pytest.fixture(scope="function")
def session(engine):
    with Session(engine) as sess:
        yield sess


def test_doctors_table_exists(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "doctors" in tables


def test_periods_table_exists(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "periods" in tables


def test_shifts_table_exists(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "shifts" in tables


def test_shift_parts_table_exists(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "shift_parts" in tables


def test_shift_extras_table_exists(engine):
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "shift_extras" in tables


def test_doctor_create(session):
    doctor = Doctor(name="Dr. João", crm="12345", hour_rate=150.0)
    session.add(doctor)
    session.commit()
    assert doctor.id is not None
    assert doctor.active is True


def test_doctor_hour_rate_positive(session):
    from sqlalchemy.exc import IntegrityError

    doctor = Doctor(name="Dr. Test", crm="99999", hour_rate=-10.0)
    session.add(doctor)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_doctor_crm_unique(session):
    from sqlalchemy.exc import IntegrityError

    d1 = Doctor(name="Dr. A", crm="UNIQUE01", hour_rate=100.0)
    d2 = Doctor(name="Dr. B", crm="UNIQUE01", hour_rate=200.0)
    session.add(d1)
    session.commit()
    session.add(d2)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_period_create(session):
    period = Period(year=2026, month=1, status=PeriodStatus.DRAFT)
    session.add(period)
    session.commit()
    assert period.id is not None
    assert period.status == PeriodStatus.DRAFT


def test_period_unique_year_month(session):
    from sqlalchemy.exc import IntegrityError

    p1 = Period(year=2026, month=6, status=PeriodStatus.DRAFT)
    p2 = Period(year=2026, month=6, status=PeriodStatus.CLOSED)
    session.add(p1)
    session.commit()
    session.add(p2)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_period_month_range(session):
    from sqlalchemy.exc import IntegrityError

    period = Period(year=2026, month=13, status=PeriodStatus.DRAFT)
    session.add(period)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_shift_create(session):
    doctor = Doctor(name="Dr. Shift", crm="SHIFT01", hour_rate=100.0)
    session.add(doctor)
    session.flush()
    period = Period(year=2026, month=1, status=PeriodStatus.DRAFT)
    session.add(period)
    session.flush()
    shift = Shift(
        period_id=period.id,
        shift_date=date(2026, 1, 15),
        shift_type=ShiftType.T1,
    )
    session.add(shift)
    session.commit()
    assert shift.id is not None


def test_shift_unique_date_type(session):
    from sqlalchemy.exc import IntegrityError

    doctor = Doctor(name="Dr. Dup", crm="DUP01", hour_rate=100.0)
    session.add(doctor)
    session.flush()
    period = Period(year=2026, month=2, status=PeriodStatus.DRAFT)
    session.add(period)
    session.flush()
    s1 = Shift(
        period_id=period.id,
        shift_date=date(2026, 2, 10),
        shift_type=ShiftType.T1,
    )
    s2 = Shift(
        period_id=period.id,
        shift_date=date(2026, 2, 10),
        shift_type=ShiftType.T1,
    )
    session.add(s1)
    session.commit()
    session.add(s2)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_shift_part_create(session):
    doctor = Doctor(name="Dr. Part", crm="PART01", hour_rate=100.0)
    session.add(doctor)
    session.flush()
    period = Period(year=2026, month=3, status=PeriodStatus.DRAFT)
    session.add(period)
    session.flush()
    shift = Shift(
        period_id=period.id,
        shift_date=date(2026, 3, 1),
        shift_type=ShiftType.T2,
    )
    session.add(shift)
    session.flush()
    part = ShiftPart(
        shift_id=shift.id,
        doctor_id=doctor.id,
        start_time=time(7, 0),
        end_time=time(19, 0),
    )
    session.add(part)
    session.commit()
    assert part.id is not None


# Removido: test_shift_part_time_order — afirmava que um ShiftPart das 19:00 às 07:00 deveria
# violar uma constraint de "ordem de horário". Mas isso é um plantão NOTURNO (cruza a meia-noite),
# que é válido no domínio. O teste testava um comportamento incorreto e não havia (nem deve haver)
# tal constraint. Ver spec 003 (baseline de testes).


def test_shift_extra_create(session):
    doctor = Doctor(name="Dr. Extra", crm="EXTRA01", hour_rate=100.0)
    session.add(doctor)
    session.flush()
    period = Period(year=2026, month=5, status=PeriodStatus.DRAFT)
    session.add(period)
    session.flush()
    shift = Shift(
        period_id=period.id,
        shift_date=date(2026, 5, 1),
        shift_type=ShiftType.R1,
    )
    session.add(shift)
    session.flush()
    extra = ShiftExtra(
        shift_id=shift.id,
        doctor_id=doctor.id,
        duration_minutes=480,
        justification="Cobertura de férias",
    )
    session.add(extra)
    session.commit()
    assert extra.id is not None
    assert extra.duration_hours == 8.0


def test_shift_extra_duration_positive(session):
    from sqlalchemy.exc import IntegrityError

    doctor = Doctor(name="Dr. Dur", crm="DUR01", hour_rate=100.0)
    session.add(doctor)
    session.flush()
    period = Period(year=2026, month=9, status=PeriodStatus.DRAFT)
    session.add(period)
    session.flush()
    shift = Shift(
        period_id=period.id,
        shift_date=date(2026, 9, 1),
        shift_type=ShiftType.R2,
    )
    session.add(shift)
    session.flush()
    extra = ShiftExtra(
        shift_id=shift.id,
        doctor_id=doctor.id,
        duration_minutes=0,
        justification="Teste",
    )
    session.add(extra)
    with pytest.raises(IntegrityError):
        session.commit()
    session.rollback()


def test_doctor_relationships(session):
    doctor = Doctor(name="Dr. Rel", crm="REL01", hour_rate=100.0)
    session.add(doctor)
    session.flush()
    period = Period(year=2026, month=7, status=PeriodStatus.DRAFT)
    session.add(period)
    session.flush()
    shift = Shift(
        period_id=period.id,
        shift_date=date(2026, 7, 1),
        shift_type=ShiftType.T1,
    )
    session.add(shift)
    session.flush()
    part = ShiftPart(
        shift_id=shift.id,
        doctor_id=doctor.id,
        start_time=time(7, 0),
        end_time=time(19, 0),
    )
    session.add(part)
    session.commit()
    session.refresh(doctor)
    assert len(doctor.shift_parts) > 0


def test_cascade_delete_shift(session):
    doctor = Doctor(name="Dr. Cascade", crm="CAS01", hour_rate=100.0)
    session.add(doctor)
    session.flush()
    period = Period(year=2026, month=8, status=PeriodStatus.DRAFT)
    session.add(period)
    session.flush()
    shift = Shift(
        period_id=period.id,
        shift_date=date(2026, 8, 1),
        shift_type=ShiftType.T1,
    )
    session.add(shift)
    session.flush()
    part = ShiftPart(
        shift_id=shift.id,
        doctor_id=doctor.id,
        start_time=time(7, 0),
        end_time=time(19, 0),
    )
    session.add(part)
    session.commit()
    shift_id = shift.id
    session.delete(shift)
    session.commit()
    remaining = session.query(ShiftPart).filter_by(shift_id=shift_id).count()
    assert remaining == 0
