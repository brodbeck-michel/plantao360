# ADR-016: Module Manifest System

**Status:** Accepted
**Date:** 2026-06-26
**Sprint:** 5.1
**Deciders:** Architecture Team

---

## Context

The Plantão 360 platform has 4 architectural aggregates (Doctor, Period, Shift, Assignment). Each aggregate has different file naming conventions due to legitimate architectural decisions (e.g., Assignment uses `shift_part` as storage name but `assignment` as domain name).

Governance tools (Architecture Validator, Golden Guard, Compliance Report, etc.) used `to_snake_case(module_name)` to derive file paths, which caused false negatives when domain names differed from storage names.

## Decision

We will implement a **Module Manifest** system where each aggregate has a YAML file declaring its complete architectural identity.

### Key Design Decisions

1. **Capabilities, not file paths**: Manifests declare WHAT capabilities exist (model, repository, service, etc.), not WHERE files are located. The loader resolves paths.

2. **Manifest as public contract**: Each manifest contains:
   - `module_id`: Permanent stable identifier (e.g., `scheduling.assignment`)
   - `module`: Identity (canonical_name, storage_name, storage_table)
   - `ownership`: Aggregate and bounded context
   - `stability`: Level, since, ADR reference
   - `lifecycle`: States, initial state, terminal states
   - `capabilities`: Boolean flags for each architectural layer
   - `aliases`: When domain name differs from storage name
   - `validation_profile`: strict | enterprise | legacy-compatible
   - `adr_references`: Links to ADRs

3. **Manifest Discovery**: Auto-discovered from `architecture/manifests/` directory. No central registry needed.

4. **Manifest Versioning**: `manifest_version: 1` field allows future schema evolution.

5. **Independent Validator**: `manifest_validator.py` validates manifests separately from the loader.

6. **Loader resolves paths**: `manifest_loader.py` tries multiple naming conventions (canonical, storage, plural) to find actual files.

### Architecture

```
architecture/
    manifests/
        doctor.yaml
        period.yaml
        shift.yaml
        assignment.yaml
    manifest_schema.yaml

tools/
    manifest_validator.py    # Independent validation
    manifest_loader.py       # Path resolution + caching
    validate_architecture.py # V2: Uses manifests
    golden_guard.py          # V2: Uses manifests
    compliance_report.py     # V2: Uses manifests
    architecture_score.py    # V2: Uses manifests
    docs_generator.py        # V2: Uses manifests
    lint_architecture.py     # V2: Uses manifests
    module_generator.py      # V2: Generates manifests
```

## Consequences

### Positive

- **Single source of truth**: All tools consume the same manifests
- **No naming assumptions**: Tools validate capabilities, not file names
- **Extensible**: New aggregates just need a new YAML file
- **Self-documenting**: Manifests describe the complete architecture
- **Future-proof**: Version field allows schema evolution
- **ADR traceability**: Each manifest links to its ADR

### Negative

- **Maintenance overhead**: Manifests must be kept in sync with code
- **Learning curve**: Developers must understand the manifest system

### Mitigations

- Integration tests verify manifests match actual codebase
- Module generator creates manifests automatically
- Manifest validator catches schema errors early

## Alternatives Considered

1. **Domain Alias Registry**: Central YAML mapping names. Rejected because it's a flat list, not a rich document.

2. **Hardcoded exceptions in tools**: Add `if module == "Assignment"` logic. Rejected because it doesn't scale.

3. **Convention-based resolution**: Always use `to_snake_case`. Rejected because it doesn't handle legitimate naming differences.

## References

- ADR-001: Monolito Modular
- ADR-012: Period Aggregate
- ADR-013: Domain Core
- ADR-014: Shift Aggregate
- ADR-015: Assignment Domain
