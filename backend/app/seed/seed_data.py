"""
Seed Data - Plantao 360

Populates the database with realistic demo data.

Usage:
    python -m app.seed.seed_data --dataset demo
    python -m app.seed.seed_data --dataset edge_cases
    python -m app.seed.seed_data --dataset showcase
    python -m app.seed.seed_data --all
    python -m app.seed.seed_data --dataset demo --clear
"""

import argparse
import random
from datetime import datetime, time, date, timedelta
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.base import SessionLocal
from app.models.doctor import Doctor
from app.models.period import Period
from app.models.shift import Shift
from app.models.shift_part import ShiftPart
from app.models.shift_extra import ShiftExtra
from app.models.payroll import Payroll

# ============================================================
# Constants
# ============================================================

SPECIALTIES = [
    "Clinica Medica", "Cardiologia", "Pediatria", "Ortopedia",
    "Neurologia", "Dermatologia", "Oftalmologia", "Otorrinolaringologia",
    "Urologia", "Ginecologia", "Obstetricia", "Anestesiologia",
    "Radiologia", "Patologia", "Infectologia",
]

DOCTOR_TYPES = ["plantonista", "diarista", "freelancer"]

SHIFT_TYPE_MAP = {
    "T1": {"start": time(7, 0), "end": time(19, 0), "hours": 720},
    "T2": {"start": time(19, 0), "end": time(7, 0), "hours": 720},
    "T3": {"start": time(7, 0), "end": time(7, 0), "hours": 1440},
    "R1": {"start": time(7, 0), "end": time(13, 0), "hours": 360},
    "R2": {"start": time(13, 0), "end": time(19, 0), "hours": 360},
}

NAMES_FIRST = [
    "Ana", "Maria", "Joao", "Jose", "Pedro", "Paulo", "Lucas", "Marcos",
    "Rafael", "Carlos", "Fernanda", "Juliana", "Camila", "Amanda", "Mariana",
    "Bruno", "Thiago", "Gabriel", "Felipe", "Andre", "Patricia", "Renata",
    "Adriana", "Claudia", "Roberto", "Fernando", "Ricardo", "Eduardo",
    "Sergio", "Alexandre", "Gustavo", "Leandro", "Diego", "Matheus",
]

NAMES_LAST = [
    "Silva", "Santos", "Oliveira", "Souza", "Ferreira", "Costa", "Rodrigues",
    "Almeida", "Nascimento", "Lima", "Araujo", "Barbosa", "Ribeiro", "Carvalho",
    "Martins", "Rocha", "Correia", "Gomes", "Mendes", "Moreira",
]


# ============================================================
# Helpers
# ============================================================

def generate_crm() -> str:
    return f"{random.randint(10000, 99999)}/ES"

def generate_name() -> str:
    return f"{random.choice(NAMES_FIRST)} {random.choice(NAMES_LAST)}"

def generate_hour_rate() -> float:
    return round(random.uniform(80, 250), 2)

def generate_phone() -> str:
    return f"(27) 9{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

def generate_email(name: str) -> str:
    slug = name.lower().replace(" ", ".").replace("'", "")
    return f"{slug}@email.com"

def days_in_month(year: int, month: int) -> int:
    if month == 12:
        return (date(year + 1, 1, 1) - date(year, month, 1)).days
    return (date(year, month + 1, 1) - date(year, month, 1)).days


# ============================================================
# Demo Dataset
# ============================================================

def generate_demo_data() -> dict:
    print("Generating demo dataset...")
    random.seed(42)

    doctors_data = []
    for i in range(35):
        name = generate_name()
        doctors_data.append({
            "name": name,
            "crm": generate_crm(),
            "hour_rate": generate_hour_rate(),
            "specialty": random.choice(SPECIALTIES),
            "phone": generate_phone(),
            "email": generate_email(name),
            "doctor_type": random.choice(DOCTOR_TYPES),
            "active": random.random() > 0.1,
        })

    periods_data = []
    for month in range(1, 7):
        status = "paid" if month < 4 else "closed" if month == 4 else "draft"
        periods_data.append({"year": 2026, "month": month, "status": status})

    shifts_data = []
    extras_data = []
    for period in periods_data:
        month = period["month"]
        year = period["year"]
        num_days = days_in_month(year, month)
        for day in range(1, num_days + 1):
            d = date(year, month, day)
            num_shifts = random.randint(1, 2)
            available_types = ["T1", "T2", "T3"]
            for _ in range(num_shifts):
                shift_type = random.choice(available_types)
                st = SHIFT_TYPE_MAP[shift_type]
                shift_status = "completed" if month < 5 else random.choice(["scheduled", "in_progress"])
                shifts_data.append({
                    "shift_date": d,
                    "shift_type": shift_type,
                    "status": shift_status,
                    "period_month": month,
                    "period_year": year,
                    "scheduled_start": datetime.combine(d, st["start"]),
                    "scheduled_end": datetime.combine(d + timedelta(days=1 if st["end"] <= st["start"] else 0), st["end"]),
                    "total_duration_minutes": st["hours"],
                    "doctor_count": 1,
                })

    print(f"  - {len(doctors_data)} doctors")
    print(f"  - {len(periods_data)} periods")
    print(f"  - {len(shifts_data)} shifts")

    return {
        "doctors": doctors_data,
        "periods": periods_data,
        "shifts": shifts_data,
        "extras": extras_data,
    }


# ============================================================
# Edge Cases Dataset
# ============================================================

def generate_edge_cases_data() -> dict:
    print("Generating edge cases dataset...")
    random.seed(99)

    doctors_data = [
        {"name": "Dr. Jose da Silva", "crm": "00001/ES", "hour_rate": 80.00, "specialty": "Clinica Medica", "phone": "(27) 99999-0001", "email": "jose.silva@email.com", "doctor_type": "plantonista", "active": True},
        {"name": "Dr. Joao Paulo Teste", "crm": "99999/ES", "hour_rate": 250.00, "specialty": "Cardiologia", "phone": "(27) 99999-9999", "email": "joao.teste@email.com", "doctor_type": "plantonista", "active": True},
        {"name": "Dra. Ana Maria Limite", "crm": "12345/ES", "hour_rate": 150.00, "specialty": "Pediatria", "phone": None, "email": None, "doctor_type": "diarista", "active": False},
    ]

    periods_data = [{"year": 2026, "month": 1, "status": "draft"}]

    shifts_data = [
        {
            "shift_date": date(2026, 1, 15), "shift_type": "T1", "status": "scheduled",
            "period_month": 1, "period_year": 2026,
            "scheduled_start": datetime(2026, 1, 15, 7, 0),
            "scheduled_end": datetime(2026, 1, 15, 19, 0),
            "total_duration_minutes": 720, "doctor_count": 1,
        },
        {
            "shift_date": date(2026, 1, 16), "shift_type": "T1", "status": "scheduled",
            "period_month": 1, "period_year": 2026,
            "scheduled_start": datetime(2026, 1, 16, 7, 0),
            "scheduled_end": datetime(2026, 1, 16, 19, 0),
            "total_duration_minutes": 720, "doctor_count": 1,
        },
        {
            "shift_date": date(2026, 1, 16), "shift_type": "T2", "status": "scheduled",
            "period_month": 1, "period_year": 2026,
            "scheduled_start": datetime(2026, 1, 16, 19, 0),
            "scheduled_end": datetime(2026, 1, 17, 7, 0),
            "total_duration_minutes": 720, "doctor_count": 1,
        },
    ]

    print(f"  - {len(doctors_data)} doctors")
    print(f"  - {len(periods_data)} periods")
    print(f"  - {len(shifts_data)} shifts")

    return {"doctors": doctors_data, "periods": periods_data, "shifts": shifts_data, "extras": []}


# ============================================================
# Showcase Dataset
# ============================================================

def generate_showcase_data() -> dict:
    print("Generating showcase dataset...")
    random.seed(123)

    doctors_data = [
        {"name": "Dr. Pedro Showcase", "crm": "11111/ES", "hour_rate": 150.00, "specialty": "Clinica Medica", "phone": "(27) 99999-1111", "email": "pedro.showcase@email.com", "doctor_type": "plantonista", "active": True},
        {"name": "Dra. Maria Demo", "crm": "22222/ES", "hour_rate": 180.00, "specialty": "Cardiologia", "phone": "(27) 99999-2222", "email": "maria.demo@email.com", "doctor_type": "plantonista", "active": True},
        {"name": "Dr. Joao Example", "crm": "33333/ES", "hour_rate": 200.00, "specialty": "Pediatria", "phone": "(27) 99999-3333", "email": "joao.example@email.com", "doctor_type": "freelancer", "active": True},
    ]

    periods_data = [{"year": 2026, "month": 6, "status": "draft"}]

    shifts_data = [
        {
            "shift_date": date(2026, 6, 15), "shift_type": "T1", "status": "scheduled",
            "period_month": 6, "period_year": 2026,
            "scheduled_start": datetime(2026, 6, 15, 7, 0),
            "scheduled_end": datetime(2026, 6, 15, 19, 0),
            "total_duration_minutes": 720, "doctor_count": 1,
        },
        {
            "shift_date": date(2026, 6, 15), "shift_type": "T2", "status": "scheduled",
            "period_month": 6, "period_year": 2026,
            "scheduled_start": datetime(2026, 6, 15, 19, 0),
            "scheduled_end": datetime(2026, 6, 16, 7, 0),
            "total_duration_minutes": 720, "doctor_count": 1,
        },
        {
            "shift_date": date(2026, 6, 16), "shift_type": "T1", "status": "scheduled",
            "period_month": 6, "period_year": 2026,
            "scheduled_start": datetime(2026, 6, 16, 7, 0),
            "scheduled_end": datetime(2026, 6, 16, 19, 0),
            "total_duration_minutes": 720, "doctor_count": 1,
        },
    ]

    print(f"  - {len(doctors_data)} doctors")
    print(f"  - {len(periods_data)} periods")
    print(f"  - {len(shifts_data)} shifts")

    return {"doctors": doctors_data, "periods": periods_data, "shifts": shifts_data, "extras": []}


# ============================================================
# Database Loader
# ============================================================

def clear_database(session: Session):
    """Remove all data from tables."""
    print("Clearing database...")
    session.execute(ShiftExtra.__table__.delete())
    session.execute(ShiftPart.__table__.delete())
    session.execute(Shift.__table__.delete())
    session.execute(Period.__table__.delete())
    session.execute(Doctor.__table__.delete())
    session.commit()
    print("  Database cleared.")


def load_doctors(session: Session, doctors_data: List[dict]) -> List[Doctor]:
    """Insert doctors into database."""
    doctors = []
    for d in doctors_data:
        doctor = Doctor(
            name=d["name"],
            crm=d["crm"],
            hour_rate=d["hour_rate"],
            specialty=d.get("specialty", "Clinica Medica"),
            phone=d.get("phone"),
            email=d.get("email"),
            doctor_type=d.get("doctor_type", "plantonista"),
            active=d.get("active", True),
        )
        session.add(doctor)
        doctors.append(doctor)
    session.flush()
    print(f"  Loaded {len(doctors)} doctors")
    return doctors


def load_periods(session: Session, periods_data: List[dict]) -> List[Period]:
    """Insert periods into database."""
    periods = []
    for p in periods_data:
        period = Period(year=p["year"], month=p["month"], status=p["status"])
        session.add(period)
        periods.append(period)
    session.flush()
    print(f"  Loaded {len(periods)} periods")
    return periods


def load_shifts(session: Session, shifts_data: List[dict], periods: List[Period], doctors: List[Doctor]) -> List[Shift]:
    """Insert shifts and assign doctors via shift_parts."""
    period_map = {(p.year, p.month): p for p in periods}
    active_doctors = [d for d in doctors if d.active]
    shifts = []
    seen_keys = set()
    for s in shifts_data:
        period = period_map.get((s["period_year"], s["period_month"]))
        if not period:
            continue
        key = (s["shift_date"], s["shift_type"])
        if key in seen_keys:
            continue
        seen_keys.add(key)
        shift = Shift(
            period_id=period.id,
            shift_date=s["shift_date"],
            shift_type=s["shift_type"],
            status=s["status"],
            scheduled_start=s.get("scheduled_start"),
            scheduled_end=s.get("scheduled_end"),
            total_duration_minutes=s.get("total_duration_minutes"),
            doctor_count=s.get("doctor_count", 1),
        )
        session.add(shift)
        session.flush()

        doctor = random.choice(active_doctors) if active_doctors else random.choice(doctors)
        st = SHIFT_TYPE_MAP.get(s["shift_type"], SHIFT_TYPE_MAP["T1"])
        start_t = st["start"]
        end_t = st["end"]
        if start_t == end_t:
            end_t = time(23, 59)
        part = ShiftPart(
            shift_id=shift.id,
            doctor_id=doctor.id,
            start_time=start_t,
            end_time=end_t,
            status="completed" if s["status"] == "completed" else "planned",
            duration_minutes=st["hours"],
        )
        session.add(part)
        shifts.append(shift)
    session.flush()
    print(f"  Loaded {len(shifts)} shifts with assignments")
    return shifts


def load_extras(session: Session, extras_data: List[dict], shifts: List[Shift], doctors: List[Doctor]):
    """Insert shift extras."""
    extras = []
    for e in extras_data:
        extra = ShiftExtra(
            shift_id=e["shift_id"],
            doctor_id=e["doctor_id"],
            duration_minutes=e["duration_minutes"],
            justification=e["justification"],
            status=e.get("status", "pending"),
        )
        session.add(extra)
        extras.append(extra)
    session.flush()
    print(f"  Loaded {len(extras)} extras")
    return extras


def populate_database(data: dict, clear: bool = False):
    """Load seed data into the database."""
    print("\nPopulating database...")
    session = SessionLocal()
    try:
        if clear:
            clear_database(session)

        doctors = load_doctors(session, data["doctors"])
        periods = load_periods(session, data["periods"])
        load_shifts(session, data["shifts"], periods, doctors)
        if data.get("extras"):
            load_extras(session, data["extras"], [], doctors)

        session.commit()
        print("\nDatabase populated successfully!")
    except Exception as e:
        session.rollback()
        print(f"\nError populating database: {e}")
        raise
    finally:
        session.close()


# ============================================================
# Main
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Plantao 360 Seed Data")
    parser.add_argument("--dataset", choices=["demo", "edge_cases", "showcase"], help="Dataset to load")
    parser.add_argument("--all", action="store_true", help="Load all datasets")
    parser.add_argument("--clear", action="store_true", help="Clear database before loading")
    args = parser.parse_args()

    if not args.dataset and not args.all:
        parser.print_help()
        return

    if args.all or args.dataset == "demo":
        data = generate_demo_data()
        populate_database(data, clear=args.clear)

    if args.all or args.dataset == "edge_cases":
        data = generate_edge_cases_data()
        populate_database(data, clear=args.clear)

    if args.all or args.dataset == "showcase":
        data = generate_showcase_data()
        populate_database(data, clear=args.clear)

    print("\nDone!")


if __name__ == "__main__":
    main()
