#!/usr/bin/env python3
"""
Architecture Validator V2 — Validates modules against their manifests.

Validates architectural CAPABILITIES, not naming conventions.
Uses Module Manifests as the source of truth.

Usage:
    python tools/validate_architecture.py Doctor
    python tools/validate_architecture.py --all
    python tools/validate_architecture.py --list
"""

import argparse
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
from manifest_loader import ManifestLoader, ModuleManifest


@dataclass
class ValidationResult:
    module: str
    manifest_id: str = ""
    passed: list[str] = field(default_factory=list)
    failed: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def score(self) -> float:
        total = len(self.passed) + len(self.failed)
        if total == 0:
            return 0.0
        return len(self.passed) / total * 100

    @property
    def is_valid(self) -> bool:
        return len(self.failed) == 0


def check_file_exists(path: Path, description: str, result: ValidationResult) -> bool:
    if path.exists():
        result.passed.append(f"  + {description}: {path.name}")
        return True
    else:
        result.failed.append(f"  x {description}: not found at {path}")
        return False


def check_file_contains(path: Path, pattern: str, description: str, result: ValidationResult) -> bool:
    if not path.exists():
        result.failed.append(f"  x {description}: file not found")
        return False
    content = path.read_text(encoding="utf-8")
    if re.search(pattern, content):
        result.passed.append(f"  + {description}")
        return True
    else:
        result.failed.append(f"  x {description}: pattern not found")
        return False


def validate_capabilities(manifest: ModuleManifest) -> ValidationResult:
    """Validate a module based on its manifest capabilities."""
    result = ValidationResult(
        module=manifest.canonical_name,
        manifest_id=manifest.module_id
    )
    resolved = manifest.resolve_files()

    # Validate declared capabilities
    for cap_name, resolved_path in resolved.items():
        if resolved_path.exists:
            result.passed.append(f"  + {cap_name}: exists ({resolved_path.path.name})")
        else:
            result.failed.append(f"  x {cap_name}: declared but not found at {resolved_path.path}")

    # Validate service patterns
    if manifest.has_capability("service") and "service" in resolved:
        service_path = resolved["service"].path
        if service_path.exists():
            content = service_path.read_text(encoding="utf-8")
            if "UnitOfWork" in content:
                result.passed.append("  + service_uses_uow")
            else:
                result.failed.append("  x service_uses_uow: UnitOfWork not found")
            if "Success" in content and "Failure" in content:
                result.passed.append("  + service_uses_result_pattern")
            else:
                result.failed.append("  x service_uses_result_pattern")
            if "ErrorCode" in content:
                result.passed.append("  + service_uses_error_codes")
            else:
                result.failed.append("  x service_uses_error_codes")
            if "EventDispatcher" in content:
                result.passed.append("  + service_uses_event_dispatcher")
            else:
                result.failed.append("  x service_uses_event_dispatcher")

    # Validate mapper pattern
    if manifest.has_capability("mapper") and "mapper" in resolved:
        mapper_path = resolved["mapper"].path
        if mapper_path.exists():
            content = mapper_path.read_text(encoding="utf-8")
            if "BaseMapper" in content:
                result.passed.append("  + mapper_inherits_basemapper")
            else:
                result.failed.append("  x mapper_inherits_basemapper")

    # Validate router patterns
    if manifest.has_capability("router") and "router" in resolved:
        router_path = resolved["router"].path
        if router_path.exists():
            content = router_path.read_text(encoding="utf-8")
            if "ApiResponse" in content:
                result.passed.append("  + router_uses_api_response")
            else:
                result.failed.append("  x router_uses_api_response")
            if "X-Total-Count" in content:
                result.passed.append("  + router_has_pagination_headers")
            else:
                result.failed.append("  x router_has_pagination_headers")
            # Check no SQLAlchemy imports (except Session)
            lines = content.split("\n")
            has_forbidden = False
            for line in lines:
                if re.search(r"from\s+sqlalchemy", line):
                    if "sqlalchemy.orm" in line and "Session" in line:
                        continue
                    has_forbidden = True
                    break
            if not has_forbidden:
                result.passed.append("  + router_no_sqlalchemy_imports")
            else:
                result.failed.append("  x router_no_sqlalchemy_imports")

    # Validate state machine if declared
    if manifest.has_capability("state_machine"):
        sm_files = list(APP_DIR.rglob(f"*{manifest.storage_name}*state_machine*.py"))
        if not sm_files:
            # Try canonical name
            sm_files = list(APP_DIR.rglob(f"*{manifest.canonical_name.lower()}*state_machine*.py"))
        if sm_files:
            result.passed.append("  + state_machine_exists")
        else:
            result.failed.append("  x state_machine_exists: declared but not found")

    # Validate policy if declared
    if manifest.has_capability("policy"):
        policy_files = list(APP_DIR.rglob(f"*{manifest.storage_name}*policy*.py"))
        if not policy_files:
            policy_files = list(APP_DIR.rglob(f"*{manifest.canonical_name.lower()}*policy*.py"))
        if policy_files:
            result.passed.append("  + policy_exists")
        else:
            result.failed.append("  x policy_exists: declared but not found")

    # Validate events if declared
    if manifest.has_capability("events"):
        events_path = APP_DIR / "domain" / "events" / "event_names.py"
        if events_path.exists():
            content = events_path.read_text(encoding="utf-8")
            # Check if module has events registered
            module_lower = manifest.canonical_name.lower()
            if module_lower in content.lower():
                result.passed.append("  + events_registered")
            else:
                result.warnings.append(f"  ! events_registered: no events found for {manifest.canonical_name}")
        else:
            result.failed.append("  x events_registered: event_names.py not found")

    # Validate test coverage
    for test_type in ["unit", "integration", "contracts"]:
        if manifest.has_capability(f"tests.{test_type}"):
            test_dir = APP_DIR / "tests" / test_type
            if test_dir.exists():
                snake = manifest._resolve_storage_name()
                canonical = manifest.canonical_name.lower()
                # Try both storage name and canonical name
                test_files = list(test_dir.glob(f"test_{snake}_*.py"))
                if not test_files and canonical != snake:
                    test_files = list(test_dir.glob(f"test_{canonical}_*.py"))
                if test_files:
                    result.passed.append(f"  + test_{test_type}: {len(test_files)} file(s)")
                else:
                    result.failed.append(f"  x test_{test_type}: declared but no test files found")
            else:
                result.failed.append(f"  x test_{test_type}: directory not found")

    return result


def validate_module(module_name: str, loader: ManifestLoader) -> ValidationResult:
    """Validate a module by name (canonical or storage)."""
    manifest = loader.get_by_canonical_name(module_name)
    if not manifest:
        manifest = loader.get_by_storage_name(module_name)
    if not manifest:
        manifest = loader.get(module_name.lower())

    if not manifest:
        result = ValidationResult(module=module_name)
        result.failed.append(f"  x No manifest found for '{module_name}'")
        return result

    return validate_capabilities(manifest)


def main():
    parser = argparse.ArgumentParser(description="Architecture Validator V2 — Manifest-driven")
    parser.add_argument("module", nargs="?", help="Module name (canonical or storage)")
    parser.add_argument("--all", action="store_true", help="Validate all modules")
    parser.add_argument("--list", action="store_true", help="List discovered modules")
    parser.add_argument("--fix-suggestions", action="store_true", help="Show fix suggestions")

    args = parser.parse_args()

    loader = ManifestLoader()

    if args.list:
        modules = loader.discover()
        print(f"\n  Discovered modules ({len(modules)}):")
        for m in modules:
            manifest = loader.get(m)
            if manifest:
                print(f"    - {manifest.canonical_name} ({manifest.module_id})")
        sys.exit(0)

    print(f"\n{'='*60}")
    print(f"  Architecture Validator V2 — Plantão 360")
    print(f"{'='*60}\n")

    if args.all:
        modules = loader.discover()
        if not modules:
            print("  No modules found.")
            sys.exit(1)
        results = []
        for mod_name in modules:
            manifest = loader.get(mod_name)
            if manifest:
                results.append(validate_capabilities(manifest))

        # Summary
        total_passed = sum(len(r.passed) for r in results)
        total_failed = sum(len(r.failed) for r in results)
        total_warnings = sum(len(r.warnings) for r in results)
        avg_score = sum(r.score for r in results) / len(results) if results else 0

        for r in results:
            status = "PASS" if r.is_valid else "FAIL"
            print(f"  [{status}] {r.module} ({r.manifest_id}) — {r.score:.1f}%")
            if not r.is_valid:
                for msg in r.failed:
                    print(f"    {msg}")

        print(f"\n{'='*60}")
        print(f"  ARCHITECTURE VALIDATION SUMMARY")
        print(f"{'='*60}")
        print(f"  Modules validated: {len(results)}")
        print(f"  Total checks: {total_passed + total_failed}")
        print(f"  Passed: {total_passed}")
        print(f"  Failed: {total_failed}")
        print(f"  Warnings: {total_warnings}")
        print(f"  Average Score: {avg_score:.1f}%")
        all_valid = all(r.is_valid for r in results)
        print(f"  Overall: {'ALL PASS' if all_valid else 'SOME FAILURES'}")
        print(f"{'='*60}\n")

        sys.exit(0 if all_valid else 1)

    elif args.module:
        result = validate_module(args.module, loader)
        status = "PASS" if result.is_valid else "FAIL"
        print(f"  [{status}] {result.module} ({result.manifest_id}) — {result.score:.1f}%")
        for msg in result.passed:
            print(f"  {msg}")
        for msg in result.failed:
            print(f"  {msg}")
        for msg in result.warnings:
            print(f"  {msg}")
        sys.exit(0 if result.is_valid else 1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
