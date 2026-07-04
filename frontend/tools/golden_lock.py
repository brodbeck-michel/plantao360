#!/usr/bin/env python3
"""
Golden Lock Validator — Plantão 360

Valida se features seguem o Golden Lock.

Uso:
    python golden_lock.py [feature_name]

Exemplo:
    python golden_lock.py doctor
    python golden_lock.py  # valida todas
"""

import os
import sys
from pathlib import Path
from typing import Dict, List

# ============================================================
# Constants
# ============================================================

FRONTEND_ROOT = Path(__file__).parent.parent
FEATURES_DIR = FRONTEND_ROOT / "src" / "features"
GOLDEN_MODULE = "doctor"

# ============================================================
# Golden Lock Requirements
# ============================================================

REQUIRED_DIRECTORIES = [
    "api",
    "components",
    "dialogs",
    "details",
    "filters",
    "forms",
    "hooks",
    "history",
    "audit",
    "pages",
    "services",
    "tables",
    "types",
    "utils",
    "manifest",
    "tests",
]

REQUIRED_FILES = ["index.ts"]

REQUIRED_PATTERNS = {
    "query_hooks": ["useQuery", "useMutation"],
    "api_client": ["apiClient"],
    "query_factory": ["createQuery", "createMutation"],
    "error_handling": ["ErrorBoundary", "showError"],
    "loading_state": ["LoadingSpinner", "isLoading"],
    "empty_state": ["EmptyState"],
    "aria_labels": ["aria-label"],
}

# ============================================================
# Validator
# ============================================================

def validate_golden_lock(feature_name: str) -> Dict:
    """Validate if a feature follows the Golden Lock."""
    feature_path = FEATURES_DIR / feature_name
    issues = []

    if not feature_path.exists():
        return {"feature": feature_name, "passed": False, "issues": ["Feature does not exist"]}

    # Check directories
    for dir_name in REQUIRED_DIRECTORIES:
        if not (feature_path / dir_name).is_dir():
            issues.append(f"Missing directory: {dir_name}")

    # Check files
    for file_name in REQUIRED_FILES:
        if not (feature_path / file_name).exists():
            issues.append(f"Missing file: {file_name}")

    # Check patterns
    for pattern_name, keywords in REQUIRED_PATTERNS.items():
        found = False
        for item in feature_path.rglob("*.ts"):
            content = item.read_text(encoding="utf-8")
            if any(kw in content for kw in keywords):
                found = True
                break
        if not found:
            for item in feature_path.rglob("*.tsx"):
                content = item.read_text(encoding="utf-8")
                if any(kw in content for kw in keywords):
                    found = True
                    break
        if not found:
            issues.append(f"Missing pattern: {pattern_name}")

    return {
        "feature": feature_name,
        "passed": len(issues) == 0,
        "issues": issues,
    }


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    feature_name = sys.argv[1] if len(sys.argv) > 1 else None

    if feature_name:
        print(f"\n🔒 Validating Golden Lock for: {feature_name}\n")
        result = validate_golden_lock(feature_name)
        results = [result]
    else:
        print("\n🔒 Validating Golden Lock for all features...\n")
        results = []
        if FEATURES_DIR.exists():
            for item in FEATURES_DIR.iterdir():
                if item.is_dir():
                    results.append(validate_golden_lock(item.name))

    # Display results
    all_passed = True
    for result in results:
        if result["passed"]:
            print(f"✅ {result['feature']}: Golden Lock compliant")
        else:
            all_passed = False
            print(f"❌ {result['feature']}:")
            for issue in result["issues"]:
                print(f"   - {issue}")
        print()

    print("✅ All features compliant" if all_passed else "❌ Some features non-compliant")
    sys.exit(0 if all_passed else 1)
