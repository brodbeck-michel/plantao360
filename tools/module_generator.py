#!/usr/bin/env python3
"""
Module Generator CLI for Plantão 360.

Generates a complete module following the Golden Module pattern.

Usage:
    python tools/module_generator.py Period --table periods --route /periods --entity Period --plural periods --event-prefix period
    python tools/module_generator.py Shift --unique-field code --unique-field-label "Código"
"""

import argparse
import json
import os
import re
import sys
import io
from pathlib import Path
from string import Template

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


TEMPLATE_DIR = Path(__file__).parent.parent / "backend" / "templates" / "golden-module"
BACKEND_DIR = Path(__file__).parent.parent / "backend"
APP_DIR = BACKEND_DIR / "app"


def to_snake_case(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def to_pascal_case(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_"))


def to_upper(name: str) -> str:
    return to_snake_case(name).upper()


def load_template(template_path: str) -> str:
    full_path = TEMPLATE_DIR / template_path
    if not full_path.exists():
        raise FileNotFoundError(f"Template not found: {full_path}")
    return full_path.read_text(encoding="utf-8")


def render_template(content: str, variables: dict) -> str:
    result = content
    for key, value in variables.items():
        placeholder = "{{" + key + "}}"
        result = result.replace(placeholder, str(value))
    return result


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_file(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")
    print(f"  Created: {path.relative_to(BACKEND_DIR.parent)}")


def generate_module(args):
    module_name = args.module
    module_name_snake = to_snake_case(module_name)
    module_name_plural = args.plural or f"{module_name_snake}s"
    module_name_plural_pascal = to_pascal_case(module_name_plural)
    module_name_upper = to_upper(module_name)
    table_name = args.table or f"{module_name_snake}s"
    route = args.route or f"/{module_name_plural}"
    event_prefix = args.event_prefix or module_name_snake
    unique_field = args.unique_field or "code"
    unique_field_label = args.unique_field_label or unique_field.upper()

    # Build field definitions from args or use defaults
    model_fields = args.model_fields or f'    name: str = mapped_column(String(255), nullable=False)'
    create_dto_fields = args.create_dto_fields or f'    name: str = Field(..., min_length=1, max_length=255, description="Nome")'
    update_dto_fields = args.update_dto_fields or f'    name: str | None = Field(None, min_length=1, max_length=255, description="Nome")'
    response_dto_fields = args.response_dto_fields or f'    name: str = Field(..., description="Nome")'
    summary_dto_fields = args.summary_dto_fields or f'    name: str = Field(..., description="Nome")'
    filter_dto_fields = args.filter_dto_fields or f'    name: str | None = Field(None, description="Filtro por nome")'
    query_dto_fields = args.query_dto_fields or f'    name: str | None = Field(None, description="Filtro por nome")'
    filter_fields = args.filter_fields or ["name"]
    allowed_sorts = args.allowed_sorts or ["id", "name", "active"]
    validation_rules = args.validation_rules or ["name"]
    extra_error_codes = args.extra_error_codes or []

    # Test data
    test_name = f"Test {module_name}"
    test_code = "TEST001"
    repo_create_fields = f'name="{test_name}", {unique_field}="{test_code}"'
    service_create_fields = f'name="{test_name}", {unique_field}="{test_code}"'
    service_update_fields = f'name="{test_name} Updated"'
    mapper_create_fields = f'name="{test_name}", {unique_field}="{test_code}"'
    mapper_dto_fields = f'name="{test_name}", {unique_field}="{test_code}"'
    validator_create_fields = f'name="{test_name}", {unique_field}="{test_code}"'
    validator_update_fields = f'name="{test_name} Updated"'
    integration_create_json = f'{{"name": "{test_name}", "{unique_field}": "{test_code}"}}'
    integration_update_json = f'{{"name": "{test_name} Updated"}}'
    repr_create_fields = f'name="{test_name}", {unique_field}="{test_code}"'
    repr_field = unique_field
    repr_expr = f"self.{unique_field}"

    variables = {
        "module_name": module_name,
        "module_name_snake": module_name_snake,
        "module_name_plural": module_name_plural,
        "module_name_plural_pascal": module_name_plural_pascal,
        "module_name_upper": module_name_upper,
        "table_name": table_name,
        "route": route,
        "event_prefix": event_prefix,
        "unique_field": unique_field,
        "unique_field_label": unique_field_label,
        "model_fields": model_fields,
        "create_dto_fields": create_dto_fields,
        "update_dto_fields": update_dto_fields,
        "response_dto_fields": response_dto_fields,
        "summary_dto_fields": summary_dto_fields,
        "filter_dto_fields": filter_dto_fields,
        "query_dto_fields": query_dto_fields,
        "filter_fields": ", ".join(f'"{f}"' for f in filter_fields),
        "allowed_sorts": ", ".join(f'"{s}"' for s in allowed_sorts),
        "validation_rules": " ".join(validation_rules),
        "extra_error_codes": "\n    ".join(extra_error_codes),
        "repo_create_fields": repo_create_fields,
        "service_create_fields": service_create_fields,
        "service_update_fields": service_update_fields,
        "mapper_create_fields": mapper_create_fields,
        "mapper_dto_fields": mapper_dto_fields,
        "validator_create_fields": validator_create_fields,
        "validator_update_fields": validator_update_fields,
        "integration_create_json": integration_create_json,
        "integration_update_json": integration_update_json,
        "repr_create_fields": repr_create_fields,
        "repr_field": repr_field,
        "repr_expr": repr_expr,
    }

    print(f"\n{'='*60}")
    print(f"  Module Generator — Plantão 360")
    print(f"{'='*60}")
    print(f"  Module:      {module_name}")
    print(f"  Table:       {table_name}")
    print(f"  Route:       {route}")
    print(f"  Event Prefix:{event_prefix}")
    print(f"  Unique Field:{unique_field}")
    print(f"{'='*60}\n")

    # Generate all files from templates
    templates = {
        f"models/{module_name_snake}.py": "models/model.py.j2",
        f"repositories/interfaces/{module_name_snake}_repository.py": "repositories/interfaces/repository_interface.py.j2",
        f"repositories/{module_name_snake}_repository.py": "repositories/repository.py.j2",
        f"services/{module_name_snake}_service.py": "services/service.py.j2",
        f"mappers/{module_name_snake}_mapper.py": "mappers/mapper.py.j2",
        f"validators/{module_name_snake}_validator.py": "validators/validator.py.j2",
        f"validators/rules/{unique_field}.py": "validators/rules/unique_field.py.j2",
        f"schemas/{module_name_snake}/{module_name_snake}_create.py": "schemas/create.py.j2",
        f"schemas/{module_name_snake}/{module_name_snake}_update.py": "schemas/update.py.j2",
        f"schemas/{module_name_snake}/{module_name_snake}_response.py": "schemas/response.py.j2",
        f"schemas/{module_name_snake}/{module_name_snake}_summary.py": "schemas/summary.py.j2",
        f"schemas/{module_name_snake}/{module_name_snake}_filters.py": "schemas/filters.py.j2",
        f"schemas/{module_name_snake}/{module_name_snake}_query.py": "schemas/query.py.j2",
        f"schemas/{module_name_snake}/__init__.py": "schemas/__init__.py.j2",
        f"api/routes/{module_name_snake}.py": "routes/router.py.j2",
        f"domain/errors/{module_name_snake}_errors.py": "domain/errors/error_codes.py.j2",
        f"tests/unit/test_{module_name_snake}_model.py": "tests/unit/test_model.py.j2",
        f"tests/unit/test_{module_name_snake}_repository.py": "tests/unit/test_repository.py.j2",
        f"tests/unit/test_{module_name_snake}_service.py": "tests/unit/test_service.py.j2",
        f"tests/unit/test_{module_name_snake}_mapper.py": "tests/unit/test_mapper.py.j2",
        f"tests/unit/test_{module_name_snake}_validator.py": "tests/unit/test_validator.py.j2",
        f"tests/integration/test_{module_name_snake}_api.py": "tests/integration/test_api.py.j2",
        f"tests/contracts/test_{module_name_snake}_contracts.py": "tests/contracts/test_contracts.py.j2",
    }

    generated = []
    for output_rel, template_rel in templates.items():
        output_path = APP_DIR / output_rel
        if output_path.exists():
            print(f"  SKIP (exists): {output_rel}")
            continue
        try:
            content = load_template(template_rel)
            rendered = render_template(content, variables)
            write_file(output_path, rendered)
            generated.append(output_rel)
        except Exception as e:
            print(f"  ERROR: {output_rel}: {e}")

    # Generate event names to add
    event_names_to_add = [
        f"    {module_name_upper}_CREATED_V1 = \"{event_prefix}.created.v1\"",
        f"    {module_name_upper}_UPDATED_V1 = \"{event_prefix}.updated.v1\"",
        f"    {module_name_upper}_DEACTIVATED_V1 = \"{event_prefix}.deactivated.v1\"",
    ]

    # Generate manifest file
    manifest_path = Path(__file__).parent.parent / "backend" / "architecture" / "manifests" / f"{module_name_snake}.yaml"
    if not manifest_path.exists():
        manifest_content = f"""manifest_version: 1

module_id: scheduling.{module_name_snake}

module:
  canonical_name: {module_name}
  storage_name: {module_name_snake}
  storage_table: {table_name}

ownership:
  aggregate: {module_name}
  bounded_context: Scheduling

stability:
  level: experimental
  since: Sprint ?
  adr: ADR-?

lifecycle:
  states:
    - active
    - inactive
  initial_state: active
  terminal_states:
    - inactive

capabilities:
  model: true
  repository: true
  repository_interface: true
  service: true
  mapper: true
  validator: true
  router: true

  state_machine: false
  policy: false
  events: true
  contracts: false
  value_objects: false

  dtos:
    create: true
    update: true
    response: true
    filters: true
    query: true
    summary: true
    detail: false

  tests:
    unit: true
    integration: true
    contracts: true

aliases: []

validation_profile: enterprise

adr_references: []
"""
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(manifest_content, encoding="utf-8")
        print(f"  Created: {manifest_path.relative_to(BACKEND_DIR.parent)}")
        generated.append(f"architecture/manifests/{module_name_snake}.yaml")

    print(f"\n{'='*60}")
    print(f"  Generated {len(generated)} files")
    print(f"{'='*60}")
    print(f"\n  Next steps:")
    print(f"  1. Add event names to app/domain/events/event_names.py:")
    for line in event_names_to_add:
        print(f"     {line}")
    print(f"  2. Register router in app/api/app.py:")
    print(f"     from app.api.routes import {module_name_snake}")
    print(f'     application.include_router({module_name_snake}.router, prefix="/api/v1")')
    print(f"  3. Update manifest: backend/architecture/manifests/{module_name_snake}.yaml")
    print(f"  4. Run: python -m pytest app/tests/unit/test_{module_name_snake}_* -v")
    print(f"  5. Run: python tools/validate_architecture.py {module_name}")
    print(f"  6. Run: python tools/manifest_validator.py --manifest {module_name_snake}")
    print()

    return generated


def main():
    parser = argparse.ArgumentParser(
        description="Generate a new module following the Golden Module pattern"
    )
    parser.add_argument("module", help="Module name in PascalCase (e.g., Period, Shift)")
    parser.add_argument("--table", help="Database table name (default: {module}_s)")
    parser.add_argument("--route", help="API route prefix (default: /{module}s)")
    parser.add_argument("--entity", help="Entity name (default: module name)")
    parser.add_argument("--plural", help="Plural name (default: {module}s)")
    parser.add_argument("--event-prefix", help="Event prefix (default: {module_snake})")
    parser.add_argument("--unique-field", default="code", help="Unique field name (default: code)")
    parser.add_argument("--unique-field-label", default="Código", help="Unique field label")
    parser.add_argument("--model-fields", help="SQLAlchemy model field definitions")
    parser.add_argument("--create-dto-fields", help="CreateDTO field definitions")
    parser.add_argument("--update-dto-fields", help="UpdateDTO field definitions")
    parser.add_argument("--response-dto-fields", help="ResponseDTO field definitions")
    parser.add_argument("--summary-dto-fields", help="SummaryDTO field definitions")
    parser.add_argument("--filter-dto-fields", help="FilterDTO field definitions")
    parser.add_argument("--query-dto-fields", help="QueryDTO field definitions")
    parser.add_argument("--filter-fields", nargs="+", help="Filter field names")
    parser.add_argument("--allowed-sorts", nargs="+", help="Allowed sort fields")
    parser.add_argument("--validation-rules", nargs="+", help="Validation rule function names")
    parser.add_argument("--extra-error-codes", nargs="+", help="Extra error codes")

    args = parser.parse_args()
    generate_module(args)


if __name__ == "__main__":
    main()
