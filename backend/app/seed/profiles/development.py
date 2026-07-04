"""Development profile — minimal dataset for development."""

from datetime import datetime, timedelta, date
import random

from app.seed.seed_data import (
    SHIFT_TYPE_MAP,
    generate_name,
    generate_crm,
    generate_hour_rate,
)


def generate_data() -> dict:
    """Generate minimal development dataset: 5 doctors, 1 period, 10 shifts."""
    print("Generating development dataset...")
    random.seed(42)

    doctors_data = []
    for _ in range(5):
        doctors_data.append({
            "name": generate_name(),
            "crm": generate_crm(),
            "hour_rate": generate_hour_rate(),
            "active": True,
        })

    periods_data = [{"year": 2026, "month": 1, "status": "draft"}]

    shifts_data = []
    for day in range(1, 11):
        d = date(2026, 1, day)
        st = SHIFT_TYPE_MAP["T1"]
        shifts_data.append({
            "shift_date": d,
            "shift_type": "T1",
            "status": "scheduled",
            "period_month": 1,
            "period_year": 2026,
            "scheduled_start": datetime.combine(d, st["start"]),
            "scheduled_end": datetime.combine(
                d + timedelta(days=1 if st["end"] <= st["start"] else 0),
                st["end"],
            ),
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
        "extras": [],
    }
