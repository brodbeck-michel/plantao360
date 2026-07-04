# Database Review v1 — Revisão Crítica de Modelagem

**Data:** 2026-06-24
**Escopo:** 5 tabelas do domínio Plantão 360

---

## Modelo Atual (DOC-02)

### doctors
| Coluna | Tipo | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| name | VARCHAR(255) | NOT NULL |
| crm | VARCHAR(20) | UNIQUE, NOT NULL |
| hour_rate | NUMERIC(10,2) | NOT NULL |
| active | BOOLEAN | DEFAULT true |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

### periods
| Coluna | Tipo | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| year | INTEGER | NOT NULL |
| month | INTEGER | NOT NULL |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'draft' |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |
| | | UNIQUE(year, month) |

### shifts
| Coluna | Tipo | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| period_id | INTEGER | FK -> periods, NOT NULL |
| shift_date | DATE | NOT NULL |
| shift_type | VARCHAR(5) | NOT NULL |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |
| | | UNIQUE(shift_date, shift_type) |

### shift_parts
| Coluna | Tipo | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| shift_id | INTEGER | FK -> shifts, NOT NULL |
| doctor_id | INTEGER | FK -> doctors, NOT NULL |
| start_time | TIME | NOT NULL |
| end_time | TIME | NOT NULL |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

### shift_extras
| Coluna | Tipo | Constraints |
|--------|------|-------------|
| id | INTEGER | PRIMARY KEY |
| shift_id | INTEGER | FK -> shifts, NOT NULL |
| doctor_id | INTEGER | FK -> doctors, NOT NULL |
| justification | TEXT | NOT NULL |
| created_at | TIMESTAMP | |
| updated_at | TIMESTAMP | |

---

## Problemas Identificados

### P1: doctors.hour_rate pode ser negativo
**Severidade:** Alta
**Impacto:** Valores negativos aceitos incorretamente
**Solução:** CHECK(hour_rate >= 0)

### P2: periods.month sem validação de range
**Severidade:** Alta
**Impacto:** Valores como 0, 13, -1 aceitos
**Solução:** CHECK(month BETWEEN 1 AND 12)

### P3: periods.year sem validação de range
**Severidade:** Média
**Impacto:** Anos absurdos aceitos
**Solução:** CHECK(year BETWEEN 2000 AND 2100)

### P4: shift_parts.start_time < end_time não validado
**Severidade:** Alta
**Impacto:** Plantão com fim antes do início
**Solução:** CHECK(start_time < end_time)

### P5: shift_extras.justification pode ser vazia
**Severidade:** Média
**Impacto:**.justificativa em branco aceita
**Solução:** CHECK(length(justification) > 0) ou application-level

### P6: Índices compostos ausentes
**Severidade:** Média
**Impacto:** Queries lentas em relatórios
**Solução:** Adicionar índices:
- (period_id, shift_date)
- (doctor_id, shift_date)
- (shift_id) em shift_parts

### P7: created_at/updated_at sem default
**Severidade:** Média
**Impacto:** Campos podem ser NULL
**Solução:** DEFAULT CURRENT_TIMESTAMP

### P8: Sem ON DELETE para FKs
**Severidade:** Média
**Impacto:** Comportamento indefinido ao deletar registro pai
**Solução:** Definir CASCADE ou RESTRICT explicitamente

### P9: shift_type como VARCHAR sem validação de enum
**Severidade:** Baixa
**Impacto:** Valores inválidos aceitos
**Solução:** Usar Enum do SQLAlchemy ou CHECK constraint

### P10: period.status como VARCHAR sem validação de enum
**Severidade:** Baixa
**Impacto:** Valores inválidos aceitos
**Solução:** Usar Enum do SQLAlchemy ou CHECK constraint

---

## Melhorias Recomendadas

| ID | Melhoria | Prioridade | Status |
|----|----------|------------|--------|
| M1 | CHECK(hour_rate >= 0) | Alta | Aprovada |
| M2 | CHECK(month BETWEEN 1 AND 12) | Alta | Aprovada |
| M3 | CHECK(start_time < end_time) | Alta | Aprovada |
| M4 | Índices compostos | Média | Aprovada |
| M5 | ON DELETE para FKs | Média | Aprovada |
| M6 | Timestamps com default | Média | Aprovada |
| M7 | Enum type para shift_type | Baixa | Documentada |
| M8 | Enum type para period.status | Baixa | Documentada |
| M9 | CHECK(year range) | Baixa | Documentada |
| M10 | CHECK(justification length) | Baixa | Documentada |

---

## Melhorias Aprovadas para Implementação

1. **M1:** CHECK(hour_rate >= 0)
2. **M2:** CHECK(month BETWEEN 1 AND 12)
3. **M3:** CHECK(start_time < end_time)
4. **M4:** Índices (period_id, shift_date), (doctor_id, shift_date), (shift_id)
5. **M5:** ON DELETE RESTRICT para todas as FKs
6. **M6:** created_at DEFAULT CURRENT_TIMESTAMP, updated_at DEFAULT CURRENT_TIMESTAMP

---

## Melhorias Apenas Documentadas

1. **M7:** Enum SQLAlchemy para shift_type — Usar CHECK constraint por compatibilidade SQLite
2. **M8:** Enum SQLAlchemy para period.status — Usar CHECK constraint por compatibilidade SQLite
3. **M9:** CHECK(year BETWEEN 2000 AND 2100) — Aceitável sem validação agora
4. **M10:** CHECK(justification length) — Validação a nível de aplicação

---

## Preparação PostgreSQL

| Ponto | Status | Nota |
|-------|--------|------|
| VARCHAR sem tamanho | ✅ | Funciona em ambos |
| BOOLEAN | ✅ | Funciona em ambos |
| NUMERIC | ✅ | Funciona em ambos |
| DATE/TIME/TIMESTAMP | ✅ | Funciona em ambos |
| SERIAL vs INTEGER PK | ✅ | INTEGER PK + sequence compatível |
| CHECK constraints | ✅ | Funciona em ambos |
| ENUMs | ⚠️ | SQLite não suporta ENUM nativo — usar VARCHAR + CHECK |
