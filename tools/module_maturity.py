#!/usr/bin/env python3
"""
Module Maturity — Analyzes module maturity level.

Usage:
    python tools/module_maturity.py
    python tools/module_maturity.py --module Doctor
"""

import argparse
import io
import json
import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BACKEND_DIR = Path(__file__).parent.parent / "backend"
APP_DIR = BACKEND_DIR / "app"


def to_snake_case(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


@dataclass
class MaturityDimension:
    name: str
    score: float
    max_score: float
    details: str

    @property
    def percentage(self) -> float:
        return (self.score / self.max_score * 100) if self.max_score > 0 else 0


@dataclass
class MaturityReport:
    module: str
    dimensions: list[MaturityDimension] = field(default_factory=list)

    @property
    def overall_score(self) -> float:
        if not self.dimensions:
            return 0.0
        total = sum(d.percentage for d in self.dimensions)
        return total / len(self.dimensions)

    @property
    def level(self) -> str:
        score = self.overall_score
        if score >= 90:
            return "MATURE"
        elif score >= 70:
            return "DEVELOPING"
        elif score >= 50:
            return "EMERGING"
        else:
            return "INITIAL"


def analyze_module(module_name: str) -> MaturityReport:
    snake = to_snake_case(module_name)
    report = MaturityReport(module=module_name)

    # Architecture
    arch_score = 0
    arch_max = 8
    if (APP_DIR / "models" / f"{snake}.py").exists(): arch_score += 1
    if (APP_DIR / "repositories" / "interfaces" / f"{snake}_repository.py").exists(): arch_score += 1
    if (APP_DIR / "repositories" / f"{snake}_repository.py").exists(): arch_score += 1
    if (APP_DIR / "services" / f"{snake}_service.py").exists(): arch_score += 1
    if (APP_DIR / "mappers" / f"{snake}_mapper.py").exists(): arch_score += 1
    if (APP_DIR / "validators" / f"{snake}_validator.py").exists(): arch_score += 1
    if (APP_DIR / "domain" / "errors" / f"{snake}_errors.py").exists(): arch_score += 1
    if (APP_DIR / "api" / "routes" / f"{snake}s.py").exists() or (APP_DIR / "api" / "routes" / f"{snake}.py").exists(): arch_score += 1
    report.dimensions.append(MaturityDimension("Architecture", arch_score, arch_max, f"{arch_score}/{arch_max} components"))

    # DTOs
    dto_score = 0
    dto_max = 5
    schemas_dir = APP_DIR / "schemas" / snake
    for dto_type in ["create", "update", "response", "filters", "query"]:
        if (schemas_dir / f"{snake}_{dto_type}.py").exists():
            dto_score += 1
    report.dimensions.append(MaturityDimension("DTOs", dto_score, dto_max, f"{dto_score}/{dto_max} DTOs"))

    # Tests
    test_score = 0
    test_max = 3
    for test_type in ["unit", "integration", "contracts"]:
        test_dir = APP_DIR / "tests" / test_type
        if test_dir.exists() and list(test_dir.glob(f"test_{snake}_*.py")):
            test_score += 1
    report.dimensions.append(MaturityDimension("Tests", test_score, test_max, f"{test_score}/{test_max} test types"))

    # Documentation
    docs_path = Path(__file__).parent.parent / "docs" / "modules" / f"{snake}-module.md"
    doc_score = 1 if docs_path.exists() else 0
    report.dimensions.append(MaturityDimension("Documentation", doc_score, 1, "Module docs" if doc_score else "No docs"))

    # Compliance
    compliance_score = 0
    compliance_max = 5
    service_path = APP_DIR / "services" / f"{snake}_service.py"
    if service_path.exists():
        content = service_path.read_text(encoding="utf-8")
        if "UnitOfWork" in content: compliance_score += 1
        if "ErrorCode" in content: compliance_score += 1
        if "EventDispatcher" in content: compliance_score += 1
        if "Success" in content and "Failure" in content: compliance_score += 1
    mapper_path = APP_DIR / "mappers" / f"{snake}_mapper.py"
    if mapper_path.exists():
        content = mapper_path.read_text(encoding="utf-8")
        if "BaseMapper" in content: compliance_score += 1
    report.dimensions.append(MaturityDimension("Compliance", compliance_score, compliance_max, f"{compliance_score}/{compliance_max} patterns"))

    return report


def find_modules() -> list[str]:
    models_dir = APP_DIR / "models"
    if not models_dir.exists():
        return []
    modules = []
    for f in models_dir.glob("*.py"):
        if f.name.startswith("_"):
            continue
        name = f.stem
        pascal = "".join(word.capitalize() for word in name.split("_"))
        modules.append(pascal)
    return sorted(modules)


def main():
    parser = argparse.ArgumentParser(description="Module Maturity")
    parser.add_argument("module", nargs="?", help="Module to analyze")
    parser.add_argument("--all", action="store_true", help="Analyze all modules")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    modules = []
    if args.module:
        modules = [args.module]
    elif args.all:
        modules = find_modules()
    else:
        modules = find_modules()

    reports = []
    for mod in modules:
        report = analyze_module(mod)
        reports.append(report)

    if args.json:
        data = [{"module": r.module, "score": round(r.overall_score, 1), "level": r.level,
                 "dimensions": [asdict(d) for d in r.dimensions]} for r in reports]
        print(json.dumps(data, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"  Module Maturity — Plantão 360")
        print(f"{'='*60}\n")
        for r in reports:
            print(f"  {r.module:20s} Score: {r.overall_score:5.1f}%  Level: {r.level}")
            for d in r.dimensions:
                bar = "#" * int(d.percentage / 10) + "-" * (10 - int(d.percentage / 10))
                print(f"    {d.name:20s} [{bar}] {d.percentage:5.1f}%  {d.details}")
            print()
        print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
