#!/usr/bin/env python3
"""
Template Consistency Check — Ensures templates match Golden Module.

Usage:
    python tools/check_templates.py
"""

import io
import os
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BACKEND_DIR = Path(__file__).parent.parent / "backend"
APP_DIR = BACKEND_DIR / "app"
TEMPLATE_DIR = BACKEND_DIR / "templates" / "golden-module"


def to_snake_case(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def check_templates_exist() -> list[dict]:
    results = []
    required_templates = [
        "models/model.py.j2",
        "repositories/interfaces/repository_interface.py.j2",
        "repositories/repository.py.j2",
        "services/service.py.j2",
        "mappers/mapper.py.j2",
        "validators/validator.py.j2",
        "validators/rules/unique_field.py.j2",
        "schemas/create.py.j2",
        "schemas/update.py.j2",
        "schemas/response.py.j2",
        "schemas/summary.py.j2",
        "schemas/filters.py.j2",
        "schemas/query.py.j2",
        "schemas/__init__.py.j2",
        "routes/router.py.j2",
        "domain/errors/error_codes.py.j2",
        "tests/unit/test_model.py.j2",
        "tests/unit/test_repository.py.j2",
        "tests/unit/test_service.py.j2",
        "tests/unit/test_mapper.py.j2",
        "tests/unit/test_validator.py.j2",
        "tests/integration/test_api.py.j2",
        "tests/contracts/test_contracts.py.j2",
    ]

    for tpl in required_templates:
        path = TEMPLATE_DIR / tpl
        results.append({
            "template": tpl,
            "exists": path.exists(),
            "size": path.stat().st_size if path.exists() else 0
        })

    return results


def check_golden_module_matches_template() -> list[dict]:
    results = []
    golden_snake = "doctor"

    # Compare model structure
    golden_model = APP_DIR / "models" / f"{golden_snake}.py"
    template_model = TEMPLATE_DIR / "models" / "model.py.j2"
    if golden_model.exists() and template_model.exists():
        golden_content = golden_model.read_text(encoding="utf-8")
        template_content = template_model.read_text(encoding="utf-8")
        # Check key patterns exist in both
        patterns = ["class.*Base.*TimestampMixin.*SoftDeleteMixin", "__tablename__", "Mapped\\["]
        for pattern in patterns:
            golden_has = bool(re.search(pattern, golden_content))
            template_has = bool(re.search(pattern.replace("{{module_name}}", "Doctor"), template_content))
            results.append({
                "component": f"Model pattern: {pattern[:30]}",
                "golden": golden_has,
                "template": template_has,
                "match": golden_has == template_has
            })

    # Compare service structure
    golden_service = APP_DIR / "services" / f"{golden_snake}_service.py"
    template_service = TEMPLATE_DIR / "services" / "service.py.j2"
    if golden_service.exists() and template_service.exists():
        golden_content = golden_service.read_text(encoding="utf-8")
        template_content = template_service.read_text(encoding="utf-8")
        patterns = ["UnitOfWork", "Result", "Success", "Failure", "EventDispatcher", "ErrorCode"]
        for pattern in patterns:
            golden_has = pattern in golden_content
            template_has = pattern in template_content
            results.append({
                "component": f"Service: {pattern}",
                "golden": golden_has,
                "template": template_has,
                "match": golden_has == template_has
            })

    return results


def main():
    print(f"\n{'='*60}")
    print(f"  Template Consistency Check — Plantão 360")
    print(f"{'='*60}\n")

    # Check templates exist
    print("  Template Files:")
    template_results = check_templates_exist()
    all_exist = True
    for r in template_results:
        status = "OK" if r["exists"] else "MISSING"
        print(f"    [{status}] {r['template']}")
        if not r["exists"]:
            all_exist = False

    # Check Golden Module matches templates
    print("\n  Golden Module vs Templates:")
    match_results = check_golden_module_matches_template()
    all_match = True
    for r in match_results:
        status = "MATCH" if r["match"] else "MISMATCH"
        print(f"    [{status}] {r['component']}")
        if not r["match"]:
            all_match = False

    print(f"\n{'='*60}")
    print(f"  Templates: {'ALL PRESENT' if all_exist else 'SOME MISSING'}")
    print(f"  Consistency: {'ALL MATCH' if all_match else 'SOME MISMATCHES'}")
    print(f"  Overall: {'PASS' if all_exist and all_match else 'FAIL'}")
    print(f"{'='*60}\n")

    sys.exit(0 if all_exist and all_match else 1)


if __name__ == "__main__":
    main()
