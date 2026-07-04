# Shift Aggregate — Ubiquitous Language

| Term | Definition |
|------|-----------|
| **Shift** | A work assignment for a specific date and type (T1/T2/T3/R1/R2) within a Period |
| **ShiftType** | Classification: T1 (morning), T2 (afternoon), T3 (night), R1 (rest morning), R2 (rest afternoon) |
| **ShiftStatus** | Lifecycle state: scheduled → in_progress → completed → cancelled |
| **ShiftPart** | A time segment within a Shift, assigning a Doctor for specific hours |
| **ShiftExtra** | Additional work beyond scheduled ShiftParts, with justification and duration |
| **Period** | Monthly container (year/month) that groups all Shifts |
| **Doctor** | A professional assigned to ShiftParts within Shifts |

## Lifecycle States

| State | Description |
|-------|-------------|
| **scheduled** | Shift is planned but not started |
| **in_progress** | Shift is actively being worked |
| **completed** | Shift has finished successfully |
| **cancelled** | Shift was cancelled before or during execution |
