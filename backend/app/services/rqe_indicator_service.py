"""RqeIndicatorService — Indicador de horas de plantão cobertas por médicos com RQE.

Responde a pergunta de gestão: do total de horas realizadas numa competência,
quanto por cento foi coberto por médicos com RQE.

Não confundir com `rqe_stats` do DashboardService, que conta **médicos** (cabeças).
Aqui a métrica é ponderada por **hora**.

Regras (PLANTAOPA-3):
- Recorte: competência (mês cheio), via period_id ou year_month.
- Horas = ShiftPart (exceto `cancelled`) + ShiftExtra (apenas `approved`).
- RQE: fotografia atual de `Doctor.has_rqe`, sem historização.
- Base completa da competência, sem truncamento — o total precisa fechar.
"""

from dataclasses import dataclass, field
from datetime import time

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.domain.constants.assignment_status import AssignmentStatus
from app.domain.constants.extra_status import ExtraStatus
from app.domain.constants.period_status import PeriodStatus
from app.models.doctor import Doctor
from app.models.period import Period
from app.models.shift import Shift
from app.models.shift_extra import ShiftExtra
from app.models.shift_part import ShiftPart

logger = get_logger("service.rqe_indicator")

MONTH_NAMES = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro",
}


def part_duration_minutes(
    start_time: time | None,
    end_time: time | None,
    duration_minutes: int | None,
) -> int:
    """Duração de uma parte de plantão, em minutos.

    `ShiftPart.duration_minutes` é nullable e o fluxo de atribuição
    (`AssignmentService.create`) não o preenche — na prática ele vem nulo.
    Por isso a duração é derivada de `start_time`/`end_time`, com o campo
    persistido valendo como override quando existir.

    Plantão que vira o dia (fim <= início) conta as 24h de volta, mesma
    convenção usada na checagem de sobreposição do AssignmentService.
    """
    if duration_minutes is not None:
        return duration_minutes
    if start_time is None or end_time is None:
        return 0
    start = start_time.hour * 60 + start_time.minute
    end = end_time.hour * 60 + end_time.minute
    if end <= start:
        end += 24 * 60
    return end - start


@dataclass(frozen=True)
class RqeDoctorHours:
    """Horas de um médico na competência, com a marca de RQE."""
    doctor_id: int
    name: str
    crm: str
    has_rqe: bool
    total_hours: float
    shift_hours: float
    extra_hours: float
    shift_count: int

    def to_dict(self) -> dict:
        return {
            "doctor_id": self.doctor_id,
            "name": self.name,
            "crm": self.crm,
            "has_rqe": self.has_rqe,
            "total_hours": self.total_hours,
            "shift_hours": self.shift_hours,
            "extra_hours": self.extra_hours,
            "shift_count": self.shift_count,
        }


@dataclass(frozen=True)
class RqeHoursIndicator:
    """Indicador consolidado de horas por RQE numa competência."""
    period_id: int = 0
    year: int = 0
    month: int = 0
    period_name: str = ""
    period_status: str = ""
    # Intervalo real coberto pelos plantões da competência. O modelo Period
    # guarda só ano/mês, mas os plantões podem atravessar o mês (a virada do
    # dia 26 do fechamento, por exemplo) — então o recorte vem dos dados.
    start_date: str = ""
    end_date: str = ""

    total_hours: float = 0.0
    hours_with_rqe: float = 0.0
    hours_without_rqe: float = 0.0
    pct_with_rqe: float = 0.0
    pct_without_rqe: float = 0.0

    doctors_total: int = 0
    doctors_with_rqe: int = 0
    doctors_without_rqe: int = 0

    doctors: list[RqeDoctorHours] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "period_id": self.period_id,
            "year": self.year,
            "month": self.month,
            "period_name": self.period_name,
            "period_status": self.period_status,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "total_hours": self.total_hours,
            "hours_with_rqe": self.hours_with_rqe,
            "hours_without_rqe": self.hours_without_rqe,
            "pct_with_rqe": self.pct_with_rqe,
            "pct_without_rqe": self.pct_without_rqe,
            "doctors_total": self.doctors_total,
            "doctors_with_rqe": self.doctors_with_rqe,
            "doctors_without_rqe": self.doctors_without_rqe,
            "doctors": [d.to_dict() for d in self.doctors],
        }


class RqeIndicatorService:
    """Consolida horas de plantão por RQE para uma competência."""

    def __init__(self, session: Session):
        self._session = session

    def execute(
        self,
        period_id: int | None = None,
        year_month: str | None = None,
    ) -> RqeHoursIndicator:
        period = self._resolve_period(period_id, year_month)
        if period is None:
            logger.info(
                "rqe_indicator.no_period",
                extra={"period_id": period_id, "year_month": year_month},
            )
            return RqeHoursIndicator(period_name="Nenhuma competência encontrada")

        doctors = self._build_doctor_hours(period.id)
        start_date, end_date = self._period_date_range(period.id)

        hours_with_rqe = sum(d.total_hours for d in doctors if d.has_rqe)
        hours_without_rqe = sum(d.total_hours for d in doctors if not d.has_rqe)
        total_hours = hours_with_rqe + hours_without_rqe
        # Competência sem horas lançadas: percentuais ficam em zero,
        # sem divisão por zero.
        pct_with_rqe = (
            (hours_with_rqe / total_hours * 100) if total_hours > 0 else 0.0
        )

        return RqeHoursIndicator(
            period_id=period.id,
            year=period.year,
            month=period.month,
            period_name=f"{MONTH_NAMES.get(period.month, '')}/{period.year}",
            period_status=period.status,
            start_date=start_date,
            end_date=end_date,
            total_hours=round(total_hours, 2),
            hours_with_rqe=round(hours_with_rqe, 2),
            hours_without_rqe=round(hours_without_rqe, 2),
            pct_with_rqe=round(pct_with_rqe, 1),
            pct_without_rqe=(
                round(100.0 - pct_with_rqe, 1) if total_hours > 0 else 0.0
            ),
            doctors_total=len(doctors),
            doctors_with_rqe=sum(1 for d in doctors if d.has_rqe),
            doctors_without_rqe=sum(1 for d in doctors if not d.has_rqe),
            doctors=doctors,
        )

    def _resolve_period(
        self, period_id: int | None, year_month: str | None
    ) -> Period | None:
        if period_id:
            return self._session.query(Period).filter(Period.id == period_id).first()
        if year_month:
            parts = year_month.split("-")
            if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                return (
                    self._session.query(Period)
                    .filter(Period.year == int(parts[0]), Period.month == int(parts[1]))
                    .first()
                )
            return None
        return (
            self._session.query(Period)
            .filter(Period.status != PeriodStatus.PAID)
            .order_by(Period.year.desc(), Period.month.desc())
            .first()
        )

    def _period_date_range(self, period_id: int) -> tuple[str, str]:
        """Primeiro e último dia com plantão na competência, em ISO.

        Sai dos próprios plantões porque `Period` só tem ano/mês: uma
        competência pode atravessar o mês (26/08 a 25/09, por exemplo).
        """
        row = (
            self._session.query(
                func.min(Shift.shift_date),
                func.max(Shift.shift_date),
            )
            .filter(Shift.period_id == period_id)
            .first()
        )
        if not row or row[0] is None:
            return "", ""
        return str(row[0]), str(row[1])

    def _build_doctor_hours(self, period_id: int) -> list[RqeDoctorHours]:
        """Horas por médico na competência — base completa, sem limite.

        Médico inativo ou com soft delete que tenha horas lançadas continua somando:
        excluí-lo faria o total divergir da soma das duas fatias.
        """
        part_rows = (
            self._session.query(
                ShiftPart.doctor_id,
                ShiftPart.start_time,
                ShiftPart.end_time,
                ShiftPart.duration_minutes,
            )
            .join(Shift, Shift.id == ShiftPart.shift_id)
            .filter(
                Shift.period_id == period_id,
                ShiftPart.status != AssignmentStatus.CANCELLED,
            )
            .all()
        )

        shift_minutes: dict[int, tuple[int, int]] = {}
        for doctor_id, start_time, end_time, duration in part_rows:
            minutes, count = shift_minutes.get(doctor_id, (0, 0))
            shift_minutes[doctor_id] = (
                minutes + part_duration_minutes(start_time, end_time, duration),
                count + 1,
            )

        extra_rows = (
            self._session.query(
                ShiftExtra.doctor_id,
                func.sum(ShiftExtra.duration_minutes),
            )
            .join(Shift, Shift.id == ShiftExtra.shift_id)
            .filter(
                Shift.period_id == period_id,
                ShiftExtra.status == ExtraStatus.APPROVED,
            )
            .group_by(ShiftExtra.doctor_id)
            .all()
        )
        extra_minutes = {doctor_id: (minutes or 0) for doctor_id, minutes in extra_rows}

        doctor_ids = set(shift_minutes) | set(extra_minutes)
        if not doctor_ids:
            return []

        doctors = self._session.query(Doctor).filter(Doctor.id.in_(doctor_ids)).all()

        entries = []
        for doctor in doctors:
            minutes, shift_count = shift_minutes.get(doctor.id, (0, 0))
            extra_min = extra_minutes.get(doctor.id, 0)
            entries.append(RqeDoctorHours(
                doctor_id=doctor.id,
                name=doctor.name,
                crm=doctor.crm,
                has_rqe=doctor.has_rqe,
                total_hours=round((minutes + extra_min) / 60.0, 2),
                shift_hours=round(minutes / 60.0, 2),
                extra_hours=round(extra_min / 60.0, 2),
                shift_count=shift_count,
            ))

        entries.sort(key=lambda e: e.total_hours, reverse=True)
        return entries
