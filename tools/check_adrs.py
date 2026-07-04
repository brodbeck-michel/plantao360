#!/usr/bin/env python3
"""
ADR Validator — Ensures architectural changes have ADRs.

Usage:
    python tools/check_adrs.py
    python tools/check_adrs.py --strict
"""

import argparse
import io
import os
import re
import sys
from pathlib import Path
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BACKEND_DIR = Path(__file__).parent.parent / "backend"
DOCS_DIR = Path(__file__).parent.parent / "docs"
ADR_DIR = DOCS_DIR / "adr"


def find_adrs() -> list[dict]:
    adrs = []
    if not ADR_DIR.exists():
        return adrs
    for f in ADR_DIR.glob("ADR-*.md"):
        content = f.read_text(encoding="utf-8")
        number_match = re.match(r"ADR-(\d+)", f.name)
        title_match = re.search(r"^# ADR-\d+: (.+)$", content, re.MULTILINE)
        status_match = re.search(r"\*\*Status:\*\*\s*(\w+)", content)
        adrs.append({
            "file": f.name,
            "number": int(number_match.group(1)) if number_match else 0,
            "title": title_match.group(1) if title_match else "Unknown",
            "status": status_match.group(1) if status_match else "unknown",
            "path": f
        })
    return sorted(adrs, key=lambda x: x["number"])


def check_adr_coverage() -> list[dict]:
    results = []
    adrs = find_adrs()

    # Check ADR numbering continuity
    numbers = [a["number"] for a in adrs]
    if numbers:
        expected = list(range(1, max(numbers) + 1))
        missing = set(expected) - set(numbers)
        if missing:
            results.append({
                "check": "ADR numbering continuity",
                "passed": False,
                "detail": f"Missing ADRs: {sorted(missing)}"
            })
        else:
            results.append({
                "check": "ADR numbering continuity",
                "passed": True,
                "detail": f"ADRs 1-{max(numbers)} present"
            })

    # Check required ADRs exist
    required_adrs = [
        (1, "Monolito Modular"),
        (6, "App Factory"),
        (7, "UUID Foundation"),
        (8, "Domain Constants"),
        (9, "Database Foundation"),
        (10, "Enterprise Application Patterns"),
        (11, "Platform Governance"),
    ]
    for number, title_keyword in required_adrs:
        found = any(a["number"] == number for a in adrs)
        results.append({
            "check": f"ADR-{number:03d} ({title_keyword})",
            "passed": found,
            "detail": "Present" if found else "Missing"
        })

    # Check ADR statuses
    active_adrs = [a for a in adrs if a["status"] in ("accepted", "proposed")]
    results.append({
        "check": "Active ADRs",
        "passed": len(active_adrs) > 0,
        "detail": f"{len(active_adrs)} active ADRs"
    })

    return results


def main():
    parser = argparse.ArgumentParser(description="ADR Validator")
    parser.add_argument("--strict", action="store_true", help="Strict mode")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  ADR Validator — Plantão 360")
    print(f"{'='*60}\n")

    adrs = find_adrs()
    print(f"  Found {len(adrs)} ADRs:")
    for adr in adrs:
        print(f"    ADR-{adr['number']:03d}: {adr['title']} [{adr['status']}]")

    print(f"\n  Coverage Checks:")
    results = check_adr_coverage()
    all_passed = True
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"    [{status}] {r['check']} — {r['detail']}")
        if not r["passed"]:
            all_passed = False

    print(f"\n{'='*60}")
    print(f"  Overall: {'PASS' if all_passed else 'FAIL'}")
    print(f"{'='*60}\n")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
