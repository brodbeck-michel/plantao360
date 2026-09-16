from datetime import timedelta

from app.models.period import Period
from app.models.shift import Shift
from app.domain.constants.period_status import PeriodStatus
from app.domain.constants.shift_status import ShiftStatus
from app.domain.constants.shift_types import ShiftType
from app.domain.constants.competency_dates import get_competency_dates
from app.services.workspace_service import WorkspaceService


LEGACY_TYPES = ["T1", "T2", "T3", "R1", "R2"]


def _legacy_period(db_session, status=PeriodStatus.DRAFT):
    """Periodo como os criados antes do R3 existir: sem a linha de R3."""
    period = Period(year=2026, month=3, status=status)
    db_session.add(period)
    db_session.flush()

    start_date, end_date = get_competency_dates(period.year, period.month)
    current = start_date
    while current <= end_date:
        for st in LEGACY_TYPES:
            db_session.add(Shift(
                period_id=period.id,
                shift_date=current,
                shift_type=st,
                status=ShiftStatus.DRAFT,
            ))
        current += timedelta(days=1)
    db_session.flush()
    return period, start_date, end_date


def _types_in_db(db_session, period_id):
    rows = db_session.query(Shift.shift_type).filter(Shift.period_id == period_id).distinct().all()
    return sorted(r[0] for r in rows)


def test_workspace_cria_turno_faltante_em_periodo_antigo(db_session):
    period, start_date, end_date = _legacy_period(db_session)
    assert "R3" not in _types_in_db(db_session, period.id)

    data = WorkspaceService(db_session).build_workspace(period.id)

    assert "R3" in _types_in_db(db_session, period.id)
    for day in data["days"]:
        assert day["shifts"]["R3"]["shift_id"] is not None


def test_workspace_nao_duplica_turno_existente(db_session):
    period, start_date, end_date = _legacy_period(db_session)
    service = WorkspaceService(db_session)

    service.build_workspace(period.id)
    total_after_first = db_session.query(Shift).filter(Shift.period_id == period.id).count()

    service.build_workspace(period.id)
    total_after_second = db_session.query(Shift).filter(Shift.period_id == period.id).count()

    dias = (end_date - start_date).days + 1
    assert total_after_first == dias * len(ShiftType.values())
    assert total_after_second == total_after_first


def test_workspace_nao_recria_turno_cancelado(db_session):
    period, start_date, _ = _legacy_period(db_session)
    db_session.add(Shift(
        period_id=period.id,
        shift_date=start_date,
        shift_type="R3",
        status=ShiftStatus.CANCELLED,
    ))
    db_session.flush()

    WorkspaceService(db_session).build_workspace(period.id)

    r3_no_dia = db_session.query(Shift).filter(
        Shift.period_id == period.id,
        Shift.shift_date == start_date,
        Shift.shift_type == "R3",
    ).all()
    assert len(r3_no_dia) == 1
    assert r3_no_dia[0].status == ShiftStatus.CANCELLED


def test_workspace_nao_toca_periodo_fechado(db_session):
    period, _, _ = _legacy_period(db_session, status=PeriodStatus.CLOSED)

    WorkspaceService(db_session).build_workspace(period.id)

    assert "R3" not in _types_in_db(db_session, period.id)
