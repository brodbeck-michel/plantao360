"""
Test script for import_backup functionality

Usage:
    python -m scripts.test_import
"""

import json
import tempfile
from pathlib import Path
from datetime import date

def create_sample_backup():
    """Create a sample backup JSON for testing."""
    return {
        "version": 2,
        "exported": "2026-08-06T12:34:39.983Z",
        "data": {
            "doctor_vlh": {
                "José Nixon Batista": 176.26,
                "Ana Carolina da Silva Mota": 158.63,
                "Samuel de Medeiros Locks": 164.51,
                "Priscila Martins Wiggers": 164.51,
            },
            "doctor_meta": {
                "José Nixon Batista": {
                    "rqe": "SIM",
                    "admissao": "08/2008"
                },
                "Ana Carolina da Silva Mota": {
                    "rqe": "SIM",
                    "admissao": "03/2022"
                },
                "Samuel de Medeiros Locks": {
                    "rqe": "SIM",
                    "admissao": "12/2020"
                },
                "Priscila Martins Wiggers": {
                    "rqe": "NAO",
                    "admissao": "01/2012"
                },
            },
            "shifts_2026-07": {
                "2026-07-01": {
                    "T1": "José Nixon Batista",
                    "T2": "Priscila Martins Wiggers",
                    "T3": "Samuel de Medeiros Locks",
                    "R1": "Ana Carolina da Silva Mota",
                    "R2": "Ana Carolina da Silva Mota",
                },
                "2026-07-02": {
                    "T1": "Ana Carolina da Silva Mota",
                    "T2": {
                        "type": "split",
                        "parts": [
                            {
                                "doc": "Samuel de Medeiros Locks",
                                "start": "15:00",
                                "end": "19:00",
                                "hours": 4
                            },
                            {
                                "doc": "Priscila Martins Wiggers",
                                "start": "19:00",
                                "end": "21:00",
                                "hours": 2
                            }
                        ]
                    },
                    "R1": "José Nixon Batista",
                    "R2": "José Nixon Batista",
                    "_extras": [
                        {
                            "doc": "Samuel de Medeiros Locks",
                            "start": "21:00",
                            "end": "23:00",
                            "hours": 2,
                            "obs": "Ficou ajudando no fluxo"
                        }
                    ]
                },
            },
            "shifts_2026-06": {},
            "shifts_2026-05": {},
            "shifts_2026-04": {},
            "shifts_2026-03": {},
            "doctors_unimed": []
        }
    }


def test_backup_creation():
    """Test creating a sample backup file."""
    print("Creating sample backup...")
    backup = create_sample_backup()

    # Write to temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(backup, f)
        temp_file = f.name

    print(f"[OK] Sample backup created: {temp_file}")
    return temp_file


def test_import():
    """Test the import functionality."""
    print("\nTesting import_backup module...")

    try:
        from scripts.import_backup import (
            parse_doctors_from_backup,
            parse_shifts_from_backup,
            load_backup_json
        )
        print("[OK] import_backup module loaded successfully")

        # Create sample backup
        backup_file = test_backup_creation()

        # Load and parse
        print("\nParsing sample backup...")
        backup_data = load_backup_json(backup_file)
        print("[OK] Backup loaded successfully")

        # Parse doctors
        doctors = parse_doctors_from_backup(backup_data)
        print(f"[OK] Parsed {len(doctors)} doctors:")
        for doc in doctors:
            print(f"  - {doc['name']} (CRM: {doc['crm']}, RQE: {doc['has_rqe']})")

        # Parse shifts
        shifts, parts, extras = parse_shifts_from_backup(backup_data)
        print(f"\n[OK] Parsed shifts:")
        print(f"  - {len(shifts)} shifts")
        print(f"  - {len(parts)} shift parts")
        print(f"  - {len(extras)} extras")

        if shifts:
            shift = shifts[0]
            print(f"\n  Sample shift:")
            print(f"    Date: {shift['shift_date']}")
            print(f"    Type: {shift['shift_type']}")
            print(f"    Period: {shift['period_year']}-{shift['period_month']:02d}")

        if parts:
            part = parts[0]
            print(f"\n  Sample shift part:")
            print(f"    Doctor: {part['doctor_name']}")
            print(f"    Duration: {part['duration_minutes']} minutes")

        if extras:
            extra = extras[0]
            print(f"\n  Sample extra:")
            print(f"    Doctor: {extra['doctor_name']}")
            print(f"    Duration: {extra['duration_minutes']} minutes")
            print(f"    Justification: {extra['justification']}")

        # Cleanup
        Path(backup_file).unlink()
        print(f"\n[OK] Cleanup completed")

        print("\n" + "=" * 60)
        print("All tests passed! Import script is ready to use.")
        print("=" * 60)

    except ImportError as e:
        print(f"[ERROR] Import error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    import sys
    sys.exit(0 if test_import() else 1)
