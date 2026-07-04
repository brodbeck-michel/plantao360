#!/usr/bin/env python3
"""
UX Validator — Plantão 360

Valida automaticamente padrões UX em todas as features.

Uso:
    python ux_validator.py [feature_name]

Exemplo:
    python ux_validator.py doctor
    python ux_validator.py  # valida todas
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

# ============================================================
# UX Requirements
# ============================================================

UX_REQUIREMENTS = [
    ("has_loading", "Loading State", ["loading", "LoadingSpinner", "isLoading"]),
    ("has_empty_state", "Empty State", ["EmptyState", "empty", "nenhum"]),
    ("has_error_handling", "Error Handling", ["error", "ErrorBoundary", "showError"]),
    ("has_success_feedback", "Success Feedback", ["showSuccess", "success", "snackbar"]),
    ("has_aria_labels", "ARIA Labels", ["aria-label", "aria-labelledby"]),
    ("has_keyboard_nav", "Keyboard Navigation", ["onKeyDown", "tabIndex"]),
    ("has_responsive", "Responsive Design", ["xs=", "sm=", "md=", "lg=", "Grid"]),
    ("has_domain_explanation", "Domain Explanation", ["DomainExplanation", "domain"]),
]

# ============================================================
# Validator
# ============================================================

def validate_ux(feature_name: str) -> Dict:
    """Validate UX requirements for a feature."""
    feature_path = FEATURES_DIR / feature_name
    if not feature_path.exists():
        return {"feature": feature_name, "passed": False, "issues": ["Feature does not exist"]}

    issues = []

    # Check pages
    pages_dir = feature_path / "pages"
    if pages_dir.exists():
        for page_file in pages_dir.iterdir():
            if page_file.suffix in (".ts", ".tsx"):
                content = page_file.read_text(encoding="utf-8")

                for req_id, req_name, keywords in UX_REQUIREMENTS:
                    found = any(kw.lower() in content.lower() for kw in keywords)
                    if not found:
                        issues.append(f"{page_file.name}: Missing {req_name}")

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
        print(f"\n🎨 Validating UX for: {feature_name}\n")
        result = validate_ux(feature_name)
        results = [result]
    else:
        print("\n🎨 Validating UX for all features...\n")
        results = []
        if FEATURES_DIR.exists():
            for item in FEATURES_DIR.iterdir():
                if item.is_dir():
                    results.append(validate_ux(item.name))

    # Display results
    all_passed = True
    for result in results:
        if result["passed"]:
            print(f"✅ {result['feature']}: UX validated")
        else:
            all_passed = False
            print(f"❌ {result['feature']}:")
            for issue in result["issues"]:
                print(f"   - {issue}")
        print()

    print("✅ All UX validations passed" if all_passed else "❌ Some UX validations failed")
    sys.exit(0 if all_passed else 1)
