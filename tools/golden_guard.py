#!/usr/bin/env python3
"""
Golden Guard V2 — Compares all modules against the Golden Module (Doctor).

Uses manifests for comparison. Compares RESPONSIBILITIES, not file names.
Each module is compared against the Doctor manifest's capabilities.

Usage:
    python tools/golden_guard.py
    python tools/golden_guard.py --module Period
    python tools/golden_guard.py --strict
"""

import argparse
import io
import sys
from pathlib import Path
from dataclasses import dataclass, field

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

sys.path.insert(0, str(Path(__file__).parent))
from manifest_loader import ManifestLoader, ModuleManifest

GOLDEN_MODULE_NAME = "doctor"


@dataclass
class GoldenCheck:
    name: str
    expected: bool
    actual: bool
    passed: bool
    details: str = ""


@dataclass
class GoldenReport:
    module: str
    manifest_id: str = ""
    checks: list[GoldenCheck] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return all(c.passed for c in self.checks)

    @property
    def score(self) -> float:
        if not self.checks:
            return 0.0
        return sum(1 for c in self.checks if c.passed) / len(self.checks) * 100


def compare_capabilities(golden: ModuleManifest, module: ModuleManifest) -> list[GoldenCheck]:
    """Compare module capabilities against golden module."""
    checks = []

    # Core capabilities
    core_caps = ["model", "repository", "repository_interface", "service",
                 "mapper", "validator", "router"]
    for cap in core_caps:
        golden_has = golden.has_capability(cap)
        module_has = module.has_capability(cap)
        checks.append(GoldenCheck(
            name=f"capability_{cap}",
            expected=golden_has,
            actual=module_has,
            passed=module_has >= golden_has,  # Module must have at least what golden has
            details=f"Golden: {golden_has}, Module: {module_has}"
        ))

    # Domain capabilities
    domain_caps = ["state_machine", "policy", "events", "contracts", "value_objects"]
    for cap in domain_caps:
        golden_has = golden.has_capability(cap)
        module_has = module.has_capability(cap)
        # Domain capabilities: golden is the standard; module should match or exceed
        # But some modules legitimately don't need all domain capabilities
        if golden_has:
            checks.append(GoldenCheck(
                name=f"domain_{cap}",
                expected=True,
                actual=module_has,
                passed=module_has,
                details=f"Golden has {cap}, Module should too"
            ))

    # DTOs
    golden_dtos = golden.data.get("capabilities", {}).get("dtos", {})
    module_dtos = module.data.get("capabilities", {}).get("dtos", {})
    for dto_type in ["create", "update", "response", "filters", "query"]:
        golden_has = golden_dtos.get(dto_type, False)
        module_has = module_dtos.get(dto_type, False)
        checks.append(GoldenCheck(
            name=f"dto_{dto_type}",
            expected=golden_has,
            actual=module_has,
            passed=module_has >= golden_has,
            details=f"Golden: {golden_has}, Module: {module_has}"
        ))

    # Tests
    golden_tests = golden.data.get("capabilities", {}).get("tests", {})
    module_tests = module.data.get("capabilities", {}).get("tests", {})
    for test_type in ["unit", "integration", "contracts"]:
        golden_has = golden_tests.get(test_type, False)
        module_has = module_tests.get(test_type, False)
        checks.append(GoldenCheck(
            name=f"test_{test_type}",
            expected=golden_has,
            actual=module_has,
            passed=module_has >= golden_has,
            details=f"Golden: {golden_has}, Module: {module_has}"
        ))

    # Validation profile
    golden_profile = golden.validation_profile
    module_profile = module.validation_profile
    checks.append(GoldenCheck(
        name="validation_profile",
        expected=True,
        actual=module_profile == golden_profile,
        passed=module_profile == golden_profile,
        details=f"Golden: {golden_profile}, Module: {module_profile}"
    ))

    return checks


def validate_module_module(module_name: str, golden: ModuleManifest, loader: ManifestLoader) -> GoldenReport:
    """Validate a module against the golden module."""
    manifest = loader.get_by_canonical_name(module_name)
    if not manifest:
        manifest = loader.get_by_storage_name(module_name)
    if not manifest:
        manifest = loader.get(module_name.lower())

    if not manifest:
        return GoldenReport(module=module_name, checks=[
            GoldenCheck(name="manifest_exists", expected=True, actual=False, passed=False)
        ])

    report = GoldenReport(module=manifest.canonical_name, manifest_id=manifest.module_id)
    report.checks = compare_capabilities(golden, manifest)
    return report


def main():
    parser = argparse.ArgumentParser(description="Golden Guard V2 — Manifest-driven compliance")
    parser.add_argument("module", nargs="?", help="Module to validate")
    parser.add_argument("--all", action="store_true", help="Validate all modules")
    parser.add_argument("--strict", action="store_true", help="Strict mode")
    args = parser.parse_args()

    loader = ManifestLoader()
    golden = loader.get(GOLDEN_MODULE_NAME)

    if not golden:
        print("  ERROR: Golden module (doctor) manifest not found!")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  Golden Guard V2 — Plantão 360")
    print(f"  Golden Module: {golden.canonical_name} ({golden.module_id})")
    print(f"{'='*60}\n")

    modules_to_check = []
    if args.module:
        modules_to_check = [args.module]
    else:
        modules_to_check = [m for m in loader.discover() if m != GOLDEN_MODULE_NAME]

    all_reports = []
    for mod in modules_to_check:
        report = validate_module_module(mod, golden, loader)
        all_reports.append(report)

        status = "PASS" if report.passed else "FAIL"
        print(f"  [{status}] {report.module} ({report.manifest_id}) — {report.score:.1f}%")
        if not report.passed:
            for check in report.checks:
                if not check.passed:
                    print(f"    FAIL: {check.name} ({check.details})")

    # Summary
    total_checks = sum(len(r.checks) for r in all_reports)
    total_passed = sum(1 for r in all_reports for c in r.checks if c.passed)
    all_valid = all(r.passed for r in all_reports)

    print(f"\n{'='*60}")
    print(f"  Summary")
    print(f"  Modules checked: {len(all_reports)}")
    print(f"  Total checks: {total_checks}")
    print(f"  Passed: {total_passed}")
    print(f"  Failed: {total_checks - total_passed}")
    print(f"  Overall: {'ALL PASS' if all_valid else 'SOME FAILURES'}")
    print(f"{'='*60}\n")

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
