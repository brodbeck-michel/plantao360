"""
Import Backup Data to Plantao360

Imports data from the legacy JSON backup format to the new database.

Usage:
    python scripts/import_backup.py <path_to_backup.json>
    python scripts/import_backup.py <path_to_backup.json> --clear
"""

import json
import argparse
from datetime import datetime, time, date, timedelta
from typing import Dict, List, Set, Optional
from pathlib import Path

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database.base import SessionLocal
from app.models.doctor import Doctor
from app.models.period import Period
from app.models.shift import Shift
from app.models.shift_part import ShiftPart
from app.models.shift_extra import ShiftExtra


# ============================================================
# Constants
# ============================================================

SHIFT_TYPE_MAP = {
    "T1": {"start": time(7, 0), "end": time(19, 0), "hours": 720},
    "T2": {"start": time(19, 0), "end": time(7, 0), "hours": 720},
    "T3": {"start": time(7, 0), "end": time(7, 0), "hours": 1440},
    "R1": {"start": time(7, 0), "end": time(13, 0), "hours": 360},
    "R2": {"start": time(13, 0), "end": time(19, 0), "hours": 360},
}

MONTHS_MAP = {
    "2026-03": (2026, 3),
    "2026-04": (2026, 4),
    "2026-05": (2026, 5),
    "2026-06": (2026, 6),
    "2026-07": (2026, 7),
    "2026-08": (2026, 8),
}


# ============================================================
# Helpers
# ============================================================

def parse_admission_date(admission_str: str) -> Optional[date]:
    """Parse admission date from format MM/YYYY."""
    try:
        if not admission_str or admission_str == "NAO":
            return None
        parts = admission_str.strip().split("/")
        if len(parts) == 2:
            month, year = int(parts[0]), int(parts[1])
            return date(year, month, 1)
    except (ValueError, IndexError):
        pass
    return None


def parse_rqe(rqe_str: str) -> bool:
    """Parse RQE field."""
    return rqe_str.upper() == "SIM" if rqe_str else False


def time_str_to_time(time_str: str) -> time:
    """Parse time string HH:MM to time object."""
    parts = time_str.split(":")
    return time(int(parts[0]), int(parts[1]))


def calculate_hours(start_time: time, end_time: time, start_date: date, end_date: date) -> float:
    """Calculate hours between start and end times, accounting for overnight shifts."""
    start_dt = datetime.combine(start_date, start_time)
    end_dt = datetime.combine(end_date, end_time)

    if end_dt < start_dt:
        end_dt += timedelta(days=1)

    delta = end_dt - start_dt
    return delta.total_seconds() / 3600


# ============================================================
# Data Parsing
# ============================================================

def load_backup_json(file_path: str) -> dict:
    """Load backup JSON file."""
    print(f"Loading backup file: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def parse_doctors_from_backup(backup_data: dict) -> List[dict]:
    """Parse doctor data from backup."""
    doctors = []
    doctor_vlh = backup_data.get("data", {}).get("doctor_vlh", {})
    doctor_meta = backup_data.get("data", {}).get("doctor_meta", {})

    for doctor_name in doctor_vlh.keys():
        meta = doctor_meta.get(doctor_name, {})

        # Generate CRM from name (hash-based for uniqueness)
        name_hash = hash(doctor_name) % 90000 + 10000
        crm = f"{name_hash}/ES"

        doctors.append({
            "name": doctor_name,
            "crm": crm,
            "has_rqe": parse_rqe(meta.get("rqe", "NAO")),
            "career_start_date": parse_admission_date(meta.get("admissao")),
            "specialty": "Clinica Medica",  # Default specialty
            "phone": None,
            "email": None,
            "doctor_type": "plantonista",
            "active": True,
        })

    return doctors


def parse_shifts_from_backup(backup_data: dict) -> tuple[List[dict], List[dict], List[dict]]:
    """Parse shifts, shift_parts, and extras from backup."""
    shifts_data = []
    shift_parts_data = []
    extras_data = []

    data = backup_data.get("data", {})
    doctor_dict = {d["name"]: d for d in parse_doctors_from_backup(backup_data)}

    # Process each month's shifts
    for month_key, shifts_by_date in data.items():
        if not month_key.startswith("shifts_"):
            continue

        year_month_parts = month_key.split("_")[1]  # "2026-03" from "shifts_2026-03"
        try:
            year, month = int(year_month_parts.split("-")[0]), int(year_month_parts.split("-")[1])
        except (ValueError, IndexError):
            continue

        for date_str, shift_details in shifts_by_date.items():
            try:
                shift_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                continue

            # Process each shift type for this date
            for shift_type in ["T1", "T2", "T3", "R1", "R2"]:
                if shift_type not in shift_details:
                    continue

                shift_assignment = shift_details[shift_type]

                # Create shift record
                shift_key = (shift_date, shift_type, year, month)
                shift_record = {
                    "shift_date": shift_date,
                    "shift_type": shift_type,
                    "status": "completed",
                    "period_year": year,
                    "period_month": month,
                    "shift_key": shift_key,
                }

                st_config = SHIFT_TYPE_MAP.get(shift_type, SHIFT_TYPE_MAP["T1"])
                shift_record["scheduled_start"] = datetime.combine(shift_date, st_config["start"])

                # Handle overnight shifts
                if st_config["end"] <= st_config["start"]:
                    shift_record["scheduled_end"] = datetime.combine(
                        shift_date + timedelta(days=1), st_config["end"]
                    )
                else:
                    shift_record["scheduled_end"] = datetime.combine(shift_date, st_config["end"])

                shift_record["total_duration_minutes"] = st_config["hours"]
                shifts_data.append(shift_record)

                # Parse assignment (simple or split)
                if isinstance(shift_assignment, dict) and shift_assignment.get("type") == "split":
                    # Split assignment
                    for part in shift_assignment.get("parts", []):
                        doctor_name = part.get("doc")
                        if doctor_name in doctor_dict:
                            start_time = time_str_to_time(part.get("start", "07:00"))
                            end_time = time_str_to_time(part.get("end", "19:00"))
                            hours = part.get("hours", calculate_hours(start_time, end_time, shift_date, shift_date))

                            shift_parts_data.append({
                                "shift_key": shift_key,
                                "doctor_name": doctor_name,
                                "start_time": start_time,
                                "end_time": end_time,
                                "duration_minutes": int(hours * 60),
                            })
                else:
                    # Simple assignment
                    doctor_name = shift_assignment
                    if doctor_name in doctor_dict:
                        st_config = SHIFT_TYPE_MAP.get(shift_type, SHIFT_TYPE_MAP["T1"])
                        shift_parts_data.append({
                            "shift_key": shift_key,
                            "doctor_name": doctor_name,
                            "start_time": st_config["start"],
                            "end_time": st_config["end"],
                            "duration_minutes": st_config["hours"],
                        })

            # Process extras
            if "_extras" in shift_details:
                for extra in shift_details["_extras"]:
                    doctor_name = extra.get("doc")
                    if doctor_name in doctor_dict:
                        start_time = time_str_to_time(extra.get("start", "21:00"))
                        end_time = time_str_to_time(extra.get("end", "23:00"))
                        hours = extra.get("hours", calculate_hours(start_time, end_time, shift_date, shift_date))
                        obs = extra.get("obs", "")

                        # Find matching shift for this extra
                        for shift_type in ["T1", "T2", "T3", "R1", "R2"]:
                            shift_key = (shift_date, shift_type, year, month)
                            extras_data.append({
                                "shift_key": shift_key,
                                "doctor_name": doctor_name,
                                "duration_minutes": int(hours * 60),
                                "justification": obs or f"Extra hours on {shift_type}",
                            })

    return shifts_data, shift_parts_data, extras_data


# ============================================================
# Database Loading
# ============================================================

def clear_database(session: Session):
    """Remove all data from tables."""
    print("Clearing database...")
    from sqlalchemy import inspect as sa_inspect

    inspector = sa_inspect(session.bind)
    existing_tables = set(inspector.get_table_names())

    tables_to_clear = [
        ShiftExtra,
        ShiftPart,
        Shift,
        Period,
        Doctor,
    ]

    for model in tables_to_clear:
        table_name = model.__tablename__
        if table_name in existing_tables:
            try:
                session.execute(model.__table__.delete())
                print(f"  Cleared table: {table_name}")
            except Exception as e:
                print(f"  Warning: could not clear table {table_name}: {e}")
                session.rollback()

    session.commit()
    print("  Database cleared.")


def load_doctors(session: Session, doctors_data: List[dict]) -> Dict[str, Doctor]:
    """Insert doctors into database."""
    doctor_map = {}

    for d in doctors_data:
        # Check if doctor already exists
        existing = session.query(Doctor).filter_by(crm=d["crm"]).first()
        if existing:
            doctor_map[d["name"]] = existing
            continue

        doctor = Doctor(
            name=d["name"],
            crm=d["crm"],
            has_rqe=d.get("has_rqe", False),
            career_start_date=d.get("career_start_date"),
            specialty=d.get("specialty", "Clinica Medica"),
            phone=d.get("phone"),
            email=d.get("email"),
            doctor_type=d.get("doctor_type", "plantonista"),
            active=d.get("active", True),
        )
        session.add(doctor)
        doctor_map[d["name"]] = doctor

    session.flush()
    print(f"  Loaded {len(doctor_map)} doctors")
    return doctor_map


def load_periods(session: Session, periods_set: Set[tuple]) -> Dict[tuple, Period]:
    """Insert periods into database."""
    period_map = {}

    for year, month in periods_set:
        existing = session.query(Period).filter_by(year=year, month=month).first()
        if existing:
            period_map[(year, month)] = existing
            continue

        period = Period(year=year, month=month, status="draft")
        session.add(period)
        period_map[(year, month)] = period

    session.flush()
    print(f"  Loaded {len(period_map)} periods")
    return period_map


def load_shifts(
    session: Session,
    shifts_data: List[dict],
    shift_parts_data: List[dict],
    periods: Dict[tuple, Period],
    doctors: Dict[str, Doctor],
) -> Dict[tuple, Shift]:
    """Insert shifts and shift_parts."""
    shift_map = {}
    shift_key_to_id = {}

    # Load shifts first
    for s in shifts_data:
        period_key = (s["period_year"], s["period_month"])
        period = periods.get(period_key)
        if not period:
            continue

        shift_key = s["shift_key"]
        if shift_key in shift_key_to_id:
            continue

        shift = Shift(
            period_id=period.id,
            shift_date=s["shift_date"],
            shift_type=s["shift_type"],
            status=s["status"],
            scheduled_start=s.get("scheduled_start"),
            scheduled_end=s.get("scheduled_end"),
            total_duration_minutes=s.get("total_duration_minutes"),
            doctor_count=1,
        )
        session.add(shift)
        session.flush()
        shift_key_to_id[shift_key] = shift.id
        shift_map[shift_key] = shift

    # Load shift_parts
    for sp in shift_parts_data:
        shift_key = sp["shift_key"]
        if shift_key not in shift_key_to_id:
            continue

        doctor_name = sp["doctor_name"]
        if doctor_name not in doctors:
            continue

        doctor = doctors[doctor_name]
        shift = shift_map[shift_key]

        part = ShiftPart(
            shift_id=shift.id,
            doctor_id=doctor.id,
            start_time=sp["start_time"],
            end_time=sp["end_time"],
            status="completed",
            duration_minutes=sp["duration_minutes"],
        )
        session.add(part)

    session.flush()
    print(f"  Loaded {len(shift_map)} shifts with {len(shift_parts_data)} assignments")
    return shift_map


def load_extras(
    session: Session,
    extras_data: List[dict],
    shifts: Dict[tuple, Shift],
    doctors: Dict[str, Doctor],
):
    """Insert shift extras."""
    extras_count = 0

    for e in extras_data:
        shift_key = e["shift_key"]
        if shift_key not in shifts:
            continue

        doctor_name = e["doctor_name"]
        if doctor_name not in doctors:
            continue

        shift = shifts[shift_key]
        doctor = doctors[doctor_name]

        extra = ShiftExtra(
            shift_id=shift.id,
            doctor_id=doctor.id,
            duration_minutes=e["duration_minutes"],
            justification=e["justification"],
            status="approved",
        )
        session.add(extra)
        extras_count += 1

    session.flush()
    print(f"  Loaded {extras_count} shift extras")


# ============================================================
# Main
# ============================================================

def import_backup(backup_file: str, clear: bool = False):
    """Import backup data to database."""
    print("\n" + "=" * 60)
    print("Plantao360 Backup Importer")
    print("=" * 60)

    try:
        # Load backup file
        backup_data = load_backup_json(backup_file)

        # Parse data
        print("\nParsing backup data...")
        doctors_data = parse_doctors_from_backup(backup_data)
        shifts_data, shift_parts_data, extras_data = parse_shifts_from_backup(backup_data)

        print(f"  Parsed {len(doctors_data)} doctors")
        print(f"  Parsed {len(shifts_data)} shifts")
        print(f"  Parsed {len(shift_parts_data)} shift assignments")
        print(f"  Parsed {len(extras_data)} shift extras")

        # Get unique periods
        periods_set = {(s["period_year"], s["period_month"]) for s in shifts_data}

        # Load to database
        print("\nPopulating database...")
        session = SessionLocal()
        try:
            if clear:
                clear_database(session)

            doctors = load_doctors(session, doctors_data)
            periods = load_periods(session, periods_set)
            shifts = load_shifts(session, shifts_data, shift_parts_data, periods, doctors)
            load_extras(session, extras_data, shifts, doctors)

            session.commit()
            print("\n" + "=" * 60)
            print("[OK] Database imported successfully!")
            print("=" * 60 + "\n")
        except Exception as e:
            session.rollback()
            print(f"\nError: {e}")
            raise
        finally:
            session.close()

    except FileNotFoundError:
        print(f"Error: File not found: {backup_file}")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON file: {backup_file}")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        raise


def main():
    parser = argparse.ArgumentParser(description="Import backup data to Plantao360")
    parser.add_argument("backup_file", help="Path to backup JSON file")
    parser.add_argument("--clear", action="store_true", help="Clear database before importing")

    args = parser.parse_args()

    if not Path(args.backup_file).exists():
        print(f"Error: File not found: {args.backup_file}")
        exit(1)

    import_backup(args.backup_file, clear=args.clear)


if __name__ == "__main__":
    main()
