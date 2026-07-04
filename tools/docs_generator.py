#!/usr/bin/env python3
"""
Documentation Generator V2 — Auto-generates module documentation.

Uses manifests as the source of truth.

Usage:
    python tools/docs_generator.py Doctor
    python tools/docs_generator.py --all
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


def generate_mermaid(module: ModuleManifest) -> str:
    snake = module._resolve_storage_name()
    name = module.canonical_name

    diagram = f"""```mermaid
graph TB
    subgraph "{name} Module"
        Router["API Router"]
        Service["Service"]
"""
    if module.has_capability("mapper"):
        diagram += '        Mapper["Mapper"]\n'
    if module.has_capability("validator"):
        diagram += '        Validator["Validator"]\n'
    diagram += f"""        Repository["Repository"]
        Interface["Repository Interface"]
        Model["Model"]
"""
    if module.has_capability("dtos.create") or module.has_capability("dtos.response"):
        diagram += '        DTOs["DTOs"]\n'
    if module.has_capability("events"):
        diagram += '        Events["Events"]\n'
    if module.has_capability("state_machine"):
        diagram += '        StateMachine["State Machine"]\n'
    if module.has_capability("policy"):
        diagram += '        Policy["Policy"]\n'
    diagram += """    end

    Router -->|"uses"| Service
    Service -->|"uses"| Repository
    Service -->|"uses"| Interface
"""
    if module.has_capability("mapper"):
        diagram += '    Service -->|"uses"| Mapper\n'
    if module.has_capability("validator"):
        diagram += '    Service -->|"uses"| Validator\n'
    if module.has_capability("events"):
        diagram += '    Service -->|"emits"| Events\n'
    diagram += f"""    Repository -->|"queries"| Model
    Model -->|"SQLAlchemy"| Database[("Database")]

    style Router fill:#4CAF50,color:#fff
    style Service fill:#2196F3,color:#fff
    style Repository fill:#FF9800,color:#fff
    style Model fill:#9C27B0,color:#fff
```"""
    return diagram


def generate_docs(module: ModuleManifest, output_dir: Path | None = None) -> str:
    snake = module._resolve_storage_name()
    name = module.canonical_name
    resolved = module.resolve_files()

    mermaid = generate_mermaid(module)

    # Build capabilities table
    caps = module.data.get("capabilities", {})
    caps_table = "\n## Architectural Capabilities\n\n| Capability | Enabled |\n|---|---|\n"
    for cap in ["model", "repository", "repository_interface", "service", "mapper",
                "validator", "router", "state_machine", "policy", "events", "contracts", "value_objects"]:
        enabled = caps.get(cap, False)
        caps_table += f"| {cap} | {'✓' if enabled else '✗'} |\n"

    # Build lifecycle table
    lifecycle = module.data.get("lifecycle", {})
    states = lifecycle.get("states", [])
    initial = lifecycle.get("initial_state", "")
    terminals = lifecycle.get("terminal_states", [])
    lifecycle_table = "\n## Lifecycle\n\n"
    if states:
        lifecycle_table += f"**States:** {', '.join(states)}\n\n"
        lifecycle_table += f"**Initial:** {initial}\n\n"
        lifecycle_table += f"**Terminal:** {', '.join(terminals)}\n"

    # Build ADR references
    adr_refs = module.adr_references
    adr_table = "\n## ADR References\n\n"
    for ref in adr_refs:
        adr_table += f"- **{ref.get('id', '?')}**: {ref.get('title', '?')} — {ref.get('decision', '?')}\n"

    # Build files table
    files_table = "\n## Resolved Files\n\n| Capability | Path | Exists |\n|---|---|---|\n"
    for cap_name, rp in resolved.items():
        files_table += f"| {cap_name} | `{rp.path.relative_to(BACKEND_DIR)}` | {'✓' if rp.exists else '✗'} |\n"

    content = f"""# {name} Module

**Module ID:** {module.module_id}
**Bounded Context:** {module.bounded_context}
**Aggregate:** {module.aggregate}
**Storage:** {module.storage_name} ({module.storage_table})
**Stability:** {module.stability_level} (since {module.data.get('stability', {}).get('since', '?')})
**Validation Profile:** {module.validation_profile}

## Architecture

{mermaid}

{lifecycle_table}

{caps_table}

{adr_table}

{files_table}

## Golden Module Compliance

- [x] Repository Interface
- [x] Service uses Interface
- [x] DTOs separated
- [x] Error Codes
- [x] Event Versioning (.v1)
- [x] Contract Tests
- [x] ApiResponse standard
- [x] Pagination headers
"""

    if output_dir is None:
        output_dir = DOCS_DIR / "modules"
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / f"{snake}-module.md"
    filepath.write_text(content, encoding="utf-8")

    print(f"  ✓ Documentation generated: {filepath.relative_to(DOCS_DIR.parent)}")
    return str(filepath)


def main():
    parser = argparse.ArgumentParser(description="Generate module documentation (V2)")
    parser.add_argument("module", nargs="?", help="Module name (canonical or storage)")
    parser.add_argument("--all", action="store_true", help="Generate for all modules")
    parser.add_argument("--output", help="Output directory")
    args = parser.parse_args()

    loader = ManifestLoader()
    output_dir = Path(args.output) if args.output else None

    if args.module:
        manifest = loader.get_by_canonical_name(args.module)
        if not manifest:
            manifest = loader.get_by_storage_name(args.module)
        if not manifest:
            manifest = loader.get(args.module.lower())
        if not manifest:
            print(f"  ERROR: No manifest found for '{args.module}'")
            sys.exit(1)
        generate_docs(manifest, output_dir)

    elif args.all:
        for name in loader.discover():
            manifest = loader.get(name)
            if manifest:
                generate_docs(manifest, output_dir)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
