#!/usr/bin/env python3
"""
Dependency Governance — Checks for dependency issues.

Usage:
    python tools/check_dependencies.py
"""

import io
import os
import re
import sys
from pathlib import Path
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

BACKEND_DIR = Path(__file__).parent.parent / "backend"
APP_DIR = BACKEND_DIR / "app"


def find_all_imports() -> dict[str, list[str]]:
    imports_by_file = {}
    for filepath in APP_DIR.rglob("*.py"):
        if "__pycache__" in str(filepath):
            continue
        try:
            content = filepath.read_text(encoding="utf-8")
            rel_path = str(filepath.relative_to(BACKEND_DIR))
            imports = []
            for line in content.split("\n"):
                line = line.strip()
                if line.startswith("from ") and " import " in line:
                    module = line.split(" from ")[1].split(" import ")[0].strip()
                    imports.append(module)
                elif line.startswith("import "):
                    module = line.split(" import ")[1].strip()
                    imports.append(module)
            imports_by_file[rel_path] = imports
        except Exception:
            continue
    return imports_by_file


def find_circular_imports(imports_by_file: dict[str, list[str]]) -> list[dict]:
    circular = []
    for file1, imps1 in imports_by_file.items():
        for imp in imps1:
            if imp.startswith("app."):
                # Check if the imported module imports back
                target_file = imp.replace("app.", "").replace(".", "/") + ".py"
                target_path = APP_DIR / target_file
                if target_path.exists():
                    target_rel = str(target_path.relative_to(BACKEND_DIR))
                    if target_rel in imports_by_file:
                        for target_imp in imports_by_file[target_rel]:
                            if target_imp.startswith("app."):
                                source_module = file1.replace("/", ".").replace(".py", "")
                                if source_module in target_imp:
                                    circular.append({
                                        "from": file1,
                                        "to": imp,
                                        "reverse": target_imp
                                    })
    return circular


def check_duplicate_imports(imports_by_file: dict[str, list[str]]) -> list[dict]:
    duplicates = []
    all_imports = []
    for file, imps in imports_by_file.items():
        for imp in imps:
            all_imports.append((file, imp))

    # Group by import
    import_files = {}
    for file, imp in all_imports:
        if imp not in import_files:
            import_files[imp] = []
        import_files[imp].append(file)

    # Find duplicates (same module imported in many files - not necessarily bad)
    for imp, files in import_files.items():
        if len(files) > 10:
            duplicates.append({
                "import": imp,
                "count": len(files),
                "files": files[:5]
            })

    return duplicates


def main():
    print(f"\n{'='*60}")
    print(f"  Dependency Governance — Plantão 360")
    print(f"{'='*60}\n")

    imports_by_file = find_all_imports()
    print(f"  Files scanned: {len(imports_by_file)}")

    # Circular imports
    circular = find_circular_imports(imports_by_file)
    if circular:
        print(f"\n  Circular Imports: {len(circular)}")
        for c in circular[:10]:
            print(f"    {c['from']} -> {c['to']}")
    else:
        print(f"\n  Circular Imports: None found")

    # Duplicate imports
    duplicates = check_duplicate_imports(imports_by_file)
    if duplicates:
        print(f"\n  Frequently Imported: {len(duplicates)}")
        for d in duplicates[:10]:
            print(f"    {d['import']}: {d['count']} files")

    print(f"\n{'='*60}")
    print(f"  Overall: {'PASS' if not circular else 'FAIL (circular imports)'}")
    print(f"{'='*60}\n")

    sys.exit(0 if not circular else 1)


if __name__ == "__main__":
    main()
