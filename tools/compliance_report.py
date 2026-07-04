#!/usr/bin/env python3
"""
Compliance Report V2 — Generates compliance checklist for each module.

Uses manifests as the source of truth.

Usage:
    python tools/compliance_report.py
    python tools/compliance_report.py --module Doctor
"""

import argparse
import io
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BACKEND_DIR = Path(__file__).parent.parent / "backend"
APP_DIR = BACKEND_DIR / "app"
DOCS_DIR = Path(__file__).parent.parent / "docs"

sys.path.insert(0, str(Path(__file__).parent))
from manifest_loader import ManifestLoader, ModuleManifest


def check_item(path: Path, description: str) -> str:
    if path.exists():
        return f"| {description} | ✓ | `{path.name}` |"
    return f"| {description} | ✗ | Missing |"


def check_content(path: Path, pattern: str, description: str) -> str:
    if not path.exists():
        return f"| {description} | ✗ | File not found |"
    content = path.read_text(encoding="utf-8")
    if re.search(pattern, content):
        return f"| {description} | ✓ | - |"
    return f"| {description} | ✗ | Pattern not found |"


def generate_compliance_from_manifest(manifest: ModuleManifest) -> str:
    """Generate compliance report from manifest capabilities."""
    resolved = manifest.resolve_files()
    rows = []
    rows.append(f"| **Component** | **Status** | **Details** |")
    rows.append(f"|---|---|---|")

    # Model
    if manifest.has_capability("model") and "model" in resolved:
        rows.append(check_item(resolved["model"].path, "Model"))

    # Repository Interface
    if manifest.has_capability("repository_interface") and "repository_interface" in resolved:
        rows.append(check_item(resolved["repository_interface"].path, "Repository Interface"))

    # Repository
    if manifest.has_capability("repository") and "repository" in resolved:
        rows.append(check_item(resolved["repository"].path, "Repository"))

    # Service
    if manifest.has_capability("service") and "service" in resolved:
        rows.append(check_item(resolved["service"].path, "Service"))

    # Mapper
    if manifest.has_capability("mapper") and "mapper" in resolved:
        rows.append(check_item(resolved["mapper"].path, "Mapper"))
        if resolved["mapper"].exists:
            rows.append(check_content(resolved["mapper"].path, r"class\s+\w+Mapper\(BaseMapper", "Mapper inherits BaseMapper"))

    # Validator
    if manifest.has_capability("validator") and "validator" in resolved:
        rows.append(check_item(resolved["validator"].path, "Validator"))

    # DTOs
    dtos = manifest.data.get("capabilities", {}).get("dtos", {})
    snake = manifest._resolve_storage_name()
    schemas_dir = APP_DIR / "schemas" / snake
    for dto_type, enabled in dtos.items():
        if enabled:
            dto_path = schemas_dir / f"{snake}_{dto_type}.py"
            rows.append(check_item(dto_path, f"DTO ({dto_type})"))

    # Error Codes
    errors_path = APP_DIR / "domain" / "errors" / f"{snake}_errors.py"
    rows.append(check_item(errors_path, "Error Codes"))

    # Router
    if manifest.has_capability("router") and "router" in resolved:
        rows.append(check_item(resolved["router"].path, "Router"))
        if resolved["router"].exists:
            rows.append(check_content(resolved["router"].path, r"ApiResponse", "Router uses ApiResponse"))
            rows.append(check_content(resolved["router"].path, r"X-Total-Count", "Router has pagination headers"))

    # Service patterns
    if manifest.has_capability("service") and "service" in resolved and resolved["service"].exists:
        rows.append(check_content(resolved["service"].path, r"ErrorCode", "Service uses Error Codes"))
        rows.append(check_content(resolved["service"].path, r"\.v1", "Service uses event versioning"))

    # State Machine
    if manifest.has_capability("state_machine"):
        sm_path = APP_DIR / "domain" / "state_machines" / f"{snake}_state_machine.py"
        if not sm_path.exists():
            sm_path = APP_DIR / "domain" / "state_machines" / f"{manifest.canonical_name.lower()}_state_machine.py"
        rows.append(check_item(sm_path, "State Machine"))

    # Policy
    if manifest.has_capability("policy"):
        policy_path = APP_DIR / "domain" / "policies" / f"{snake}_policy.py"
        if not policy_path.exists():
            policy_path = APP_DIR / "domain" / "policies" / f"{manifest.canonical_name.lower()}_policy.py"
        rows.append(check_item(policy_path, "Policy"))

    # Tests
    for test_type in ["unit", "integration", "contracts"]:
        if manifest.has_capability(f"tests.{test_type}"):
            test_dir = APP_DIR / "tests" / test_type
            if test_dir.exists():
                test_files = list(test_dir.glob(f"test_{snake}_*.py"))
                if test_files:
                    rows.append(f"| Tests ({test_type}) | ✓ | {len(test_files)} file(s) |")
                else:
                    rows.append(f"| Tests ({test_type}) | ✗ | No test files |")
            else:
                rows.append(f"| Tests ({test_type}) | ✗ | Directory not found |")

    # Documentation
    docs_path = DOCS_DIR / "modules" / f"{snake}-module.md"
    rows.append(check_item(docs_path, "Documentation"))

    # Summary
    passed = sum(1 for r in rows if "✓" in r)
    failed = sum(1 for r in rows if "✗" in r)
    total = passed + failed

    report = f"""# Module Compliance Report: {manifest.canonical_name}

**Generated:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}
**Module ID:** {manifest.module_id}
**Storage:** {manifest.storage_name} ({manifest.storage_table})
**Validation Profile:** {manifest.validation_profile}

---

{chr(10).join(rows)}

---

## Summary

| Metric | Value |
|--------|-------|
| Module | {manifest.canonical_name} |
| Table | {manifest.storage_table} |
| Components Checked | {total} |
| Passed | {passed} |
| Failed | {failed} |
| Compliance | {passed/total*100:.1f}% |
"""
    return report


def main():
    parser = argparse.ArgumentParser(description="Generate module compliance report (V2)")
    parser.add_argument("--module", "-m", help="Module name (canonical or storage)")
    parser.add_argument("--all", action="store_true", help="Generate for all modules")
    args = parser.parse_args()

    loader = ManifestLoader()

    if args.module:
        manifest = loader.get_by_canonical_name(args.module)
        if not manifest:
            manifest = loader.get_by_storage_name(args.module)
        if not manifest:
            manifest = loader.get(args.module.lower())
        if not manifest:
            print(f"  ERROR: No manifest found for '{args.module}'")
            sys.exit(1)
        report = generate_compliance_from_manifest(manifest)
        snake = manifest._resolve_storage_name()
        output_path = DOCS_DIR / "reports" / f"compliance-{snake}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(f"  ✓ Report generated: {output_path.relative_to(DOCS_DIR.parent)}")

    elif args.all:
        for name in loader.discover():
            manifest = loader.get(name)
            if manifest:
                report = generate_compliance_from_manifest(manifest)
                snake = manifest._resolve_storage_name()
                output_path = DOCS_DIR / "reports" / f"compliance-{snake}.md"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(report, encoding="utf-8")
                print(f"  ✓ {manifest.canonical_name}: {output_path.relative_to(DOCS_DIR.parent)}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
