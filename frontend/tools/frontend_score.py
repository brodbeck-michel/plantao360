#!/usr/bin/env python3
"""
Frontend Score — Plantão 360

Calcula score de qualidade para cada feature.

Uso:
    python frontend_score.py [feature_name]

Exemplo:
    python frontend_score.py doctor
    python frontend_score.py  # score de todas
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
FEATURES_DIR = FRONTEND_ROOT / "src" / "features"
SHARED_DIR = FRONTEND_ROOT / "src" / "shared"
MANIFESTS_DIR = FRONTEND_ROOT / "manifests"

# ============================================================
# Score Criteria
# ============================================================

CRITERIA = {
    "architecture": {
        "weight": 20,
        "checks": [
            ("has_index_ts", "Barrel file (index.ts)"),
            ("has_types_dir", "Types directory"),
            ("has_hooks_dir", "Hooks directory"),
            ("has_services_dir", "Services directory"),
            ("has_pages_dir", "Pages directory"),
            ("has_components_dir", "Components directory"),
            ("has_dialogs_dir", "Dialogs directory"),
            ("has_forms_dir", "Forms directory"),
            ("has_tables_dir", "Tables directory"),
            ("has_filters_dir", "Filters directory"),
        ],
    },
    "reuse": {
        "weight": 15,
        "checks": [
            ("uses_shared_components", "Uses shared components"),
            ("uses_query_factory", "Uses query factory"),
            ("uses_api_client", "Uses API client"),
            ("no_direct_axios", "No direct Axios imports"),
        ],
    },
    "performance": {
        "weight": 10,
        "checks": [
            ("has_lazy_loading", "Lazy loading"),
            ("has_memoization", "Memoization"),
        ],
    },
    "accessibility": {
        "weight": 15,
        "checks": [
            ("has_aria_labels", "ARIA labels"),
            ("has_keyboard_nav", "Keyboard navigation"),
            ("has_screen_reader", "Screen reader support"),
        ],
    },
    "ux": {
        "weight": 15,
        "checks": [
            ("has_empty_state", "Empty state"),
            ("has_loading_state", "Loading state"),
            ("has_error_state", "Error state"),
            ("has_success_feedback", "Success feedback"),
            ("has_confirmation_dialog", "Confirmation dialog"),
        ],
    },
    "testing": {
        "weight": 10,
        "checks": [
            ("has_tests_dir", "Tests directory"),
            ("has_test_files", "Test files"),
        ],
    },
    "documentation": {
        "weight": 10,
        "checks": [
            ("has_manifest", "Manifest"),
            ("has_readme", "README"),
        ],
    },
    "componentization": {
        "weight": 5,
        "checks": [
            ("has_components", "Components"),
            ("has_hooks", "Hooks"),
        ],
    },
}


# ============================================================
# Check Functions
# ============================================================

def has_index_ts(feature_path: Path) -> bool:
    return (feature_path / "index.ts").exists()

def has_types_dir(feature_path: Path) -> bool:
    return (feature_path / "types").is_dir()

def has_hooks_dir(feature_path: Path) -> bool:
    return (feature_path / "hooks").is_dir()

def has_services_dir(feature_path: Path) -> bool:
    return (feature_path / "services").is_dir()

def has_pages_dir(feature_path: Path) -> bool:
    return (feature_path / "pages").is_dir()

def has_components_dir(feature_path: Path) -> bool:
    return (feature_path / "components").is_dir()

def has_dialogs_dir(feature_path: Path) -> bool:
    return (feature_path / "dialogs").is_dir()

def has_forms_dir(feature_path: Path) -> bool:
    return (feature_path / "forms").is_dir()

def has_tables_dir(feature_path: Path) -> bool:
    return (feature_path / "tables").is_dir()

def has_filters_dir(feature_path: Path) -> bool:
    return (feature_path / "filters").is_dir()

def uses_shared_components(feature_path: Path) -> bool:
    shared_dir = SHARED_DIR / "components"
    if not shared_dir.exists():
        return False
    for item in shared_dir.iterdir():
        if item.suffix == ".tsx" and item.name != "index.ts":
            return True
    return False

def uses_query_factory(feature_path: Path) -> bool:
    services_dir = feature_path / "services"
    if not services_dir.exists():
        return False
    for item in services_dir.iterdir():
        if item.suffix == ".ts":
            content = item.read_text(encoding="utf-8")
            if "query-factory" in content:
                return True
    return False

def uses_api_client(feature_path: Path) -> bool:
    services_dir = feature_path / "services"
    if not services_dir.exists():
        return False
    for item in services_dir.iterdir():
        if item.suffix == ".ts":
            content = item.read_text(encoding="utf-8")
            if "api/client" in content:
                return True
    return False

def no_direct_axios(feature_path: Path) -> bool:
    for item in feature_path.rglob("*.ts"):
        content = item.read_text(encoding="utf-8")
        if "import axios" in content or "from 'axios'" in content:
            return False
    for item in feature_path.rglob("*.tsx"):
        content = item.read_text(encoding="utf-8")
        if "import axios" in content or "from 'axios'" in content:
            return False
    return True

def has_lazy_loading(feature_path: Path) -> bool:
    pages_dir = feature_path / "pages"
    if not pages_dir.exists():
        return False
    for item in pages_dir.iterdir():
        if item.suffix in (".ts", ".tsx"):
            content = item.read_text(encoding="utf-8")
            if "lazy" in content or "React.lazy" in content:
                return True
    return False

def has_memoization(feature_path: Path) -> bool:
    for item in feature_path.rglob("*.tsx"):
        content = item.read_text(encoding="utf-8")
        if "React.memo" in content or "useMemo" in content or "useCallback" in content:
            return True
    return False

def has_aria_labels(feature_path: Path) -> bool:
    for item in feature_path.rglob("*.tsx"):
        content = item.read_text(encoding="utf-8")
        if "aria-label" in content or "aria-labelledby" in content:
            return True
    return False

def has_keyboard_nav(feature_path: Path) -> bool:
    for item in feature_path.rglob("*.tsx"):
        content = item.read_text(encoding="utf-8")
        if "onKeyDown" in content or "tabIndex" in content:
            return True
    return False

def has_screen_reader(feature_path: Path) -> bool:
    for item in feature_path.rglob("*.tsx"):
        content = item.read_text(encoding="utf-8")
        if "role=" in content or "aria-live" in content or "sr-only" in content:
            return True
    return False

def has_empty_state(feature_path: Path) -> bool:
    pages_dir = feature_path / "pages"
    if not pages_dir.exists():
        return False
    for item in pages_dir.iterdir():
        if item.suffix in (".ts", ".tsx"):
            content = item.read_text(encoding="utf-8")
            if "EmptyState" in content or "empty" in content.lower():
                return True
    return False

def has_loading_state(feature_path: Path) -> bool:
    pages_dir = feature_path / "pages"
    if not pages_dir.exists():
        return False
    for item in pages_dir.iterdir():
        if item.suffix in (".ts", ".tsx"):
            content = item.read_text(encoding="utf-8")
            if "LoadingSpinner" in content or "loading" in content.lower():
                return True
    return False

def has_error_state(feature_path: Path) -> bool:
    pages_dir = feature_path / "pages"
    if not pages_dir.exists():
        return False
    for item in pages_dir.iterdir():
        if item.suffix in (".ts", ".tsx"):
            content = item.read_text(encoding="utf-8")
            if "ErrorBoundary" in content or "error" in content.lower():
                return True
    return False

def has_success_feedback(feature_path: Path) -> bool:
    dialogs_dir = feature_path / "dialogs"
    if not dialogs_dir.exists():
        return False
    for item in dialogs_dir.iterdir():
        if item.suffix in (".ts", ".tsx"):
            content = item.read_text(encoding="utf-8")
            if "showSuccess" in content or "success" in content.lower():
                return True
    return False

def has_confirmation_dialog(feature_path: Path) -> bool:
    dialogs_dir = feature_path / "dialogs"
    if not dialogs_dir.exists():
        return False
    for item in dialogs_dir.iterdir():
        if item.suffix in (".ts", ".tsx"):
            content = item.read_text(encoding="utf-8")
            if "ConfirmDialog" in content or "confirm" in content.lower():
                return True
    return False

def has_tests_dir(feature_path: Path) -> bool:
    return (feature_path / "tests").is_dir()

def has_test_files(feature_path: Path) -> bool:
    tests_dir = feature_path / "tests"
    if not tests_dir.exists():
        return False
    for item in tests_dir.iterdir():
        if item.suffix in (".ts", ".tsx") and "test" in item.name:
            return True
    return False

def has_manifest(feature_path: Path) -> bool:
    manifest_path = MANIFESTS_DIR / f"{feature_path.name}.json"
    return manifest_path.exists()

def has_readme(feature_path: Path) -> bool:
    return (feature_path / "README.md").exists()

def has_components(feature_path: Path) -> bool:
    components_dir = feature_path / "components"
    if not components_dir.exists():
        return False
    for item in components_dir.iterdir():
        if item.suffix == ".tsx":
            return True
    return False

def has_hooks(feature_path: Path) -> bool:
    hooks_dir = feature_path / "hooks"
    if not hooks_dir.exists():
        return False
    for item in hooks_dir.iterdir():
        if item.suffix == ".ts":
            return True
    return False


# ============================================================
# Score Calculator
# ============================================================

def calculate_score(feature_name: str) -> Dict:
    """Calculate score for a feature."""
    feature_path = FEATURES_DIR / feature_name
    if not feature_path.exists():
        return {"feature": feature_name, "score": 0, "grade": "F", "details": {}}

    total_score = 0
    details = {}

    for criteria_name, criteria in CRITERIA.items():
        checks_passed = 0
        checks_total = len(criteria["checks"])

        for check_name, check_label in criteria["checks"]:
            check_func = globals().get(check_name)
            if check_func and check_func(feature_path):
                checks_passed += 1

        criteria_score = (checks_passed / checks_total) * criteria["weight"]
        total_score += criteria_score
        details[criteria_name] = {
            "score": round(criteria_score, 1),
            "max": criteria["weight"],
            "passed": checks_passed,
            "total": checks_total,
        }

    # Grade
    if total_score >= 90:
        grade = "A+"
    elif total_score >= 80:
        grade = "A"
    elif total_score >= 70:
        grade = "B"
    elif total_score >= 60:
        grade = "C"
    elif total_score >= 50:
        grade = "D"
    else:
        grade = "F"

    return {
        "feature": feature_name,
        "score": round(total_score, 1),
        "grade": grade,
        "details": details,
    }


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    feature_name = sys.argv[1] if len(sys.argv) > 1 else None

    if feature_name:
        print(f"\n📊 Calculating score for: {feature_name}\n")
        result = calculate_score(feature_name)
        results = [result]
    else:
        print("\n📊 Calculating scores for all features...\n")
        results = []
        if FEATURES_DIR.exists():
            for item in FEATURES_DIR.iterdir():
                if item.is_dir():
                    results.append(calculate_score(item.name))

    # Display results
    for result in results:
        print(f"{'='*50}")
        print(f"Feature: {result['feature']}")
        print(f"Score: {result['score']}/100 ({result['grade']})")
        print(f"{'='*50}")
        for criteria_name, details in result["details"].items():
            bar = "█" * int(details["score"] / details["max"] * 10)
            empty = "░" * (10 - len(bar))
            print(f"  {criteria_name:20s} [{bar}{empty}] {details['score']}/{details['max']}")
        print()

    # Summary
    if len(results) > 1:
        avg_score = sum(r["score"] for r in results) / len(results)
        print(f"\n{'='*50}")
        print(f"Average Score: {avg_score:.1f}/100")
        print(f"{'='*50}")
