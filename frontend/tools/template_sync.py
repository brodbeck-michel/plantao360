#!/usr/bin/env python3
"""
Template Sync — Plantão 360

Sincroniza templates com o Golden Module.

Uso:
    python template_sync.py

Exemplo:
    python template_sync.py
"""

import os
import sys
import shutil
from pathlib import Path

# ============================================================
# Constants
# ============================================================

FRONTEND_ROOT = Path(__file__).parent.parent
FEATURES_DIR = FRONTEND_ROOT / "src" / "features"
TEMPLATES_DIR = Path(__file__).parent / "templates"
GOLDEN_MODULE = "doctor"

# ============================================================
# Template Sync
# ============================================================

def sync_templates():
    """Sync templates from Golden Module."""
    golden_path = FEATURES_DIR / GOLDEN_MODULE

    if not golden_path.exists():
        print("❌ Golden Module not found!")
        return False

    # Create templates directory
    TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)

    # Sync each directory
    for dir_name in ["components", "hooks", "services", "types", "forms", "tables", "filters", "dialogs"]:
        golden_dir = golden_path / dir_name
        if golden_dir.exists():
            template_dir = TEMPLATES_DIR / dir_name
            template_dir.mkdir(parents=True, exist_ok=True)

            for item in golden_dir.iterdir():
                if item.is_file():
                    # Read and template-ize the content
                    content = item.read_text(encoding="utf-8")

                    # Replace Doctor-specific names with placeholders
                    content = content.replace("Doctor", "{{FEATURE_PASCAL}}")
                    content = content.replace("doctor", "{{FEATURE_NAME}}")
                    content = content.replace("useDoctors", "use{{FEATURE_PASCAL}}s")
                    content = content.replace("doctorQueries", "{{FEATURE_NAME}}Queries")

                    # Write template
                    template_path = template_dir / item.name.replace("doctor", "{{FEATURE_NAME}}")
                    template_path.write_text(content, encoding="utf-8")
                    print(f"   ✅ Synced: {dir_name}/{item.name}")

    print("\n✅ Templates synced from Golden Module")
    return True


# ============================================================
# CLI
# ============================================================

if __name__ == "__main__":
    print("\n🔄 Syncing templates from Golden Module...\n")
    sync_templates()
