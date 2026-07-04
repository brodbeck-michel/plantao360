# Plantão 360 — Aggregate Interactions

## Doctor ↔ ShiftPart

```
Doctor reads: ShiftParts for a given Doctor
Doctor mutates: Never directly (via Use Cases only)
```

## Period ↔ Shift

```
Period reads: Shifts within year/month
Period mutates: Never directly (via Use Cases only)
Shift reads: Period for boundaries
```

## Shift ↔ ShiftPart

```
Shift reads: ShiftParts as children (aggregate)
Shift mutates: ShiftParts lifecycle
ShiftPart reads: Shift for date/type/reference
ShiftPart mutates: Own status only
```

## ShiftPart ↔ Doctor

```
ShiftPart reads: Doctor for name/CRM
ShiftPart mutates: Never (Doctor is separate Aggregate)
```

## ShiftPart ↔ Period

```
ShiftPart reads: Period indirectly via Shift
ShiftPart mutates: Never
```

## Events Flow

```
Doctor events → Doctor module
Period events → Period module
Shift events → Shift module
Assignment events → Assignment module (ShiftPart)
```

## Coverage & Overlap

```
CoveragePolicy checks: minimum doctor count per Shift
OverlapDetector checks: time conflicts for same Doctor
Both are read-only: they never mutate state
```
