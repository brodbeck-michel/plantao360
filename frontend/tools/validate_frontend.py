#!/usr/bin/env python3
"""
Frontend Architecture Validator — Plantão 360

Valida automaticamente a estrutura, imports, API contracts e naming de features.

Uso:
    python validate_frontend.py [feature_name]

Exemplo:
    python validate_frontend.py doctor
    python validate_frontend.py  # valida todas
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple

# ============================================================
# Constants
# ============================================================

FRONTEND_ROOT = Path(__file__).parent.parent
FEATURES_DIR = FRONTEND_ROOT / "src" / "features"
SHARED_DIR = FRONTEND_ROOT / "src" / "shared"
MANIFESTS_DIR = FRONTEND_ROOT / "manifests"

FORBIDDEN_IMPORTS = [
    "axios",
    "src/api/client",
    "src/config/api",
    "src/config/urls",
]

REQUIRED_STRUCTURE = {
    "directories": ["components", "hooks", "services", "types", "pages"],
    "files": ["index.ts"],
}

# ============================================================
# Validators
# ============================================================

def validate_structure(feature_name: str) -> Tuple[bool, List[str], List[str]]:
    """Validate feature directory structure."""
    feature_path = FEATURES_DIR / feature_name
    errors = []
    warnings = []

    for dir_name in REQUIRED_STRUCTURE["directories"]:
        dir_path = feature_path / dir_name
        if not dir_path.exists():
            errors.append(f"Missing required directory: {dir_name}")

    for file_name in REQUIRED_STRUCTURE["files"]:
        file_path = feature_path / file_name
        if not file_path.exists():
            warnings.append(f"Missing recommended file: {file_name}")

    return len(errors) == 0, errors, warnings


def validate_imports(feature_name: str) -> Tuple[bool, List[str], List[str]]:
    """Validate that no forbidden imports exist."""
    feature_path = FEATURES_DIR / feature_name
    errors = []
    warnings = []

    def check_file(file_path: Path):
        content = file_path.read_text(encoding="utf-8")
        lines = content.split("\n")
        for i, line in enumerate(lines, 1):
            for forbidden in FORBIDDEN_IMPORTS:
                if forbidden in line:
                    rel_path = file_path.relative_to(feature_path)
                    errors.append(f"Forbidden import in {rel_path}:{i}: {forbidden}")

    def walk_dir(dir_path: Path):
        for item in dir_path.iterdir():
            if item.is_dir():
                walk_dir(item)
            elif item.suffix in (".ts", ".tsx"):
                check_file(item)

    walk_dir(feature_path)

    return len(errors) == 0, errors, warnings


def validate_manifest(feature_name: str) -> Tuple[bool, List[str], List[str]]:
    """Validate feature manifest."""
    manifest_path = MANIFESTS_DIR / f"{feature_name}.json"
    errors = []
    warnings = []

    if not manifest_path.exists():
        errors.append(f"Manifest file not found: {feature_name}.json")
        return False, errors, warnings

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        errors.append(f"Invalid JSON in manifest: {e}")
        return False, errors, warnings

    if not manifest.get("name"):
        errors.append('Manifest missing "name" field')
    if not manifest.get("routes"):
        errors.append('Manifest missing "routes" field')

    return len(errors) == 0, errors, warnings


def validate_naming(feature_name: str) -> Tuple[bool, List[str], List[str]]:
    """Validate feature naming conventions."""
    errors = []
    warnings = []

    if not feature_name.islower():
        errors.append(f"Feature name must be lowercase: {feature_name}")
    if "-" in feature_name:
        errors.append(f"Feature name must not contain hyphens: {feature_name}")
    if not feature_name.isidentifier():
        errors.append(f"Feature name must be a valid identifier: {feature_name}")

    return len(errors) == 0, errors, warnings


# ============================================================
# Main Validator
# ============================================================

def validate_feature(feature_name: str) -> Dict:
    """Validate a single feature."""
    results = {
        "feature": feature_name,
        "passed": True,
        "errors": [],
        "warnings": [],
    }

    for validator_name, validator in [
        ("naming", validate_naming),
        ("structure", validate_structure),
        ("imports", validate_imports),
        ("manifest", validate_manifest),
    ]:
        passed, errors, warnings = validator(feature_name)
        if not passed:
            results["passed"] = False
        results["errors"].extend(errors)
        results["warnings"].extend(warnings)

    return results


def validate_all_features() -> List[Dict]:
    """Validate all features."""
    results = []

    if not FEATURES_DIR.exists():
        return results

    for item in FEATURES_DIR.iterdir():
        if item.is_dir():
            results.append(validate_feature(item.name))

    return results


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    feature_name = sys.argv[1] if len(sys.argv) > 1 else None

    if feature_name:
        print(f"\n🔍 Validating feature: {feature_name}\n")
        results = [validate_feature(feature_name)]
    else:
        print("\n🔍 Validating all features...\n")
        results = validate_all_features()

    all_passed = all(r["passed"] for r in results)

    for result in results:
        icon = "✅" if result["passed"] else "❌"
        print(f"{icon} {result['feature']}:")
        for error in result["errors"]:
            print(f"   ❌ {error}")
        for warning in result["warnings"]:
            print(f"   ⚠️  {warning}")
        if not result["errors"] and not result["warnings"]:
            print("   All checks passed")
        print()

    print("✅ All validations passed" if all_passed else "❌ Some validations failed")
    sys.exit(0 if all_passed else 1)
