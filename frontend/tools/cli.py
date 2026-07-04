#!/usr/bin/env python3
"""
Frontend CLI — Plantão 360

CLI unificada para todas as ferramentas do Frontend.

Uso:
    python cli.py <command> [args]

Comandos:
    feature:create <name>     Criar nova feature
    validate [name]           Validar features
    score [name]              Calcular score
    catalog                   Gerar catálogo
    drift [name]              Detectar drift
    golden-lock [name]        Validar golden lock
    ux-validate [name]        Validar UX
    manifest-validate [name]  Validar manifests
    review                    Gerar review
    sync-templates            Sincronizar templates
"""

import sys
import os

# Add tools directory to path
sys.path.insert(0, os.path.dirname(os.pathfile.abspath(__file__)))

from feature_generator import generate_feature
from validate_frontend import validate_feature, validate_all_features
from frontend_score import calculate_score
from component_catalog import generate_catalog
from template_drift import detect_drift
from golden_lock import validate_golden_lock
from ux_validator import validate_ux
from manifest_validator import validate_manifest
from frontend_review import generate_review
from template_sync import sync_templates

# ============================================================
# Commands
# ============================================================

COMMANDS = {
    "feature:create": lambda args: generate_feature(args[0]) if args else print("Uso: feature:create <name>"),
    "validate": lambda args: validate_all_features() if not args else validate_feature(args[0]),
    "score": lambda args: [print(f"Score: {calculate_score(args[0])}")] if args else [print(f"{f}: {calculate_score(f)}") for f in os.listdir(os.path.join(os.path.dirname(__file__), "..", "src", "features")) if os.path.isdir(os.path.join(os.path.dirname(__file__), "..", "src", "features", f))],
    "catalog": lambda args: generate_catalog(),
    "drift": lambda args: detect_drift(args[0]) if args else [detect_drift(f) for f in os.listdir(os.path.join(os.path.dirname(__file__), "..", "src", "features")) if os.path.isdir(os.path.join(os.path.dirname(__file__), "..", "src", "features", f))],
    "golden-lock": lambda args: validate_golden_lock(args[0]) if args else [validate_golden_lock(f) for f in os.listdir(os.path.join(os.path.dirname(__file__), "..", "src", "features")) if os.path.isdir(os.path.join(os.path.dirname(__file__), "..", "src", "features", f))],
    "ux-validate": lambda args: validate_ux(args[0]) if args else [validate_ux(f) for f in os.listdir(os.path.join(os.path.dirname(__file__), "..", "src", "features")) if os.path.isdir(os.path.join(os.path.dirname(__file__), "..", "src", "features", f))],
    "manifest-validate": lambda args: validate_manifest(args[0]) if args else [validate_manifest(f) for f in os.listdir(os.path.join(os.path.dirname(__file__), "..", "manifests")) if f.endswith(".json")],
    "review": lambda args: generate_review(),
    "sync-templates": lambda args: sync_templates(),
}

# ============================================================
# CLI
# ============================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nComandos disponíveis:")
        for cmd in COMMANDS:
            print(f"  {cmd}")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    if command not in COMMANDS:
        print(f"Comando desconhecido: {command}")
        print(__doc__)
        sys.exit(1)

    print(f"\n🔧 Executando: {command}\n")
    COMMANDS[command](args)


if __name__ == "__main__":
    main()
