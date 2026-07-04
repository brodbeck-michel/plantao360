#!/usr/bin/env python3
"""
Template Drift Detector — Plantão 360

Compara features com o Golden Module e detecta divergências.

Uso:
    python template_drift.py [feature_name]

Exemplo:
    python template_drift.py period
    python template_drift.py  # compara todas
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
GOLDEN_MODULE = "doctor"

# ============================================================
# Drift Detector
# ============================================================

def detect_drift(feature_name: str) -> Dict:
    """Detect drift between a feature and the Golden Module."""
    golden_path = FEATURES_DIR / GOLDEN_MODULE
    feature_path = FEATURES_DIR / feature_name

    if not feature_path.exists():
        return {"feature": feature_name, "drift": True, "issues": ["Feature does not exist"]}

    issues = []

    # Check directory structure
    golden_dirs = set()
    for item in golden_path.iterdir():
        if item.is_dir():
            golden_dirs.add(item.name)

    feature_dirs = set()
    for item in feature_path.iterdir():
        if item.is_dir():
            feature_dirs.add(item.name)

    missing_dirs = golden_dirs - feature_dirs
    extra_dirs = feature_dirs - golden_dirs

    if missing_dirs:
        issues.append(f"Missing directories: {', '.join(missing_dirs)}")
    if extra_dirs:
        issues.append(f"Extra directories: {', '.join(extra_dirs)}")

    # Check file count in each directory
    for dir_name in golden_dirs & feature_dirs:
        golden_dir = golden_path / dir_name
        feature_dir = feature_path / dir_name

        golden_files = len([f for f in golden_dir.iterdir() if f.is_file()])
        feature_files = len([f for f in feature_dir.iterdir() if f.is_file()])

        if feature_files < golden_files:
            issues.append(f"{dir_name}/: Expected {golden_files} files, found {feature_files}")

    # Check index.ts exists
    if not (feature_path / "index.ts").exists():
        issues.append("Missing index.ts")

    return {
        "feature": feature_name,
        "drift": len(issues) > 0,
        "issues": issues,
    }


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    feature_name = sys.argv[1] if len(sys.argv) > 1 else None

    if feature_name:
        print(f"\n🔍 Checking drift for: {feature_name}\n")
        result = detect_drift(feature_name)
        results = [result]
    else:
        print("\n🔍 Checking drift for all features...\n")
        results = []
        if FEATURES_DIR.exists():
            for item in FEATURES_DIR.iterdir():
                if item.is_dir() and item.name != GOLDEN_MODULE:
                    results.append(detect_drift(item.name))

    # Display results
    all_clean = True
    for result in results:
        if result["drift"]:
            all_clean = False
            print(f"❌ {result['feature']}:")
            for issue in result["issues"]:
                print(f"   - {issue}")
        else:
            print(f"✅ {result['feature']}: No drift detected")
        print()

    print("✅ No drift detected" if all_clean else "❌ Drift detected")
    sys.exit(0 if all_clean else 1)
