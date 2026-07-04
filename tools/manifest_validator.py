#!/usr/bin/env python3
"""
Manifest Validator — Independent validation of Module Manifests.

Validates schema, version, required fields, coherence, ADR references,
and uniqueness of module_id across all manifests.

Usage:
    python tools/manifest_validator.py
    python tools/manifest_validator.py --manifest doctor
    python tools/manifest_validator.py --validate-all
"""

import argparse
import sys
from pathlib import Path
from dataclasses import dataclass, field

import yaml

ARCHITECTURE_DIR = Path(__file__).parent.parent / "backend" / "architecture"
MANIFESTS_DIR = ARCHITECTURE_DIR / "manifests"
SCHEMA_PATH = ARCHITECTURE_DIR / "manifest_schema.yaml"

SUPPORTED_MANIFEST_VERSIONS = [1]


def _setup_encoding():
    """Setup encoding for standalone execution."""
    import io
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if sys.stderr.encoding != 'utf-8':
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


@dataclass
class ValidationError:
    manifest: str
    field: str
    message: str
    severity: str = "error"


@dataclass
class ValidationResult:
    manifest: str
    passed: list[str] = field(default_factory=list)
    errors: list[ValidationError] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0

    @property
    def score(self) -> float:
        total = len(self.passed) + len(self.errors)
        if total == 0:
            return 0.0
        return len(self.passed) / total * 100


def load_yaml(path: Path) -> dict | None:
    try:
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        return None


def validate_manifest_version(data: dict, manifest_name: str) -> list[ValidationError]:
    errors = []
    if "manifest_version" not in data:
        errors.append(ValidationError(
            manifest=manifest_name, field="manifest_version",
            message="Required field 'manifest_version' is missing"
        ))
    else:
        version = data["manifest_version"]
        if version not in SUPPORTED_MANIFEST_VERSIONS:
            errors.append(ValidationError(
                manifest=manifest_name, field="manifest_version",
                message=f"Unsupported manifest_version: {version}. Supported: {SUPPORTED_MANIFEST_VERSIONS}"
            ))
    return errors


def validate_required_fields(data: dict, manifest_name: str) -> list[ValidationError]:
    errors = []
    required_top = ["module_id", "module", "ownership", "stability", "lifecycle", "capabilities", "validation_profile"]
    for field_name in required_top:
        if field_name not in data:
            errors.append(ValidationError(
                manifest=manifest_name, field=field_name,
                message=f"Required field '{field_name}' is missing"
            ))

    if "module" in data:
        module = data["module"]
        for field_name in ["canonical_name", "storage_name", "storage_table"]:
            if field_name not in module:
                errors.append(ValidationError(
                    manifest=manifest_name, field=f"module.{field_name}",
                    message=f"Required field 'module.{field_name}' is missing"
                ))

    if "ownership" in data:
        ownership = data["ownership"]
        for field_name in ["aggregate", "bounded_context"]:
            if field_name not in ownership:
                errors.append(ValidationError(
                    manifest=manifest_name, field=f"ownership.{field_name}",
                    message=f"Required field 'ownership.{field_name}' is missing"
                ))

    if "stability" in data:
        stability = data["stability"]
        for field_name in ["level", "since", "adr"]:
            if field_name not in stability:
                errors.append(ValidationError(
                    manifest=manifest_name, field=f"stability.{field_name}",
                    message=f"Required field 'stability.{field_name}' is missing"
                ))

    if "lifecycle" in data:
        lifecycle = data["lifecycle"]
        for field_name in ["states", "initial_state", "terminal_states"]:
            if field_name not in lifecycle:
                errors.append(ValidationError(
                    manifest=manifest_name, field=f"lifecycle.{field_name}",
                    message=f"Required field 'lifecycle.{field_name}' is missing"
                ))

    if "capabilities" in data:
        caps = data["capabilities"]
        required_caps = ["model", "repository", "repository_interface", "service", "router"]
        for cap in required_caps:
            if cap not in caps:
                errors.append(ValidationError(
                    manifest=manifest_name, field=f"capabilities.{cap}",
                    message=f"Required capability '{cap}' is missing"
                ))
        if "dtos" not in caps:
            errors.append(ValidationError(
                manifest=manifest_name, field="capabilities.dtos",
                message="Required capability 'capabilities.dtos' is missing"
            ))
        if "tests" not in caps:
            errors.append(ValidationError(
                manifest=manifest_name, field="capabilities.tests",
                message="Required capability 'capabilities.tests' is missing"
            ))

    return errors


def validate_coherence(data: dict, manifest_name: str) -> list[ValidationError]:
    errors = []
    if "lifecycle" in data:
        lifecycle = data["lifecycle"]
        states = lifecycle.get("states", [])
        initial = lifecycle.get("initial_state")
        terminals = lifecycle.get("terminal_states", [])

        if initial and initial not in states:
            errors.append(ValidationError(
                manifest=manifest_name, field="lifecycle.initial_state",
                message=f"initial_state '{initial}' is not in states list"
            ))
        for t in terminals:
            if t not in states:
                errors.append(ValidationError(
                    manifest=manifest_name, field="lifecycle.terminal_states",
                    message=f"terminal_state '{t}' is not in states list"
                ))

    if "stability" in data:
        level = data["stability"].get("level", "")
        valid_levels = ["experimental", "stable", "frozen"]
        if level not in valid_levels:
            errors.append(ValidationError(
                manifest=manifest_name, field="stability.level",
                message=f"Invalid stability level '{level}'. Must be one of: {valid_levels}"
            ))

    if "module_id" in data:
        module_id = data["module_id"]
        if not isinstance(module_id, str) or "." not in module_id:
            errors.append(ValidationError(
                manifest=manifest_name, field="module_id",
                message=f"module_id must be a string with '.' separator (e.g., scheduling.assignment)"
            ))

    return errors


def validate_adr_references(data: dict, manifest_name: str) -> list[ValidationError]:
    errors = []
    adr_refs = data.get("adr_references", [])
    for ref in adr_refs:
        if "id" not in ref:
            errors.append(ValidationError(
                manifest=manifest_name, field="adr_references",
                message="ADR reference missing 'id' field"
            ))
        if "title" not in ref:
            errors.append(ValidationError(
                manifest=manifest_name, field="adr_references",
                message=f"ADR reference '{ref.get('id', '?')}' missing 'title' field"
            ))
    return errors


def validate_manifest_file(path: Path) -> ValidationResult:
    manifest_name = path.stem
    result = ValidationResult(manifest=manifest_name)

    data = load_yaml(path)
    if data is None:
        result.errors.append(ValidationError(
            manifest=manifest_name, field="yaml",
            message=f"Failed to parse YAML: {path}"
        ))
        return result

    result.passed.append(f"YAML parsed successfully")

    errors = validate_manifest_version(data, manifest_name)
    result.errors.extend(errors)
    if not errors:
        result.passed.append(f"Version supported: {data.get('manifest_version')}")

    errors = validate_required_fields(data, manifest_name)
    result.errors.extend(errors)
    if not errors:
        result.passed.append("All required fields present")

    errors = validate_coherence(data, manifest_name)
    result.errors.extend(errors)
    if not errors:
        result.passed.append("Coherence checks passed")

    errors = validate_adr_references(data, manifest_name)
    result.errors.extend(errors)
    if not errors:
        result.passed.append("ADR references valid")

    return result


def validate_uniqueness(all_results: list[ValidationResult], all_data: dict[str, dict]) -> list[str]:
    warnings = []
    module_ids = {}
    canonical_names = {}

    for name, data in all_data.items():
        mid = data.get("module_id")
        if mid:
            if mid in module_ids:
                warnings.append(f"Duplicate module_id '{mid}' in manifests: {module_ids[mid]} and {name}")
            module_ids[mid] = name

        cn = data.get("module", {}).get("canonical_name")
        if cn:
            if cn in canonical_names:
                warnings.append(f"Duplicate canonical_name '{cn}' in manifests: {canonical_names[cn]} and {name}")
            canonical_names[cn] = name

    return warnings


def main():
    _setup_encoding()
    parser = argparse.ArgumentParser(description="Validate Module Manifests")
    parser.add_argument("--manifest", "-m", help="Validate a specific manifest")
    parser.add_argument("--validate-all", action="store_true", help="Validate all manifests")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  Manifest Validator — Plantão 360")
    print(f"{'='*60}\n")

    if not MANIFESTS_DIR.exists():
        print(f"  ERROR: Manifests directory not found: {MANIFESTS_DIR}")
        sys.exit(1)

    manifest_files = sorted(MANIFESTS_DIR.glob("*.yaml"))
    if not manifest_files:
        print(f"  No manifests found in {MANIFESTS_DIR}")
        sys.exit(1)

    all_data = {}
    all_results = []

    for mf in manifest_files:
        data = load_yaml(mf)
        if data:
            all_data[mf.stem] = data

    for mf in manifest_files:
        if args.manifest and mf.stem != args.manifest:
            continue
        result = validate_manifest_file(mf)
        all_results.append(result)

        status = "PASS" if result.is_valid else "FAIL"
        print(f"  [{status}] {mf.stem} — {result.score:.1f}%")
        for msg in result.passed:
            print(f"    + {msg}")
        for err in result.errors:
            print(f"    x [{err.field}] {err.message}")
        for warn in result.warnings:
            print(f"    ! {warn}")

    # Uniqueness check across manifests
    if len(all_data) > 1:
        uniqueness_warnings = validate_uniqueness(all_results, all_data)
        for w in uniqueness_warnings:
            print(f"    ! {w}")

    # Summary
    total_passed = sum(len(r.passed) for r in all_results)
    total_errors = sum(len(r.errors) for r in all_results)
    all_valid = all(r.is_valid for r in all_results)

    print(f"\n{'='*60}")
    print(f"  Summary")
    print(f"  Manifests validated: {len(all_results)}")
    print(f"  Passed: {total_passed}")
    print(f"  Errors: {total_errors}")
    print(f"  Status: {'ALL VALID' if all_valid else 'VALIDATION ERRORS'}")
    print(f"{'='*60}\n")

    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()
