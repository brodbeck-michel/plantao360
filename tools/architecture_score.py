#!/usr/bin/env python3
"""
Architecture Score V2 — Calculates architecture quality score.

Uses manifests as the source of truth.

Usage:
    python tools/architecture_score.py
    python tools/architecture_score.py --json
"""

import argparse
import io
import json
import re
import sys
from pathlib import Path
from dataclasses import dataclass

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent))
from manifest_loader import ManifestLoader, ModuleManifest


@dataclass
class ScoreComponent:
    name: str
    score: float
    max_score: float
    details: str


def score_capabilities(modules: list[ModuleManifest]) -> ScoreComponent:
    score = 0
    max_score = 0
    details = []
    for mod in modules:
        resolved = mod.resolve_files()
        for cap_name, rp in resolved.items():
            max_score += 1
            if rp.exists:
                score += 1
            else:
                details.append(f"{mod.canonical_name}: {cap_name} missing")
    return ScoreComponent("Capability Compliance", score, max_score,
                          "; ".join(details[:5]) if details else "All capabilities present")


def score_service_patterns(modules: list[ModuleManifest]) -> ScoreComponent:
    score = 0
    max_score = 0
    details = []
    patterns = ["UnitOfWork", "Success", "Failure", "ErrorCode", "EventDispatcher"]
    for mod in modules:
        if mod.has_capability("service"):
            resolved = mod.resolve_files()
            if "service" in resolved and resolved["service"].exists:
                content = resolved["service"].path.read_text(encoding="utf-8")
                for pattern in patterns:
                    max_score += 1
                    if pattern in content:
                        score += 1
                    else:
                        details.append(f"{mod.canonical_name}: no {pattern}")
    return ScoreComponent("Service Patterns", score, max_score,
                          "; ".join(details[:5]) if details else "All patterns present")


def score_event_versioning() -> ScoreComponent:
    from manifest_loader import APP_DIR
    events_path = APP_DIR / "domain" / "events" / "event_names.py"
    if not events_path.exists():
        return ScoreComponent("Event Versioning", 0, 1, "No event_names.py")
    content = events_path.read_text(encoding="utf-8")
    versioned = len(re.findall(r'\.v1"', content))
    total = len(re.findall(r'= "', content))
    if total == 0:
        return ScoreComponent("Event Versioning", 1, 1, "No events defined")
    score = versioned / total
    return ScoreComponent("Event Versioning", score, 1, f"{versioned}/{total} versioned")


def score_manifests() -> ScoreComponent:
    from manifest_loader import MANIFESTS_DIR
    if not MANIFESTS_DIR.exists():
        return ScoreComponent("Manifest Coverage", 0, 1, "No manifests directory")
    yaml_files = list(MANIFESTS_DIR.glob("*.yaml"))
    # Each module in codebase should have a manifest
    from manifest_loader import APP_DIR
    models_dir = APP_DIR / "models"
    if not models_dir.exists():
        return ScoreComponent("Manifest Coverage", 0, 1, "No models directory")
    model_files = [f for f in models_dir.glob("*.py") if not f.name.startswith("_")]
    total = len(model_files)
    covered = len(yaml_files)
    if total == 0:
        return ScoreComponent("Manifest Coverage", 1, 1, "No modules")
    return ScoreComponent("Manifest Coverage", covered, total, f"{covered}/{total} modules have manifests")


def calculate_score() -> tuple[float, list[ScoreComponent]]:
    loader = ManifestLoader()
    manifests = list(loader.load_all().values())
    components = [
        score_capabilities(manifests),
        score_service_patterns(manifests),
        score_event_versioning(),
        score_manifests(),
    ]
    total_weighted = sum(c.score for c in components)
    total_max = sum(c.max_score for c in components)
    if total_max == 0:
        return 0.0, components
    final_score = (total_weighted / total_max) * 100
    return final_score, components


def main():
    parser = argparse.ArgumentParser(description="Architecture Score V2")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    score, components = calculate_score()

    if args.json:
        data = {
            "score": round(score, 1),
            "components": [{"name": c.name, "score": c.score, "max": c.max_score, "details": c.details} for c in components]
        }
        print(json.dumps(data, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"  Architecture Score V2 — Plantão 360")
        print(f"{'='*60}\n")
        for c in components:
            pct = (c.score / c.max_score * 100) if c.max_score > 0 else 0
            bar = "#" * int(pct / 5) + "-" * (20 - int(pct / 5))
            print(f"  {c.name:25s} [{bar}] {pct:5.1f}%  {c.details}")
        print(f"\n{'='*60}")
        print(f"  FINAL SCORE: {score:.1f}/100")
        print(f"{'='*60}\n")

    sys.exit(0 if score >= 80 else 1)


if __name__ == "__main__":
    main()
