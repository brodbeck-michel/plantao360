# Plantão 360 — Ubiquitous Language

## Core Entities

| Term | Definition |
|------|-----------|
| **Doctor** | A medical professional registered in the system with CRM, name, and hourly rate |
| **Period** | Monthly container (year/month) grouping all Shifts. Lifecycle: draft→closed→paid |
| **Shift** | A work assignment for a specific date and type (T1/T2/T3/R1/R2) within a Period |
| **ShiftPart** | A Doctor Assignment — allocates a Doctor to a Shift for specific hours |
| **ShiftExtra** | Additional work beyond scheduled ShiftParts, with justification and duration |

## Shift Types

| Type | Description |
|------|-------------|
| **T1** | Morning shift |
| **T2** | Afternoon shift |
| **T3** | Night shift |
| **R1** | Rest morning |
| **R2** | Rest afternoon |

## Assignment (ShiftPart) Concepts

| Term | Definition |
|------|-----------|
| **Assignment** | The act of allocating a Doctor to a Shift for specific hours |
| **AssignmentStatus** | Lifecycle: planned→confirmed→started→completed→cancelled |
| **Primary Doctor** | The main doctor assigned to a Shift (future concept) |
| **Backup Doctor** | A secondary doctor who can replace the primary (future concept) |
| **Coverage** | Whether a Shift has the minimum required number of Doctors |
| **Overlap** | When two Assignments for the same Doctor conflict in time |
| **Replacement** | Substituting one Doctor for another in an Assignment |
| **Duration** | Time between start_time and end_time, used for payroll calculation |

## Shift Lifecycle States

| State | Description |
|-------|-------------|
| **scheduled** | Shift is planned but not started |
| **in_progress** | Shift is actively being worked |
| **completed** | Shift has finished successfully |
| **cancelled** | Shift was cancelled before or during execution |

## Period Lifecycle States

| State | Description |
|-------|-------------|
| **draft** | Period is open for editing |
| **closed** | Period is finalized, no edits allowed |
| **paid** | Period has been processed for payment |

---

## Architecture Governance

| Term | Definition |
|------|-----------|
| **Module Manifest** | YAML file declaring an aggregate's complete architectural identity |
| **module_id** | Permanent stable identifier (e.g., `scheduling.assignment`) |
| **canonical_name** | Domain name used in code (e.g., `Assignment`) |
| **storage_name** | DB table/model name (e.g., `shift_part`) |
| **capabilities** | Architectural layers declared by a manifest (model, repository, service, etc.) |
| **Manifest Loader** | Component that resolves capabilities to actual file paths |
| **Manifest Validator** | Independent tool that validates manifest schema and coherence |
| **Manifest Discovery** | Auto-discovery of manifests from `architecture/manifests/` directory |
| **validation_profile** | Per-aggregate validation strictness (strict, enterprise, legacy-compatible) |
| **paid** | Period has been processed for payment |
