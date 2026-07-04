# Database Quality Report

**Data:** 2026-06-24

---

## Integridade — 9/10

| Critério | Nota | Justificativa |
|----------|------|---------------|
| PKs definidas | ✅ | Todas as tabelas possuem PK |
| FKs com ON DELETE | ✅ | RESTRICT ou CASCADE definido |
| CHECK constraints | ✅ | hour_rate, month, year, start_time < end_time |
| UNIQUE constraints | ✅ | crm, (year,month), (shift_date,shift_type) |
| NOT NULL | ✅ | Todos os campos obrigatórios marcados |

**Dedução:** 1 ponto — falta CHECK em shift_extras.justification (length > 0)

---

## Performance — 8/10

| Critério | Nota | Justificativa |
|----------|------|---------------|
| Índices em FKs | ✅ | Todos os indexes criados |
| Índices compostos | ✅ | (period_id,shift_date), (doctor_id,shift_id) |
| Índices para relatórios | ✅ | (status), (shift_date) |
| lazy loading | ✅ | selectin em todos os relationships |

**Dedução:** 2 pontos — sem índices para full-text search (name)

---

## Evolução — 9/10

| Critério | Nota | Justificativa |
|----------|------|---------------|
| Timestamps | ✅ | created_at e updated_at em todas as tabelas |
| Soft delete | ✅ | active em doctors |
| Flexibilidade | ✅ | VARCHAR para enums (compatível SQLite/PG) |
| Migrations | ✅ | Alembic configurado |

**Dedução:** 1 ponto — sem campo `version` para optimistic locking

---

## Remuneração — 7/10

| Critério | Nota | Justificativa |
|----------|------|---------------|
| hour_rate | ✅ | Doctor.hour_rate com CHECK >= 0 |
| ShiftPart horas | ✅ | start_time/end_time com CHECK |
| ShiftExtra horas | ⚠️ | **duration_minutes AUSENTE** |
| Cálculo viável | ⚠️ | Depende de adicionar campo |

**Dedução:** 3 pontos — ShiftExtra sem duração

---

## Relatórios — 8/10

| Critério | Nota | Justificativa |
|----------|------|---------------|
| Query por médico | ✅ | Índices adequados |
| Query por período | ✅ | Índices adequados |
| Query por tipo | ✅ | shift_type indexável |
| Agregações | ✅ | Campos numéricos adequados |

**Dedução:** 2 pontos — sem campo `sector` para relatórios por setor

---

## Importação Legada — 8/10

| Critério | Nota | Justificativa |
|----------|------|---------------|
| Campos compatíveis | ✅ | Nomes genéricos |
| Tipos flexíveis | ✅ | VARCHAR para enums |
| Sem auto-incremento UUID | ✅ | INTEGER PK compatível |

**Dedução:** 2 pontos — ShiftExtra sem duração dificulta importação

---

## Nota Final

| Categoria | Nota |
|-----------|------|
| Integridade | 9/10 |
| Performance | 8/10 |
| Evolução | 9/10 |
| Remuneração | 7/10 |
| Relatórios | 8/10 |
| Importação Legada | 8/10 |
| **Média** | **8.2/10** |

---

## Ações Críticas

1. **ADICIONAR `duration_minutes` em shift_extras** — Nota sobe para 9/10
2. Migration incremental para o ajuste
