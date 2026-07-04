from datetime import date, time as time_type, timedelta

from sqlalchemy.orm import Session

from app.models.period import Period
from app.models.shift import Shift
from app.models.shift_part import ShiftPart
from app.models.doctor import Doctor
from app.domain.constants.shift_types import ShiftType
from app.domain.constants.shift_status import ShiftStatus
from app.domain.constants.competency_dates import get_competency_dates


SHIFT_TYPE_LABELS = {
    "T1": "T1 TITULAR MANHÃ",
    "T2": "T2 TITULAR TARDE",
    "T3": "T3 TITULAR NOITE",
    "R1": "R1 REFORÇO MANHÃ",
    "R2": "R2 REFORÇO TARDE",
}

SHIFT_TYPE_ORDER = ["T1", "T2", "T3", "R1", "R2"]

DAY_NAMES = ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"]

SHIFT_TIMES = {
    "T1": (time_type(7, 0), time_type(12, 59)),
    "T2": (time_type(13, 0), time_type(18, 59)),
    "T3": (time_type(19, 0), time_type(6, 59)),
    "R1": (time_type(9, 0), time_type(14, 59)),
    "R2": (time_type(15, 0), time_type(21, 0)),
}


class WorkspaceService:
    def __init__(self, db: Session):
        self.db = db

    def build_workspace(self, period_id: int) -> dict | None:
        period = self.db.query(Period).filter(Period.id == period_id).first()
        if not period:
            return None

        start_date, end_date = self._get_period_dates(period)
        shift_types = [s.value for s in ShiftType]

        existing_shifts = self.db.query(Shift).filter(
            Shift.period_id == period_id,
            Shift.shift_date >= start_date,
            Shift.shift_date <= end_date,
            Shift.status != ShiftStatus.CANCELLED,
        ).all()

        shift_map: dict[tuple[date, str], Shift] = {}
        for s in existing_shifts:
            shift_map[(s.shift_date, s.shift_type)] = s

        all_shift_ids = [s.id for s in existing_shifts]
        all_assignments = []
        if all_shift_ids:
            all_assignments = self.db.query(ShiftPart).filter(
                ShiftPart.shift_id.in_(all_shift_ids),
                ShiftPart.status.in_(["planned", "confirmed"]),
            ).all()

        assignments_by_shift: dict[int, list[ShiftPart]] = {}
        for a in all_assignments:
            assignments_by_shift.setdefault(a.shift_id, []).append(a)

        doctors = self.db.query(Doctor).filter(Doctor.active == True).all()
        doctor_map = {d.id: d for d in doctors}

        days = []
        total_assignments = 0
        current = start_date
        while current <= end_date:
            dow = DAY_NAMES[current.weekday()]
            shifts_data = {}
            for st in shift_types:
                shift = shift_map.get((current, st))
                if shift:
                    assign_list = assignments_by_shift.get(shift.id, [])
                    assignments = []
                    for a in assign_list:
                        doc = doctor_map.get(a.doctor_id)
                        assignments.append({
                            "id": a.id,
                            "shift_id": a.shift_id,
                            "shift_type": st,
                            "doctor_id": a.doctor_id,
                            "doctor_name": doc.name if doc else f"Médico #{a.doctor_id}",
                            "start_time": a.start_time.strftime("%H:%M"),
                            "end_time": a.end_time.strftime("%H:%M"),
                            "status": a.status,
                        })
                        total_assignments += 1
                    shifts_data[st] = {
                        "shift_id": shift.id,
                        "shift_type": st,
                        "assignments": assignments,
                    }
                else:
                    shifts_data[st] = {
                        "shift_id": None,
                        "shift_type": st,
                        "assignments": [],
                    }
            days.append({
                "date": current.isoformat(),
                "day_of_week": dow,
                "shifts": shifts_data,
            })
            current += timedelta(days=1)

        total_shifts = len(days) * len(shift_types)
        total_hours = sum(
            self._calc_hours(a.get("start_time", ""), a.get("end_time", ""))
            for day in days
            for shift in day["shifts"].values()
            for a in shift.get("assignments", [])
        )

        return {
            "period": {
                "id": period.id,
                "name": f"{period.month:02d}/{period.year}",
                "year": period.year,
                "month": period.month,
                "status": period.status,
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
            "days": days,
            "doctors": [
                {"id": d.id, "name": d.name, "crm": d.crm, "hour_rate": float(d.hour_rate), "specialty": d.specialty, "active": d.active}
                for d in doctors
            ],
            "summary": {
                "total_shifts": total_shifts,
                "filled_shifts": total_assignments,
                "coverage_rate": round((total_assignments / total_shifts * 100) if total_shifts > 0 else 0, 1),
                "total_doctors": len(doctors),
                "total_hours": round(total_hours, 1),
            },
        }

    def _get_period_dates(self, period: Period) -> tuple[date, date]:
        return get_competency_dates(period.year, period.month)

    def _calc_hours(self, start_str: str, end_str: str) -> float:
        try:
            parts_s = start_str.split(":")
            parts_e = end_str.split(":")
            start_minutes = int(parts_s[0]) * 60 + int(parts_s[1])
            end_minutes = int(parts_e[0]) * 60 + int(parts_e[1])
            if end_minutes <= start_minutes:
                end_minutes += 24 * 60
            return (end_minutes - start_minutes) / 60.0
        except Exception:
            return 0.0
