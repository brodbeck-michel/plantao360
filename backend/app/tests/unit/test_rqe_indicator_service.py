"""Testes do RqeIndicatorService — indicador de horas por RQE (PLANTAOPA-3)."""

from datetime import date, time

import pytest

from app.domain.constants.assignment_status import AssignmentStatus
from app.domain.constants.extra_status import ExtraStatus
from app.models.doctor import Doctor
from app.models.period import Period
from app.models.shift import Shift
from app.models.shift_extra import ShiftExtra
from app.models.shift_part import ShiftPart
from app.services.rqe_indicator_service import RqeIndicatorService


@pytest.fixture
def period(db_session):
    p = Period(year=2026, month=9, status="draft")
    db_session.add(p)
    db_session.commit()
    return p


@pytest.fixture
def shift(db_session, period):
    s = Shift(
        period_id=period.id,
        shift_date=date(2026, 9, 10),
        shift_type="D",
        status="scheduled",
    )
    db_session.add(s)
    db_session.commit()
    return s


def make_doctor(
    db_session, name: str, crm: str, has_rqe: bool, active: bool = True
) -> Doctor:
    d = Doctor(name=name, crm=crm, has_rqe=has_rqe, active=active)
    db_session.add(d)
    db_session.commit()
    return d


def add_part(
    db_session, shift, doctor, minutes: int,
    status: str = AssignmentStatus.COMPLETED,
):
    part = ShiftPart(
        shift_id=shift.id,
        doctor_id=doctor.id,
        start_time=time(7, 0),
        end_time=time(19, 0),
        status=status,
        duration_minutes=minutes,
    )
    db_session.add(part)
    db_session.commit()
    return part


def add_extra(db_session, shift, doctor, minutes: int, status: str):
    extra = ShiftExtra(
        shift_id=shift.id,
        doctor_id=doctor.id,
        duration_minutes=minutes,
        justification="teste",
        status=status,
    )
    db_session.add(extra)
    db_session.commit()
    return extra


def test_percentual_e_de_horas_e_nao_de_medicos(db_session, period, shift):
    """Um médico com RQE de muitas horas pesa mais que dois sem RQE de poucas horas."""
    com_rqe = make_doctor(db_session, "Com RQE", "CRM1", has_rqe=True)
    sem_rqe_a = make_doctor(db_session, "Sem RQE A", "CRM2", has_rqe=False)
    sem_rqe_b = make_doctor(db_session, "Sem RQE B", "CRM3", has_rqe=False)

    add_part(db_session, shift, com_rqe, minutes=600)   # 10h
    add_part(db_session, shift, sem_rqe_a, minutes=180)  # 3h
    add_part(db_session, shift, sem_rqe_b, minutes=120)  # 2h

    result = RqeIndicatorService(db_session).execute(period_id=period.id)

    # 2 de 3 médicos são sem RQE (66%), mas 10h de 15h são com RQE (66,7%).
    assert result.total_hours == 15.0
    assert result.hours_with_rqe == 10.0
    assert result.hours_without_rqe == 5.0
    assert result.pct_with_rqe == 66.7
    assert result.doctors_with_rqe == 1
    assert result.doctors_without_rqe == 2


def test_extras_somente_aprovados_entram_no_total(db_session, period, shift):
    doctor = make_doctor(db_session, "Médico", "CRM1", has_rqe=True)
    add_part(db_session, shift, doctor, minutes=600)  # 10h

    add_extra(db_session, shift, doctor, minutes=60, status=ExtraStatus.APPROVED)
    add_extra(db_session, shift, doctor, minutes=120, status=ExtraStatus.PENDING)
    add_extra(db_session, shift, doctor, minutes=120, status=ExtraStatus.REJECTED)
    add_extra(db_session, shift, doctor, minutes=120, status=ExtraStatus.CANCELLED)

    result = RqeIndicatorService(db_session).execute(period_id=period.id)

    assert result.total_hours == 11.0  # 10h de plantão + 1h do extra aprovado
    assert result.doctors[0].extra_hours == 1.0


def test_plantao_cancelado_nao_conta(db_session, period, shift):
    doctor = make_doctor(db_session, "Médico", "CRM1", has_rqe=False)
    add_part(db_session, shift, doctor, minutes=600, status=AssignmentStatus.COMPLETED)
    add_part(db_session, shift, doctor, minutes=600, status=AssignmentStatus.CANCELLED)

    result = RqeIndicatorService(db_session).execute(period_id=period.id)

    assert result.total_hours == 10.0
    assert result.doctors[0].shift_count == 1


@pytest.mark.parametrize("status", [
    AssignmentStatus.PLANNED,
    AssignmentStatus.CONFIRMED,
    AssignmentStatus.STARTED,
    AssignmentStatus.COMPLETED,
])
def test_plantao_nao_cancelado_conta_em_qualquer_status(
    db_session, period, shift, status
):
    doctor = make_doctor(db_session, "Médico", "CRM1", has_rqe=True)
    add_part(db_session, shift, doctor, minutes=120, status=status)

    result = RqeIndicatorService(db_session).execute(period_id=period.id)

    assert result.total_hours == 2.0


def test_soma_das_fatias_fecha_com_o_total(db_session, period, shift):
    """Critério de aceite nº 1 — com RQE + sem RQE tem que dar o total."""
    for i in range(12):
        doctor = make_doctor(db_session, f"Médico {i}", f"CRM{i}", has_rqe=(i % 3 == 0))
        add_part(db_session, shift, doctor, minutes=37 * (i + 1))
        add_extra(db_session, shift, doctor, minutes=13, status=ExtraStatus.APPROVED)

    result = RqeIndicatorService(db_session).execute(period_id=period.id)

    assert result.hours_with_rqe + result.hours_without_rqe == result.total_hours
    assert result.doctors_total == 12  # sem truncamento por limite
    assert round(result.pct_with_rqe + result.pct_without_rqe, 1) == 100.0


def test_medico_inativo_com_horas_continua_somando(db_session, period, shift):
    """Excluí-lo faria o total divergir da soma das fatias."""
    ativo = make_doctor(db_session, "Ativo", "CRM1", has_rqe=True)
    inativo = make_doctor(db_session, "Inativo", "CRM2", has_rqe=False, active=False)
    add_part(db_session, shift, ativo, minutes=300)
    add_part(db_session, shift, inativo, minutes=300)

    result = RqeIndicatorService(db_session).execute(period_id=period.id)

    assert result.total_hours == 10.0
    assert result.doctors_total == 2
    assert result.pct_with_rqe == 50.0


def test_competencia_sem_horas_nao_divide_por_zero(db_session, period):
    result = RqeIndicatorService(db_session).execute(period_id=period.id)

    assert result.period_id == period.id
    assert result.total_hours == 0.0
    assert result.pct_with_rqe == 0.0
    assert result.pct_without_rqe == 0.0
    assert result.doctors == []


def test_competencia_inexistente_retorna_indicador_vazio(db_session):
    result = RqeIndicatorService(db_session).execute(period_id=9999)

    assert result.period_id == 0
    assert result.total_hours == 0.0
    assert result.period_name == "Nenhuma competência encontrada"


def test_resolve_competencia_por_year_month(db_session, period, shift):
    doctor = make_doctor(db_session, "Médico", "CRM1", has_rqe=True)
    add_part(db_session, shift, doctor, minutes=600)

    result = RqeIndicatorService(db_session).execute(year_month="2026-09")

    assert result.period_id == period.id
    assert result.period_name == "Setembro/2026"
    assert result.total_hours == 10.0


def test_year_month_invalido_nao_explode(db_session, period):
    result = RqeIndicatorService(db_session).execute(year_month="setembro")

    assert result.period_id == 0


def test_sem_filtro_usa_competencia_mais_recente_nao_paga(db_session, period, shift):
    antiga = Period(year=2026, month=1, status="draft")
    db_session.add(antiga)
    db_session.commit()

    result = RqeIndicatorService(db_session).execute()

    assert result.period_id == period.id  # 2026-09 é mais recente que 2026-01


def test_ranking_ordenado_por_horas_desc(db_session, period, shift):
    pouco = make_doctor(db_session, "Pouco", "CRM1", has_rqe=True)
    muito = make_doctor(db_session, "Muito", "CRM2", has_rqe=False)
    add_part(db_session, shift, pouco, minutes=60)
    add_part(db_session, shift, muito, minutes=600)

    result = RqeIndicatorService(db_session).execute(period_id=period.id)

    assert [d.name for d in result.doctors] == ["Muito", "Pouco"]
    assert result.doctors[0].total_hours == 10.0


# ============================================================
# Duração derivada de start_time/end_time
#
# AssignmentService.create não preenche duration_minutes — na prática o campo
# vem nulo. Somar a coluna direto daria 0h para todo mundo.
# ============================================================


def add_part_sem_duracao(db_session, shift, doctor, start: time, end: time):
    part = ShiftPart(
        shift_id=shift.id,
        doctor_id=doctor.id,
        start_time=start,
        end_time=end,
        status=AssignmentStatus.PLANNED,
        duration_minutes=None,
    )
    db_session.add(part)
    db_session.commit()
    return part


def test_duracao_derivada_quando_duration_minutes_e_nulo(db_session, period, shift):
    doctor = make_doctor(db_session, "Médico", "CRM1", has_rqe=True)
    add_part_sem_duracao(db_session, shift, doctor, time(7, 0), time(19, 0))

    result = RqeIndicatorService(db_session).execute(period_id=period.id)

    assert result.total_hours == 12.0
    assert result.pct_with_rqe == 100.0


def test_plantao_que_vira_o_dia_conta_as_horas_da_madrugada(db_session, period, shift):
    doctor = make_doctor(db_session, "Noturno", "CRM1", has_rqe=False)
    add_part_sem_duracao(db_session, shift, doctor, time(19, 0), time(7, 0))

    result = RqeIndicatorService(db_session).execute(period_id=period.id)

    assert result.total_hours == 12.0


def test_duration_minutes_preenchido_tem_precedencia(db_session, period, shift):
    """O campo persistido é override: se alguém preencheu, ele manda."""
    doctor = make_doctor(db_session, "Médico", "CRM1", has_rqe=True)
    add_part(db_session, shift, doctor, minutes=300)  # 5h, apesar do 7h-19h

    result = RqeIndicatorService(db_session).execute(period_id=period.id)

    assert result.total_hours == 5.0


def test_duracao_derivada_e_persistida_convivem(db_session, period, shift):
    com_rqe = make_doctor(db_session, "Com RQE", "CRM1", has_rqe=True)
    sem_rqe = make_doctor(db_session, "Sem RQE", "CRM2", has_rqe=False)
    add_part_sem_duracao(db_session, shift, com_rqe, time(7, 0), time(19, 0))  # 12h
    add_part(db_session, shift, sem_rqe, minutes=720)  # 12h

    result = RqeIndicatorService(db_session).execute(period_id=period.id)

    assert result.total_hours == 24.0
    assert result.pct_with_rqe == 50.0
