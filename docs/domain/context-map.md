# Plantão 360 — Context Map

## Module Relationships

```
┌─────────┐     ┌──────────┐     ┌──────────┐
│  Doctor  │────<│  Shift   │────<│  Period  │
└─────────┘     └──────────┘     └──────────┘
     │               │
     │               │
     └───────┬───────┘
             │
        ┌─────────┐
        │ ShiftPart│ (Assignment)
        └─────────┘
             │
        ┌─────────┐
        │ShiftExtra│
        └─────────┘
```

## Aggregate Boundaries

| Aggregate | Root Entity | Child Entities |
|-----------|-------------|----------------|
| Doctor | Doctor | — |
| Period | Period | — |
| Shift | Shift | ShiftPart, ShiftExtra |
| Assignment | ShiftPart | — |

## Cross-Aggregate Interactions

| From | To | Type | Description |
|------|-----|------|-------------|
| ShiftPart | Shift | Read (FK) | ShiftPart reads Shift for date/type |
| ShiftPart | Doctor | Read (FK) | ShiftPart reads Doctor for name/CRM |
| ShiftPart | Period | Indirect | Via Shift → Period |
| Shift | Period | Read (FK) | Shift reads Period for year/month |
| ShiftExtra | Shift | Read (FK) | ShiftExtra reads Shift |
| ShiftExtra | Doctor | Read (FK) | ShiftExtra reads Doctor |

## Rules

1. No entity may directly mutate another Aggregate's state
2. All mutations occur through Use Cases
3. ShiftPart queries Shift/Doctor but never modifies them
4. Period lifecycle affects Shift availability
5. Doctor deactivation does not delete existing ShiftParts
