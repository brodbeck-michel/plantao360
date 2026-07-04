# Remuneration Query Analysis

**Data:** 2026-06-24

---

## Consulta 1: Plantões de um médico

```sql
SELECT sp.*, s.shift_date, s.shift_type
FROM shift_parts sp
JOIN shifts s ON sp.shift_id = s.id
WHERE sp.doctor_id = ?
ORDER BY s.shift_date;
```

| Índice Utilizado | Complexidade |
|------------------|--------------|
| ix_shift_parts_doctor_id | O(1) lookup + O(n) sort |

**Status:** ✅ Otimizado

---

## Consulta 2: Plantões de um período

```sql
SELECT s.*, sp.start_time, sp.end_time, d.name
FROM shifts s
JOIN shift_parts sp ON sp.shift_id = s.id
JOIN doctors d ON sp.doctor_id = d.id
WHERE s.period_id = ?
ORDER BY s.shift_date;
```

| Índice Utilizado | Complexidade |
|------------------|--------------|
| ix_shifts_period_id | O(1) lookup + O(n) sort |

**Status:** ✅ Otimizado

---

## Consulta 3: Extras de um médico

```sql
SELECT se.*, s.shift_date, s.shift_type
FROM shift_extras se
JOIN shifts s ON se.shift_id = s.id
WHERE se.doctor_id = ?
ORDER BY s.shift_date;
```

| Índice Utilizado | Complexidade |
|------------------|--------------|
| ix_shift_extras_doctor_id | O(1) lookup + O(n) sort |

**Status:** ✅ Otimizado

---

## Consulta 4: Remuneração mensal por médico

```sql
SELECT
    d.id,
    d.name,
    d.hour_rate,
    SUM(EXTRACT(EPOCH FROM (sp.end_time - sp.start_time)) / 3600) as total_hours,
    SUM(EXTRACT(EPOCH FROM (sp.end_time - sp.start_time)) / 3600) * d.hour_rate as total_remuneration
FROM doctors d
JOIN shift_parts sp ON sp.doctor_id = d.id
JOIN shifts s ON sp.shift_id = s.id
WHERE s.period_id = ?
GROUP BY d.id, d.name, d.hour_rate;
```

| Índice Utilizado | Complexidade |
|------------------|--------------|
| ix_shift_parts_doctor_id | O(n) scan + O(n) group |

**Status:** ✅ Aceitável para volumes atuais

---

## Consulta 5: Extras para remuneração

```sql
SELECT
    se.doctor_id,
    d.hour_rate,
    se.duration_minutes,
    (se.duration_minutes / 60.0) * d.hour_rate as extra_value
FROM shift_extras se
JOIN doctors d ON se.doctor_id = d.id
WHERE se.shift_id IN (
    SELECT id FROM shifts WHERE period_id = ?
);
```

| Índice Utilizado | Complexidade |
|------------------|--------------|
| ix_shift_extras_shift_id | O(1) lookup |

**Status:** ⚠️ Depende de `duration_minutes` (campo a ser adicionado)

---

## Resumo

| Query | Índice | Status |
|-------|--------|--------|
| Plantões por médico | ix_shift_parts_doctor_id | ✅ |
| Plantões por período | ix_shifts_period_id | ✅ |
| Extras por médico | ix_shift_extras_doctor_id | ✅ |
| Remuneração mensal | ix_shift_parts_doctor_id | ✅ |
| Remuneração extras | ix_shift_extras_shift_id | ⚠️ Precisa duration_minutes |
