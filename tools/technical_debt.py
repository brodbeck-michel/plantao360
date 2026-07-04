#!/usr/bin/env python3
"""
Technical Debt Detector — Generates debt report.

Usage:
    python tools/technical_debt.py
    python tools/technical_debt.py --json
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
DOCS_DIR = Path(__file__).parent.parent / "docs"


@dataclass
class DebtItem:
    file: str
    line: int
    type: str
    message: str
    severity: str = "warning"


@dataclass
class DebtReport:
    items: list[DebtItem] = field(default_factory=list)
    files_scanned: int = 0

    @property
    def todo_count(self) -> int:
        return sum(1 for i in self.items if i.type == "TODO")

    @property
    def fixme_count(self) -> int:
        return sum(1 for i in self.items if i.type == "FIXME")

    @property
    def deprecated_count(self) -> int:
        return sum(1 for i in self.items if i.type == "DEPRECATED")

    @property
    def unused_import_count(self) -> int:
        return sum(1 for i in self.items if i.type == "UNUSED_IMPORT")

    @property
    def total(self) -> int:
        return len(self.items)


def scan_file(filepath: Path) -> list[DebtItem]:
    items = []
    try:
        content = filepath.read_text(encoding="utf-8")
        lines = content.split("\n")
        rel_path = str(filepath.relative_to(BACKEND_DIR))
    except Exception:
        return items

    for i, line in enumerate(lines, 1):
        # TODOs
        todo_match = re.search(r"#\s*TODO[:\s]*(.*)", line)
        if todo_match:
            items.append(DebtItem(
                file=rel_path, line=i, type="TODO",
                message=todo_match.group(1).strip() or "No description",
                severity="info"
            ))

        # FIXMEs
        fixme_match = re.search(r"#\s*FIXME[:\s]*(.*)", line)
        if fixme_match:
            items.append(DebtItem(
                file=rel_path, line=i, type="FIXME",
                message=fixme_match.group(1).strip() or "No description",
                severity="warning"
            ))

        # Deprecated
        if re.search(r"deprecated|@deprecated", line, re.IGNORECASE):
            items.append(DebtItem(
                file=rel_path, line=i, type="DEPRECATED",
                message="Deprecated code detected",
                severity="warning"
            ))

        # Unused imports (simple heuristic: imported but not used)
        import_match = re.match(r"from\s+\S+\s+import\s+(.*)", line)
        if import_match:
            imported = [n.strip() for n in import_match.group(1).split(",")]
            for name in imported:
                if name and name != "*" and name not in content[len(line):]:
                    items.append(DebtItem(
                        file=rel_path, line=i, type="UNUSED_IMPORT",
                        message=f"Potentially unused import: {name}",
                        severity="info"
                    ))

    return items


def generate_report() -> DebtReport:
    report = DebtReport()
    for filepath in APP_DIR.rglob("*.py"):
        if "__pycache__" in str(filepath) or "test_" in filepath.name:
            continue
        report.files_scanned += 1
        report.items.extend(scan_file(filepath))
    return report


def write_markdown_report(report: DebtReport) -> str:
    output_dir = DOCS_DIR / "reports"
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / "technical-debt.md"

    content = f"""# Technical Debt Report

**Generated:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}

**Files Scanned:** {report.files_scanned}

---

## Summary

| Type | Count |
|------|-------|
| TODOs | {report.todo_count} |
| FIXMEs | {report.fixme_count} |
| Deprecated | {report.deprecated_count} |
| Unused Imports | {report.unused_import_count} |
| **Total** | **{report.total}** |

---

## Items

| File | Line | Type | Message |
|------|------|------|---------|
"""
    for item in sorted(report.items, key=lambda x: (x.type, x.file, x.line)):
        content += f"| {item.file} | {item.line} | {item.type} | {item.message} |\n"

    content += f"""

---

## By File

"""
    files = {}
    for item in report.items:
        if item.file not in files:
            files[item.file] = []
        files[item.file].append(item)

    for file_path, items in sorted(files.items()):
        content += f"### {file_path}\n\n"
        for item in items:
            content += f"- Line {item.line}: [{item.type}] {item.message}\n"
        content += "\n"

    filepath.write_text(content, encoding="utf-8")
    return str(filepath)


def main():
    parser = argparse.ArgumentParser(description="Technical Debt Detector")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    print(f"\n{'='*60}")
    print(f"  Technical Debt Detector — Plantão 360")
    print(f"{'='*60}\n")

    report = generate_report()

    if args.json:
        data = {
            "files_scanned": report.files_scanned,
            "todo_count": report.todo_count,
            "fixme_count": report.fixme_count,
            "deprecated_count": report.deprecated_count,
            "unused_import_count": report.unused_import_count,
            "total": report.total,
            "items": [asdict(i) for i in report.items]
        }
        print(json.dumps(data, indent=2))
    else:
        print(f"  Files Scanned: {report.files_scanned}")
        print(f"  TODOs: {report.todo_count}")
        print(f"  FIXMEs: {report.fixme_count}")
        print(f"  Deprecated: {report.deprecated_count}")
        print(f"  Unused Imports: {report.unused_import_count}")
        print(f"  Total Debt Items: {report.total}")

        filepath = write_markdown_report(report)
        print(f"\n  Report: {filepath}")


if __name__ == "__main__":
    main()
