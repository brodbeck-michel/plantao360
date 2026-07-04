#!/usr/bin/env python3
"""
Developer CLI for Plantão 360.

Unified command-line interface for all development tools.

Usage:
    python tools/dev.py new-module Period
    python tools/dev.py validate Doctor
    python tools/dev.py lint
    python tools/dev.py docs Doctor
    python tools/dev.py tests Doctor
    python tools/dev.py architecture
    python tools/dev.py review
    python tools/dev.py scaffold Period
    python tools/dev.py health
    python tools/dev.py metrics
    python tools/dev.py adr "Title"
    python tools/dev.py compliance --all
    python tools/dev.py new-use-case ClosePeriod --module Periods
"""

import argparse
import subprocess
import sys
from pathlib import Path


TOOLS_DIR = Path(__file__).parent
BACKEND_DIR = TOOLS_DIR.parent / "backend"


def run_tool(script: str, args: list[str]) -> int:
    script_path = TOOLS_DIR / script
    if not script_path.exists():
        print(f"  ✗ Tool not found: {script}")
        return 1
    cmd = [sys.executable, str(script_path)] + args
    result = subprocess.run(cmd, cwd=str(TOOLS_DIR.parent))
    return result.returncode


def cmd_new_module(args):
    """Generate a new module from the Golden Module template."""
    gen_args = [args.module]
    if args.table:
        gen_args.extend(["--table", args.table])
    if args.route:
        gen_args.extend(["--route", args.route])
    if args.unique_field:
        gen_args.extend(["--unique-field", args.unique_field])
    if args.unique_field_label:
        gen_args.extend(["--unique-field-label", args.unique_field_label])
    return run_tool("module_generator.py", gen_args)


def cmd_validate(args):
    """Validate module architecture."""
    if args.all:
        return run_tool("validate_architecture.py", ["--all"])
    return run_tool("validate_architecture.py", [args.module])


def cmd_lint(args):
    """Run architecture linter."""
    lint_args = []
    if args.module:
        lint_args.extend(["--module", args.module])
    if args.strict:
        lint_args.append("--strict")
    return run_tool("lint_architecture.py", lint_args)


def cmd_docs(args):
    """Generate module documentation."""
    return run_tool("docs_generator.py", [args.module])


def cmd_tests(args):
    """Run module tests."""
    import re
    snake = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", args.module).lower()
    test_args = [
        f"app/tests/unit/test_{snake}_*.py",
        f"app/tests/contracts/test_{snake}_*.py",
        "-v", "--tb=short",
        "--override-ini=addopts=-v --tb=short",
    ]
    subprocess.run(
        [sys.executable, "-m", "pytest"] + test_args,
        cwd=str(BACKEND_DIR)
    )
    return 0


def cmd_architecture(args):
    """Validate all modules architecture."""
    return run_tool("validate_architecture.py", ["--all"])


def cmd_review(args):
    """Run full project review."""
    print("\n  Running Architecture Validation...")
    run_tool("validate_architecture.py", ["--all"])
    print("\n  Running Architecture Lint...")
    run_tool("lint_architecture.py", [])
    print("\n  Running Golden Guard...")
    run_tool("golden_guard.py", [])
    print("\n  Running Template Check...")
    run_tool("check_templates.py", [])
    print("\n  Running ADR Validator...")
    run_tool("check_adrs.py", [])
    print("\n  Running Metrics...")
    run_tool("project_metrics.py", [])
    print("\n  Running Compliance Report...")
    run_tool("compliance_report.py", ["--all"])
    print("\n  Running Architecture Score...")
    run_tool("architecture_score.py", [])
    print("\n  Running Module Maturity...")
    run_tool("module_maturity.py", ["--all"])
    print("\n  Running Technical Debt...")
    run_tool("technical_debt.py", [])
    print("\n  Running Release Readiness...")
    run_tool("release_readiness.py", [])
    return 0


def cmd_scaffold(args):
    """Scaffold a complete module (generate + validate)."""
    result = cmd_new_module(args)
    if result == 0:
        import re
        snake = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", "_", args.module).lower()
        print("\n  Validating generated module...")
        run_tool("validate_architecture.py", [args.module])
        print("\n  Running linter...")
        run_tool("lint_architecture.py", ["--module", args.module])
    return result


def cmd_health(args):
    """Generate project health report."""
    return run_tool("project_metrics.py", [])


def cmd_metrics(args):
    """Show project metrics."""
    return run_tool("project_metrics.py", [])


def cmd_adr(args):
    """Generate an ADR."""
    adr_args = [args.title]
    if args.status:
        adr_args.extend(["--status", args.status])
    return run_tool("adr_generator.py", adr_args)


def cmd_compliance(args):
    """Generate compliance report."""
    if args.all:
        return run_tool("compliance_report.py", ["--all"])
    return run_tool("compliance_report.py", ["--module", args.module])


def cmd_new_use_case(args):
    """Generate a new use case."""
    print(f"  Use Case Generator — {args.name}")
    print(f"  Module: {args.module}")
    print(f"  (Use case generation not yet implemented)")
    return 0


def cmd_golden_guard(args):
    """Run Golden Guard."""
    return run_tool("golden_guard.py", ["--all"])


def cmd_check_templates(args):
    """Check template consistency."""
    return run_tool("check_templates.py", [])


def cmd_check_adrs(args):
    """Validate ADRs."""
    return run_tool("check_adrs.py", [])


def cmd_technical_debt(args):
    """Generate technical debt report."""
    return run_tool("technical_debt.py", [])


def cmd_check_dependencies(args):
    """Check dependencies."""
    return run_tool("check_dependencies.py", [])


def cmd_architecture_score(args):
    """Calculate architecture score."""
    return run_tool("architecture_score.py", [])


def cmd_release_readiness(args):
    """Check release readiness."""
    return run_tool("release_readiness.py", [])


def cmd_module_maturity(args):
    """Analyze module maturity."""
    maturity_args = []
    if args.module:
        maturity_args.append(args.module)
    elif args.all:
        maturity_args.append("--all")
    return run_tool("module_maturity.py", maturity_args)


def cmd_dashboard(args):
    """Generate project dashboard."""
    print("\n  Generating Dashboard...")
    run_tool("project_metrics.py", [])
    run_tool("architecture_score.py", [])
    run_tool("compliance_report.py", ["--all"])
    run_tool("module_maturity.py", ["--all"])
    run_tool("technical_debt.py", [])
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Plantão 360 Developer CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Commands:
  new-module         Generate a new module from Golden Module template
  validate           Validate module architecture
  lint               Run architecture linter
  docs               Generate module documentation
  tests              Run module tests
  architecture       Validate all modules
  review             Run full project review
  scaffold           Generate + validate a module
  health             Project health report
  metrics            Project metrics
  adr                Generate ADR
  compliance         Module compliance report
  new-use-case       Generate a use case
  golden-guard       Run Golden Guard
  check-templates    Check template consistency
  check-adrs         Validate ADRs
  technical-debt     Technical debt report
  check-dependencies Check dependencies
  architecture-score Calculate architecture score
  release-readiness  Check release readiness
  module-maturity    Analyze module maturity
  dashboard          Generate project dashboard
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # new-module
    p_new = subparsers.add_parser("new-module", help="Generate a new module")
    p_new.add_argument("module", help="Module name (PascalCase)")
    p_new.add_argument("--table", help="Table name")
    p_new.add_argument("--route", help="Route prefix")
    p_new.add_argument("--unique-field", help="Unique field name")
    p_new.add_argument("--unique-field-label", help="Unique field label")
    p_new.set_defaults(func=cmd_new_module)

    # validate
    p_val = subparsers.add_parser("validate", help="Validate module architecture")
    p_val.add_argument("module", nargs="?", help="Module name")
    p_val.add_argument("--all", action="store_true", help="Validate all")
    p_val.set_defaults(func=cmd_validate)

    # lint
    p_lint = subparsers.add_parser("lint", help="Run architecture linter")
    p_lint.add_argument("--module", "-m", help="Module to lint")
    p_lint.add_argument("--strict", action="store_true")
    p_lint.set_defaults(func=cmd_lint)

    # docs
    p_docs = subparsers.add_parser("docs", help="Generate documentation")
    p_docs.add_argument("module", help="Module name")
    p_docs.set_defaults(func=cmd_docs)

    # tests
    p_tests = subparsers.add_parser("tests", help="Run tests")
    p_tests.add_argument("module", help="Module name")
    p_tests.set_defaults(func=cmd_tests)

    # architecture
    p_arch = subparsers.add_parser("architecture", help="Validate all modules")
    p_arch.set_defaults(func=cmd_architecture)

    # review
    p_review = subparsers.add_parser("review", help="Full project review")
    p_review.set_defaults(func=cmd_review)

    # scaffold
    p_scaffold = subparsers.add_parser("scaffold", help="Generate + validate module")
    p_scaffold.add_argument("module", help="Module name")
    p_scaffold.add_argument("--table", help="Table name")
    p_scaffold.add_argument("--route", help="Route prefix")
    p_scaffold.add_argument("--unique-field", help="Unique field")
    p_scaffold.add_argument("--unique-field-label", help="Unique field label")
    p_scaffold.set_defaults(func=cmd_scaffold)

    # health
    p_health = subparsers.add_parser("health", help="Health report")
    p_health.set_defaults(func=cmd_health)

    # metrics
    p_metrics = subparsers.add_parser("metrics", help="Project metrics")
    p_metrics.set_defaults(func=cmd_metrics)

    # adr
    p_adr = subparsers.add_parser("adr", help="Generate ADR")
    p_adr.add_argument("title", help="ADR title")
    p_adr.add_argument("--status", default="proposed")
    p_adr.set_defaults(func=cmd_adr)

    # compliance
    p_comp = subparsers.add_parser("compliance", help="Compliance report")
    p_comp.add_argument("module", nargs="?", help="Module name")
    p_comp.add_argument("--all", action="store_true")
    p_comp.set_defaults(func=cmd_compliance)

    # new-use-case
    p_uc = subparsers.add_parser("new-use-case", help="Generate use case")
    p_uc.add_argument("name", help="Use case name")
    p_uc.add_argument("--module", required=True, help="Module")
    p_uc.set_defaults(func=cmd_new_use_case)

    # golden-guard
    p_gg = subparsers.add_parser("golden-guard", help="Run Golden Guard")
    p_gg.set_defaults(func=cmd_golden_guard)

    # check-templates
    p_ct = subparsers.add_parser("check-templates", help="Check template consistency")
    p_ct.set_defaults(func=cmd_check_templates)

    # check-adrs
    p_ca = subparsers.add_parser("check-adrs", help="Validate ADRs")
    p_ca.set_defaults(func=cmd_check_adrs)

    # technical-debt
    p_td = subparsers.add_parser("technical-debt", help="Technical debt report")
    p_td.set_defaults(func=cmd_technical_debt)

    # check-dependencies
    p_cd = subparsers.add_parser("check-dependencies", help="Check dependencies")
    p_cd.set_defaults(func=cmd_check_dependencies)

    # architecture-score
    p_as = subparsers.add_parser("architecture-score", help="Calculate architecture score")
    p_as.set_defaults(func=cmd_architecture_score)

    # release-readiness
    p_rr = subparsers.add_parser("release-readiness", help="Check release readiness")
    p_rr.set_defaults(func=cmd_release_readiness)

    # module-maturity
    p_mm = subparsers.add_parser("module-maturity", help="Analyze module maturity")
    p_mm.add_argument("module", nargs="?", help="Module name")
    p_mm.add_argument("--all", action="store_true", help="All modules")
    p_mm.set_defaults(func=cmd_module_maturity)

    # dashboard
    p_dash = subparsers.add_parser("dashboard", help="Generate project dashboard")
    p_dash.set_defaults(func=cmd_dashboard)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    result = args.func(args)
    sys.exit(result)


if __name__ == "__main__":
    main()
