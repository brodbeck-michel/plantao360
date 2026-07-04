#!/usr/bin/env python3
"""
Release Readiness — Validates all release criteria.

Usage:
    python tools/release_readiness.py
"""

import io
import subprocess
import sys
import time
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

TOOLS_DIR = Path(__file__).parent
BACKEND_DIR = TOOLS_DIR.parent / "backend"


def run_check(name: str, command: list[str]) -> dict:
    start = time.time()
    try:
        result = subprocess.run(
            command,
            cwd=str(BACKEND_DIR),
            capture_output=True,
            text=True,
            timeout=120
        )
        elapsed = time.time() - start
        return {
            "name": name,
            "passed": result.returncode == 0,
            "time": round(elapsed, 2),
            "output": result.stdout[-500:] if result.stdout else "",
            "error": result.stderr[-500:] if result.stderr else ""
        }
    except subprocess.TimeoutExpired:
        return {"name": name, "passed": False, "time": 120, "error": "Timeout"}
    except Exception as e:
        return {"name": name, "passed": False, "time": 0, "error": str(e)}


def main():
    print(f"\n{'='*60}")
    print(f"  Release Readiness — Plantão 360")
    print(f"{'='*60}\n")

    checks = [
        ("Architecture Validator", [sys.executable, str(TOOLS_DIR / "validate_architecture.py"), "--all"]),
        ("Architecture Linter", [sys.executable, str(TOOLS_DIR / "lint_architecture.py")]),
        ("Golden Guard", [sys.executable, str(TOOLS_DIR / "golden_guard.py")]),
        ("Template Consistency", [sys.executable, str(TOOLS_DIR / "check_templates.py")]),
        ("ADR Validator", [sys.executable, str(TOOLS_DIR / "check_adrs.py")]),
        ("Compliance Report", [sys.executable, str(TOOLS_DIR / "compliance_report.py"), "--all"]),
        ("Architecture Score", [sys.executable, str(TOOLS_DIR / "architecture_score.py")]),
        ("Technical Debt", [sys.executable, str(TOOLS_DIR / "technical_debt.py")]),
        ("Dependency Check", [sys.executable, str(TOOLS_DIR / "check_dependencies.py")]),
        ("Pytest", [sys.executable, "-m", "pytest", "app/tests/", "-v", "--tb=short", "--override-ini=addopts=-v --tb=short"]),
    ]

    results = []
    all_passed = True
    for name, cmd in checks:
        print(f"  Running: {name}...", end=" ", flush=True)
        result = run_check(name, cmd)
        results.append(result)
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] ({result['time']}s)")
        if not result["passed"]:
            all_passed = False

    print(f"\n{'='*60}")
    print(f"  RESULTS")
    print(f"{'='*60}")
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  [{status}] {r['name']:30s} ({r['time']}s)")

    total_time = sum(r["time"] for r in results)
    passed = sum(1 for r in results if r["passed"])
    print(f"\n  Passed: {passed}/{len(results)}")
    print(f"  Total Time: {total_time:.1f}s")
    print(f"  Release: {'READY' if all_passed else 'BLOCKED'}")
    print(f"{'='*60}\n")

    # Write report
    output_path = BACKEND_DIR.parent / "docs" / "reports" / "release-readiness.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    content = f"""# Release Readiness Report

**Generated:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}

## Results

| Check | Status | Time |
|-------|--------|------|
"""
    for r in results:
        status = "PASS" if r["passed"] else "FAIL"
        content += f"| {r['name']} | {status} | {r['time']}s |\n"
    content += f"""
## Summary

- **Passed:** {passed}/{len(results)}
- **Total Time:** {total_time:.1f}s
- **Release:** {'READY' if all_passed else 'BLOCKED'}
"""
    output_path.write_text(content, encoding="utf-8")
    print(f"  Report: {output_path}")

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
