# Shift Module — Critical Review v1

**Date:** Sprint 4
**Author:** Architecture Team

---

## 1. Does the current model correctly represent an Aggregate?

**Answer: Partially.**

The current `shifts` table is a minimal CRUD model:
- `id`, `period_id`, `shift_date`, `shift_type`
- No lifecycle status
- No duration tracking
- No state management

An Aggregate requires:
- ✅ Identity (`id`)
- ✅ Reference to Period (`period_id`)
- ❌ Lifecycle status (missing)
- ❌ Duration information (missing — only in ShiftPart)
- ❌ Domain events (missing)
- ❌ Version for optimistic locking (missing)

**Verdict:** The model is a persistence skeleton, not an Aggregate. Must be enhanced.

---

## 2. Are there missing business rules?

**Yes, critically:**

| Rule | Status |
|------|--------|
| A shift belongs to exactly one period | ✅ Enforced (FK) |
| A shift has a unique date+type per period | ✅ Enforced (UNIQUE) |
| A shift can be started | ❌ No status field |
| A shift can be completed | ❌ No status field |
| A shift can be cancelled | ❌ No status field |
| Duration must be calculable | ❌ No duration fields |
| ShiftParts cannot overlap | ❌ Not enforced at model level |
| Doctor cannot be double-booked | ❌ Not enforced |
| Shift cannot be modified after completion | ❌ No lifecycle |

---

## 3. Are there undocumented invariants?

**Yes:**

1. A shift's date must fall within its period's year/month
2. A shift cannot have ShiftParts that overlap in time
3. A shift cannot be cancelled if it has already started
4. Duration is the sum of ShiftPart durations
5. A completed shift cannot receive new ShiftParts
6. A cancelled shift is immutable

---

## 4. Are there insufficient fields for lifecycle?

**Yes:**

Missing fields needed:
- `status` — lifecycle state (scheduled, in_progress, completed, cancelled)
- `scheduled_start` — when the shift starts (datetime)
- `scheduled_end` — when the shift ends (datetime)
- `actual_start` — when the shift actually started
- `actual_end` — when the shift actually ended

---

## 5. Are there excessive dependencies on Period or Doctor?

**No.** The current model only has a FK to Period. Doctor is accessed through ShiftPart. This is correct — Shift references Period, and ShiftPart references both Shift and Doctor.

---

## 6. Are there decisions that will complicate Payroll or Reports?

**Potential issues:**

1. **No duration at Shift level** — Payroll needs total hours per shift. Currently requires joining ShiftParts. Should add `total_duration_minutes` to Shift.
2. **No cost tracking** — Payroll will need cost per shift. Should prepare `total_cost` field.
3. **No doctor count** — Reports need number of doctors per shift. Should add `doctor_count`.

---

## Decisions Made

1. **Add `status` field** — lifecycle management
2. **Add `scheduled_start`/`scheduled_end`** — planned time range
3. **Add `actual_start`/`actual_end`** — actual time range
4. **Add `total_duration_minutes`** — computed from ShiftParts
5. **Add `doctor_count`** — computed from ShiftParts
6. **Keep `shift_type`** — it's a classification, not lifecycle
7. **Defer cost tracking** — belongs to Payroll sprint
8. **Defer overlap validation** — belongs to Allocation sprint

---

## Implementation Plan

1. Generate Shift module via IDP
2. Enhance model with lifecycle fields
3. Implement State Machine
4. Create Value Objects
5. Implement Use Cases
6. Add tests
