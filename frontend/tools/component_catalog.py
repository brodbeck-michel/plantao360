#!/usr/bin/env python3
"""
Component Catalog — Plantão 360

Gera catálogo de componentes automaticamente.

Uso:
    python component_catalog.py

Exemplo:
    python component_catalog.py
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List

# ============================================================
# Constants
# ============================================================

FRONTEND_ROOT = Path(__file__).parent.parent
SHARED_DIR = FRONTEND_ROOT / "src" / "shared" / "components"
FEATURES_DIR = FRONTEND_ROOT / "src" / "features"
CATALOG_PATH = FRONTEND_ROOT / "docs" / "frontend" / "component-catalog.json"

# ============================================================
# Catalog Generator
# ============================================================

def extract_component_info(file_path: Path) -> Dict:
    """Extract component information from file."""
    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    info = {
        "name": file_path.stem,
        "file": str(file_path.relative_to(FRONTEND_ROOT)),
        "props": [],
        "description": "",
        "dependencies": [],
    }

    # Extract description from comment block
    for line in lines[:20]:
        if line.strip().startswith("*") and not line.strip().startswith("**"):
            desc = line.strip().lstrip("* ").strip()
            if desc and not desc.startswith("Plantão") and not desc.startswith("Sprint"):
                info["description"] = desc
                break

    # Extract props from interface
    in_props = False
    for line in lines:
        if "Props" in line and "interface" in line:
            in_props = True
            continue
        if in_props:
            if line.strip().startswith("}"):
                in_props = False
                continue
            if ":" in line and not line.strip().startswith("//"):
                prop_name = line.split(":")[0].strip().rstrip("?")
                if prop_name and not prop_name.startswith("//"):
                    info["props"].append(prop_name)

    # Extract dependencies from imports
    for line in lines:
        if "import" in line and "from" in line:
            dep = line.split("from")[1].strip().strip("'\"")
            if dep.startswith("@mui") or dep.startswith("react"):
                info["dependencies"].append(dep)

    return info


def generate_catalog() -> Dict:
    """Generate complete component catalog."""
    catalog = {
        "generated_at": "2026-06-27",
        "shared_components": [],
        "feature_components": [],
    }

    # Shared components
    if SHARED_DIR.exists():
        for item in SHARED_DIR.iterdir():
            if item.suffix == ".tsx" and item.name != "index.ts":
                info = extract_component_info(item)
                info["type"] = "shared"
                info["reusable"] = True
                catalog["shared_components"].append(info)

    # Feature components
    if FEATURES_DIR.exists():
        for feature_dir in FEATURES_DIR.iterdir():
            if feature_dir.is_dir():
                components_dir = feature_dir / "components"
                if components_dir.exists():
                    for item in components_dir.iterdir():
                        if item.suffix == ".tsx":
                            info = extract_component_info(item)
                            info["type"] = "feature"
                            info["feature"] = feature_dir.name
                            info["reusable"] = False
                            catalog["feature_components"].append(info)

    return catalog


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    print("\n📚 Generating component catalog...\n")

    catalog = generate_catalog()

    # Save catalog
    CATALOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CATALOG_PATH.write_text(json.dumps(catalog, indent=2), encoding="utf-8")

    print(f"✅ Catalog generated: {CATALOG_PATH}")
    print(f"   Shared components: {len(catalog['shared_components'])}")
    print(f"   Feature components: {len(catalog['feature_components'])}")
    print()

    # Display summary
    print("📋 Shared Components:")
    for comp in catalog["shared_components"]:
        print(f"   - {comp['name']}: {comp['description'][:50]}...")

    print("\n📋 Feature Components:")
    for comp in catalog["feature_components"]:
        print(f"   - {comp['name']} ({comp['feature']}): {comp['description'][:50]}...")
