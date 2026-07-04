#!/usr/bin/env python3
"""
Manifest Validator — Plantão 360

Valida automaticamente todos os manifests de features.

Uso:
    python manifest_validator.py [feature_name]

Exemplo:
    python manifest_validator.py doctor
    python manifest_validator.py  # valida todos
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List

# ============================================================
# Constants
# ============================================================

FRONTEND_ROOT = Path(__file__).parent.parent
MANIFESTS_DIR = FRONTEND_ROOT / "manifests"

REQUIRED_FIELDS = [
    "name",
    "version",
    "description",
    "type",
    "golden_module",
    "generated_from",
    "golden_version",
    "owner",
    "maturity",
    "routes",
    "components",
    "hooks",
    "services",
    "types",
    "tests",
    "shared_dependencies",
]

VALID_MATURITY_LEVELS = ["experimental", "alpha", "beta", "production_ready", "golden"]

# ============================================================
# Validator
# ============================================================

def validate_manifest(feature_name: str) -> Dict:
    """Validate a feature manifest."""
    manifest_path = MANIFESTS_DIR / f"{feature_name}.json"
    errors = []
    warnings = []

    if not manifest_path.exists():
        return {
            "feature": feature_name,
            "passed": False,
            "errors": [f"Manifest not found: {feature_name}.json"],
            "warnings": [],
        }

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return {
            "feature": feature_name,
            "passed": False,
            "errors": [f"Invalid JSON: {e}"],
            "warnings": [],
        }

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in manifest:
            errors.append(f"Missing required field: {field}")

    # Check maturity level
    if "maturity" in manifest:
        if manifest["maturity"] not in VALID_MATURITY_LEVELS:
            errors.append(f"Invalid maturity level: {manifest['maturity']}")

    # Check routes structure
    if "routes" in manifest:
        for route_name, route in manifest["routes"].items():
            if "path" not in route:
                errors.append(f"Route '{route_name}' missing 'path'")
            if "component" not in route:
                errors.append(f"Route '{route_name}' missing 'component'")

    return {
        "feature": feature_name,
        "passed": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    feature_name = sys.argv[1] if len(sys.argv) > 1 else None

    if feature_name:
        print(f"\n📋 Validating manifest for: {feature_name}\n")
        result = validate_manifest(feature_name)
        results = [result]
    else:
        print("\n📋 Validating all manifests...\n")
        results = []
        if MANIFESTS_DIR.exists():
            for item in MANIFESTS_DIR.iterdir():
                if item.suffix == ".json":
                    results.append(validate_manifest(item.stem))

    # Display results
    all_passed = True
    for result in results:
        if result["passed"]:
            print(f"✅ {result['feature']}: Manifest valid")
        else:
            all_passed = False
            print(f"❌ {result['feature']}:")
            for error in result["errors"]:
                print(f"   ❌ {error}")
            for warning in result["warnings"]:
                print(f"   ⚠️  {warning}")
        print()

    print("✅ All manifests valid" if all_passed else "❌ Some manifests invalid")
    sys.exit(0 if all_passed else 1)
