#!/usr/bin/env python3
"""
Code Metrics for Plantão 360.

Generates project metrics and statistics.

Usage:
    python tools/project_metrics.py
    python tools/project_metrics.py --json
"""

import argparse
import ast
import json
import os
import re
import sys
import io
from pathlib import Path
from dataclasses import dataclass, field, asdict

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


BACKEND_DIR = Path(__file__).parent.parent / "backend"
APP_DIR = BACKEND_DIR / "app"


@dataclass
class ModuleMetrics:
    name: str
    model_fields: int = 0
    repository_methods: int = 0
    service_methods: int = 0
    dto_count: int = 0
    validator_rules: int = 0
    error_codes: int = 0
    endpoints: int = 0
    test_files: int = 0
    test_functions: int = 0


@dataclass
class ProjectMetrics:
    total_modules: int = 0
    total_models: int = 0
    total_services: int = 0
    total_repositories: int = 0
    total_dtos: int = 0
    total_endpoints: int = 0
    total_test_files: int = 0
    total_test_functions: int = 0
    total_lines: int = 0
    total_classes: int = 0
    total_functions: int = 0
    total_todos: int = 0
    total_fixmes: int = 0
    modules: dict = field(default_factory=dict)


def count_lines(filepath: Path) -> int:
    try:
        content = filepath.read_text(encoding="utf-8")
        return len(content.split("\n"))
    except Exception:
        return 0


def count_patterns(filepath: Path, pattern: str) -> int:
    try:
        content = filepath.read_text(encoding="utf-8")
        return len(re.findall(pattern, content))
    except Exception:
        return 0


def analyze_module(module_name: str) -> ModuleMetrics:
    snake = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", module_name).lower()
    metrics = ModuleMetrics(name=module_name)

    # Model
    model_path = APP_DIR / "models" / f"{snake}.py"
    if model_path.exists():
        content = model_path.read_text(encoding="utf-8")
        metrics.model_fields = len(re.findall(r"(\w+):\s*Mapped\[", content))

    # Repository
    repo_path = APP_DIR / "repositories" / f"{snake}_repository.py"
    if repo_path.exists():
        content = repo_path.read_text(encoding="utf-8")
        metrics.repository_methods = len(re.findall(r"def\s+\w+", content))

    # Service
    service_path = APP_DIR / "services" / f"{snake}_service.py"
    if service_path.exists():
        content = service_path.read_text(encoding="utf-8")
        metrics.service_methods = len(re.findall(r"def\s+\w+", content))

    # DTOs
    schemas_dir = APP_DIR / "schemas" / snake
    if schemas_dir.exists():
        metrics.dto_count = len(list(schemas_dir.glob(f"{snake}_*.py")))

    # Validator
    validator_path = APP_DIR / "validators" / f"{snake}_validator.py"
    if validator_path.exists():
        content = validator_path.read_text(encoding="utf-8")
        metrics.validator_rules = len(re.findall(r"validate_\w+", content))

    # Error Codes
    errors_path = APP_DIR / "domain" / "errors" / f"{snake}_errors.py"
    if errors_path.exists():
        content = errors_path.read_text(encoding="utf-8")
        metrics.error_codes = len(re.findall(r"(\w+)\s*=\s*\"", content))

    # Endpoints
    router_path = APP_DIR / "api" / "routes" / f"{snake}.py"
    if router_path.exists():
        content = router_path.read_text(encoding="utf-8")
        metrics.endpoints = len(re.findall(r"@router\.(get|post|put|delete)", content))

    # Tests
    for test_type in ["unit", "integration", "contracts"]:
        test_dir = APP_DIR / "tests" / test_type
        if test_dir.exists():
            test_files = list(test_dir.glob(f"test_{snake}_*.py"))
            metrics.test_files += len(test_files)
            for tf in test_files:
                content = tf.read_text(encoding="utf-8")
                metrics.test_functions += len(re.findall(r"def\s+test_", content))

    return metrics


def collect_metrics() -> ProjectMetrics:
    metrics = ProjectMetrics()

    # Find modules by scanning models directory
    models_dir = APP_DIR / "models"
    if models_dir.exists():
        for f in models_dir.glob("*.py"):
            if f.name.startswith("_"):
                continue
            name = "".join(word.capitalize() for word in f.stem.split("_"))
            module_metrics = analyze_module(name)
            metrics.modules[name] = module_metrics

            metrics.total_models += 1
            metrics.total_services += 1 if module_metrics.service_methods > 0 else 0
            metrics.total_repositories += 1 if module_metrics.repository_methods > 0 else 0
            metrics.total_dtos += module_metrics.dto_count
            metrics.total_endpoints += module_metrics.endpoints
            metrics.total_test_files += module_metrics.test_files
            metrics.total_test_functions += module_metrics.test_functions

    # Count total lines, classes, functions across all Python files
    for filepath in APP_DIR.rglob("*.py"):
        if "__pycache__" in str(filepath):
            continue
        metrics.total_lines += count_lines(filepath)
        metrics.total_classes += count_patterns(filepath, r"^class\s+\w+", )
        metrics.total_functions += count_patterns(filepath, r"^def\s+\w+")
        metrics.total_todos += count_patterns(filepath, r"#\s*TODO")
        metrics.total_fixmes += count_patterns(filepath, r"#\s*FIXME")

    return metrics


def print_metrics(metrics: ProjectMetrics) -> None:
    print(f"\n{'='*60}")
    print(f"  Plantão 360 — Project Metrics")
    print(f"{'='*60}\n")

    print(f"  Modules:          {metrics.total_modules}")
    print(f"  Models:           {metrics.total_models}")
    print(f"  Services:         {metrics.total_services}")
    print(f"  Repositories:     {metrics.total_repositories}")
    print(f"  DTOs:             {metrics.total_dtos}")
    print(f"  Endpoints:        {metrics.total_endpoints}")
    print(f"  Test Files:       {metrics.total_test_files}")
    print(f"  Test Functions:   {metrics.total_test_functions}")
    print()
    print(f"  Total Lines:      {metrics.total_lines}")
    print(f"  Total Classes:    {metrics.total_classes}")
    print(f"  Total Functions:  {metrics.total_functions}")
    print(f"  TODOs:            {metrics.total_todos}")
    print(f"  FIXMEs:           {metrics.total_fixmes}")

    if metrics.modules:
        print(f"\n  {'─'*56}")
        print(f"  Module Breakdown:")
        print(f"  {'─'*56}")
        for name, m in metrics.modules.items():
            print(f"  {name:20s} │ Fields: {m.model_fields:2d} │ Endpoints: {m.endpoints:2d} │ Tests: {m.test_functions:2d}")

    print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Project metrics")
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()
    metrics = collect_metrics()
    metrics.total_modules = len(metrics.modules)

    if args.json:
        data = asdict(metrics)
        print(json.dumps(data, indent=2))
    else:
        print_metrics(metrics)


if __name__ == "__main__":
    main()
