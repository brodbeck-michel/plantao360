#!/usr/bin/env python3
"""
Architecture Linter V2 — Checks for architectural violations.

Uses manifests for module discovery and capability awareness.

Usage:
    python tools/lint_architecture.py
    python tools/lint_architecture.py --module Doctor
"""

import argparse
import ast
import io
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BACKEND_DIR = Path(__file__).parent.parent / "backend"
APP_DIR = BACKEND_DIR / "app"

sys.path.insert(0, str(Path(__file__).parent))
from manifest_loader import ManifestLoader


@dataclass
class LintViolation:
    file: str
    line: int
    rule: str
    message: str
    severity: str = "error"


@dataclass
class LintResult:
    violations: list[LintViolation] = field(default_factory=list)
    files_checked: int = 0

    @property
    def error_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for v in self.violations if v.severity == "warning")

    @property
    def passed(self) -> bool:
        return self.error_count == 0


def lint_file(filepath: Path) -> list[LintViolation]:
    violations = []
    try:
        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")
    except Exception:
        return violations

    rel_path = str(filepath.relative_to(BACKEND_DIR))

    # Rule: No SQLAlchemy in router files
    if "routes/" in rel_path:
        for i, line in enumerate(lines, 1):
            if re.search(r"from\s+sqlalchemy", line):
                if "sqlalchemy.orm" in line and "Session" in line:
                    continue
                violations.append(LintViolation(
                    file=rel_path, line=i, rule="no_sqlalchemy_in_router",
                    message="Router imports SQLAlchemy directly"
                ))

    # Rule: No business logic in router files
    if "routes/" in rel_path:
        in_handler = False
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if re.match(r"def\s+\w+\(", stripped):
                in_handler = True
            if in_handler:
                if re.match(r"\s+(if|try|except|for|while)\s+", line):
                    violations.append(LintViolation(
                        file=rel_path, line=i, rule="no_business_logic_in_router",
                        message="Router contains complex logic in handler",
                        severity="warning"
                    ))

    # Rule: No SQLAlchemy in service files
    if "services/" in rel_path:
        for i, line in enumerate(lines, 1):
            if re.search(r"from\s+sqlalchemy", line):
                violations.append(LintViolation(
                    file=rel_path, line=i, rule="no_sqlalchemy_in_service",
                    message="Service imports SQLAlchemy directly"
                ))

    # Rule: Service must use Repository Interface
    if "services/" in rel_path and rel_path.endswith("_service.py"):
        has_interface = bool(re.search(r"RepositoryInterface|Protocol", content))
        has_concrete = bool(re.search(r"from\s+app\.repositories\.\w+\s+import\s+\w+Repository(?!Interface)", content))
        if has_concrete and not has_interface:
            violations.append(LintViolation(
                file=rel_path, line=1, rule="service_uses_interface",
                message="Service imports concrete Repository instead of Interface"
            ))

    # Rule: Mapper must inherit BaseMapper
    if "mappers/" in rel_path and rel_path.endswith("_mapper.py") and "base_mapper" not in rel_path:
        has_base = bool(re.search(r"class\s+\w+Mapper\(BaseMapper", content))
        if not has_base:
            violations.append(LintViolation(
                file=rel_path, line=1, rule="mapper_inherits_basemapper",
                message="Mapper does not inherit BaseMapper"
            ))

    # Rule: No print statements
    for i, line in enumerate(lines, 1):
        if re.search(r"\bprint\s*\(", line) and not line.strip().startswith("#"):
            violations.append(LintViolation(
                file=rel_path, line=i, rule="no_print",
                message="print() statement found (use structured logging)"
            ))

    # Rule: Error codes must be used
    if "services/" in rel_path:
        if "Failure(" in content and "ErrorCode" not in content:
            violations.append(LintViolation(
                file=rel_path, line=1, rule="error_codes_used",
                message="Service uses Failure() without Error Codes",
                severity="warning"
            ))

    # Rule: Router must use ApiResponse
    if "routes/" in rel_path:
        if "return ApiResponse" not in content and "return {" in content:
            violations.append(LintViolation(
                file=rel_path, line=1, rule="router_uses_api_response",
                message="Router returns raw dict instead of ApiResponse",
                severity="warning"
            ))

    return violations


def lint_module_files(module_files: list[Path]) -> LintResult:
    result = LintResult()
    for filepath in module_files:
        result.files_checked += 1
        violations = lint_file(filepath)
        result.violations.extend(violations)
    return result


def find_module_files(storage_name: str, canonical_name: str) -> list[Path]:
    """Find all Python files for a module using manifest names."""
    module_files = []
    snake = canonical_name.lower()

    # Also try storage_name if different
    names_to_try = list(set([snake, storage_name]))

    for dirpath in [APP_DIR / "models", APP_DIR / "repositories", APP_DIR / "services",
                    APP_DIR / "mappers", APP_DIR / "validators", APP_DIR / "schemas",
                    APP_DIR / "api" / "routes", APP_DIR / "domain"]:
        if not dirpath.exists():
            continue
        for f in dirpath.rglob("*.py"):
            for name in names_to_try:
                if name in f.stem:
                    module_files.append(f)
                    break
    return module_files


def lint_all() -> LintResult:
    result = LintResult()
    for filepath in APP_DIR.rglob("*.py"):
        if "__pycache__" in str(filepath):
            continue
        result.files_checked += 1
        violations = lint_file(filepath)
        result.violations.extend(violations)
    return result


def print_results(result: LintResult, module: str = "All") -> None:
    print(f"\n{'='*60}")
    print(f"  Architecture Lint V2 — {module}")
    print(f"{'='*60}\n")

    if not result.violations:
        print("  ✓ No violations found!")
    else:
        for v in result.violations:
            icon = "✗" if v.severity == "error" else "!"
            print(f"  {icon} [{v.rule}] {v.file}:{v.line}")
            print(f"    {v.message}")
            print()

    print(f"{'='*60}")
    print(f"  Files checked: {result.files_checked}")
    print(f"  Errors: {result.error_count}")
    print(f"  Warnings: {result.warning_count}")
    print(f"  Status: {'✓ PASS' if result.passed else '✗ FAIL'}")
    print(f"{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description="Architecture linter V2")
    parser.add_argument("--module", "-m", help="Module to lint (canonical or storage)")
    parser.add_argument("--all", action="store_true", help="Lint all files")
    args = parser.parse_args()

    if args.module:
        loader = ManifestLoader()
        manifest = loader.get_by_canonical_name(args.module)
        if not manifest:
            manifest = loader.get_by_storage_name(args.module)
        if not manifest:
            manifest = loader.get(args.module.lower())

        if manifest:
            files = find_module_files(manifest.storage_name, manifest.canonical_name)
            result = lint_module_files(files)
            print_results(result, manifest.canonical_name)
        else:
            print(f"  ERROR: No manifest found for '{args.module}'")
            sys.exit(1)
    else:
        result = lint_all()
        print_results(result)

    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
