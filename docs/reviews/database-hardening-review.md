# Database Hardening Review

**Data:** 2026-06-24
**Escopo:** Auditoria completa da modelagem Sprint 1

---

## Doctor

| Campo | Tipo | Avaliação |
|-------|------|-----------|
| id | INTEGER PK | ✅ Adequado |
| name | VARCHAR(255) | ✅ Adequado |
| crm | VARCHAR(20) UNIQUE | ✅ Adequado |
| hour_rate | NUMERIC(10,2) | ✅ Adequado, CHECK >= 0 |
| active | BOOLEAN | ✅ Soft delete |
| created_at | TIMESTAMP | ✅ server_default |
| updated_at | TIMESTAMP | ✅ server_default + onupdate |

**Avaliação:** Modelo completo para remuneração.

---

## Period

| Campo | Tipo | Avaliação |
|-------|------|-----------|
| id | INTEGER PK | ✅ Adequado |
| year | INTEGER | ✅ CHECK 2000-2100 |
| month | INTEGER | ✅ CHECK 1-12 |
| status | VARCHAR(20) | ✅ PeriodStatus enum |
| created_at | TIMESTAMP | ✅ server_default |
| updated_at | TIMESTAMP | ✅ server_default + onupdate |
| UNIQUE(year, month) | | ✅ Prevenção de duplicatas |

**Avaliação:** Modelo completo para controle de períodos.

---

## Shift

| Campo | Tipo | Avaliação |
|-------|------|-----------|
| id | INTEGER PK | ✅ Adequado |
| period_id | FK periods | ✅ RESTRICT |
| shift_date | DATE | ✅ Adequado |
| shift_type | VARCHAR(5) | ✅ ShiftType enum |
| created_at | TIMESTAMP | ✅ server_default |
| updated_at | TIMESTAMP | ✅ server_default + onupdate |
| UNIQUE(shift_date, shift_type) | | ✅ Um plantão por tipo/dia |

**Avaliação:** Modelo adequado. UNIQUE impede dois T1 no mesmo dia.

---

## ShiftPart

| Campo | Tipo | Avaliação |
|-------|------|-----------|
| id | INTEGER PK | ✅ Adequado |
| shift_id | FK shifts | ✅ CASCADE |
| doctor_id | FK doctors | ✅ RESTRICT |
| start_time | TIME | ✅ Adequado |
| end_time | TIME | ✅ CHECK start_time < end_time |
| created_at | TIMESTAMP | ✅ server_default |
| updated_at | TIMESTAMP | ✅ server_default + onupdate |

**Avaliação:** Modelo completo. Horas calculáveis via (end_time - start_time).

---

## ShiftExtra

| Campo | Tipo | Avaliação |
|-------|------|-----------|
| id | INTEGER PK | ✅ Adequado |
| shift_id | FK shifts | ✅ CASCADE |
| doctor_id | FK doctors | ✅ RESTRICT |
| justification | TEXT | ✅ Adequado |
| created_at | TIMESTAMP | ✅ server_default |
| updated_at | TIMESTAMP | ✅ server_default + onupdate |

**Avaliação:** ⚠️ **CAMPO AUSENTE: duration_minutes**
Sem duração, é impossível calcular remuneração de extras.

---

## Respostas Obrigatórias

### O modelo suporta remuneração?
**Parcial.** ShiftPart sim (start_time/end_time). ShiftExtra NÃO — falta duração.

### O modelo suporta auditoria?
**Sim.** Timestamps em todas as tabelas. Audit model separado.

### O modelo suporta importação de legado?
**Sim.** Campos suficientes. Estrutura flexível.

### O modelo suporta crescimento futuro?
**Sim.** Índices adequados. Estrutura normalizada.

### Existem campos ausentes?
**SIM — duration_minutes em shift_extras.**

### Existem constraints ausentes?
Não. Constraints atuais são suficientes.

---

## Melhorias Aprovadas

1. **Adicionar `duration_minutes` em shift_extras** — CRÍTICO
2. **Migration incremental** — Não alterar migration inicial

## Melhorias Documentadas (sem implementação)

1. Adicionar `total_hours` em shift_parts (computado)
2. Adicionar campo `sector` em shifts (futuro multi-setor)
