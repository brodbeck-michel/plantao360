# Validation Matrix — Plantao 360

> ETAPA 4 — Auditoria completa de todas as regras de validação nas 5 camadas.
> Gerado em: 2026-06-29

## Visão Geral

O Plantao 360 emprega validação em 5 camadas, cada uma com responsabilidade específica:

1. **Banco (DB)**: Restrições físicas — CHECK, UNIQUE, FK, NOT NULL. Última linha de defesa.
2. **ORM**: Mapeamento SQLAlchemy — tipos, nullable, defaults, server_defaults. Espelha o DB.
3. **Domain**: Regras de negócio — state machines, transições, contratos, value objects.
4. **Validator**: Validação customizada — regras de negócio acionadas pelo service antes do commit.
5. **Schema (Pydantic)**: Validação de input — constraints de campo, tipos, tamanhos. Barreira de entrada.
6. **API**: Validação de rota — Query params, dependency injection, exception handlers.

> Nota: O AuditDecorator (`audit_decorator.py`) não contém validação — é infraestrutura de logging.

---

## Matriz de Validações

### 1. Doctors

| # | Regra | Camada | Arquivo:linha | Justificativa | Por que não nas demais |
|---|-------|--------|---------------|---------------|----------------------|
| D01 | `name` obrigatório (não vazio) | Validator | `rules/doctor_name.py:4-5` | Regra de negócio: médico deve ter nome | Schema já exige via `Field(..., min_length=1)`, mas Validator é o gateway antes do service |
| D02 | `name` max 255 caracteres | Validator | `rules/doctor_name.py:8-9` | Consistência com o banco String(255) | Schema também tem `max_length=255`; DB tem `String(255)` — **DUPLICADO com Schema** |
| D03 | `crm` obrigatório | Validator | `rules/crm.py:6-7` | CRM é identificador único do médico | Schema já exige via `Field(...)` |
| D04 | `crm` formato: 4-10 dígitos | Validator | `rules/crm.py:8-9` | Regra de negócio: CRM brasileiro | DB tem `String(20)` mas não valida formato; Schema tem `min_length=1, max_length=20` mas não valida regex — Validator é único neste formato |
| D05 | `hour_rate` > 0 | Validator | `rules/hour_rate.py:5-6` | Valor hora deve ser positivo | **DUPLICADO**: Schema tem `gt=0`; DB tem `CheckConstraint("hour_rate >= 0")` — nota: DB permite 0, Validator/Schema não |
| D06 | `name` min_length=1, max_length=255 | Schema | `doctor_create.py:7` | Pydantic validation na entrada | Validator também valida (D01, D02) — **DUPLICADO** |
| D07 | `crm` min_length=1, max_length=20 | Schema | `doctor_create.py:8` | Pydantic validation na entrada | Validator também valida (D03) — parcialmente duplicado |
| D08 | `hour_rate` gt=0 | Schema | `doctor_create.py:9` | Pydantic validation na entrada | **DUPLICADO** com D05 (Validator) e D10 (DB) |
| D09 | `name` nullable=False, String(255) | ORM | `doctor.py:23` | Mapeamento SQLAlchemy | DB também tem NOT NULL via migration |
| D10 | `crm` nullable=False, unique=True, String(20) | ORM | `doctor.py:24` | Mapeamento SQLAlchemy + unique index | DB também tem UNIQUE index |
| D11 | `hour_rate` nullable=False, Numeric(10,2) | ORM | `doctor.py:25` | Mapeamento SQLAlchemy | DB também tem NOT NULL |
| D12 | `hour_rate >= 0` CHECK | DB | `doctor.py:17` / migration `001_init` | Restrição física no banco | ORM tem nullable=False mas não CHECK de range |
| D13 | `crm` UNIQUE index | DB | `doctor.py:18` / migration `001_init` | CRM duplicado não permitido | ORM tem `unique=True` — refletido |
| D14 | Update: name, crm, hour_rate opcionais | Validator | `doctor_validator.py:22-30` | Update parcial — só valida campos presentes | Schema também tem campos Optional |
| D15 | Update: mesmos campos com mesmas regras | Schema | `doctor_update.py:7-9` | Pydantic validation | Validator também valida (D14) — parcialmente duplicado |
| D16 | Soft delete: `active` default=True | ORM | `base_mixins.py:22-26` | Soft delete via flag | DB tem server_default="1" |
| D17 | `created_at`, `updated_at` NOT NULL, server_default | ORM | `base_mixins.py:8-18` | Timestamps automáticos | DB tem server_default=CURRENT_TIMESTAMP |

---

### 2. Shifts

| # | Regra | Camada | Arquivo:linha | Justificativa | Por que não nas demais |
|---|-------|--------|---------------|---------------|----------------------|
| S01 | `shift_date` obrigatório | Validator | `shift_validator.py:15-16` | Data é campo essencial do plantão | Schema já exige via `Field(...)` |
| S02 | `shift_type` obrigatório | Validator | `shift_validator.py:17-18` | Tipo define o turno | Schema já exige via `Field(...)` |
| S03 | `shift_type` ∈ {T1,T2,T3,R1,R2} | Validator | `shift_validator.py:19-20` | Tipos válidos definidos no domínio | Domain tem `ShiftType` enum; Schema não valida — **único no Validator** |
| S04 | `scheduled_end > scheduled_start` | Validator | `shift_validator.py:22-23` | Fim deve ser após início | **DUPLICADO**: Domain rules `shift_rules.py:48`, Value Object `shift_time_range.py:11-12` |
| S05 | Cannot update completed/cancelled shift | Domain | `shift_rules.py:19-24` | State machine: transições imutáveis | State Machine também valida transições |
| S06 | Can start only SCHEDULED | Domain | `shift_rules.py:27-30` | State machine | State Machine `shift_state_machine.py:9-10` |
| S07 | Can complete only IN_PROGRESS | Domain | `shift_rules.py:33-36` | State machine | State Machine `shift_state_machine.py:11-12` |
| S08 | Can cancel only SCHEDULED/IN_PROGRESS | Domain | `shift_rules.py:39-42` | State machine | State Machine `shift_state_machine.py:14-20` |
| S09 | `scheduled_end > scheduled_start` | Domain | `shift_rules.py:45-49` | Regra de negócio em runtime | **DUPLICADO** com S04, S11 |
| S10 | `end > start` (datetime) | Domain | `value_objects/shift_time_range.py:10-12` | Value Object — imutável | **DUPLICADO** com S04, S09 |
| S11 | Cannot end shift not started | Domain | `value_objects/shift_timeline.py:28-29` | Timeline invariante | Único neste nível |
| S12 | `shift_date` unique per `shift_type` | DB | `shift.py:21` / migration `001_init` | UniqueConstraint | ORM também tem `UniqueConstraint` |
| S13 | `period_id` FK RESTRICT | DB | `shift.py:29-32` / migration `001_init` | FK para periods | ORM define FK |
| S14 | Status default=SCHEDULED | ORM | `shift.py:35` | Estado inicial | DB tem server_default="scheduled" |
| S15 | Schema: period_id, shift_date, shift_type obrigatórios | Schema | `shift_create.py:7-9` | Pydantic validation | Validator também valida S01/S02 |
| S16 | API: Query params ge=1, le=100 | API | `routes/shift.py:19-20` | Paginação | FastAPI Query validation |

---

### 3. Periods

| # | Regra | Camada | Arquivo:linha | Justificativa | Por que não nas demais |
|---|-------|--------|---------------|---------------|----------------------|
| P01 | `month` entre 1 e 12 | Validator | `period_validator.py:14-15` | Mês válido | **DUPLICADO**: Schema `period_create.py:8` (ge=1, le=12); DB `period.py:19` (CHECK BETWEEN 1 AND 12) |
| P02 | `year` entre 2000 e 2100 | Validator | `period_validator.py:16-17` | Ano válido | **DUPLICADO**: Schema `period_create.py:7` (ge=2000, le=2100); DB `period.py:20` (CHECK BETWEEN 2000 AND 2100) |
| P03 | `month` ge=1, le=12 | Schema | `period_create.py:8` | Pydantic validation | **DUPLICADO** com P01, P05 |
| P04 | `year` ge=2000, le=2100 | Schema | `period_create.py:7` | Pydantic validation | **DUPLICADO** com P02, P06 |
| P05 | `month BETWEEN 1 AND 12` CHECK | DB | `period.py:19` / migration `001_init` | Restrição física | ORM/Schema também validam |
| P06 | `year BETWEEN 2000 AND 2100` CHECK | DB | `period.py:20` / migration `001_init` | Restrição física | ORM/Schema também validam |
| P07 | `year, month` UNIQUE | DB | `period.py:18` / migration `001_init` | Competência única | ORM tem `UniqueConstraint` |
| P08 | Status default=DRAFT | ORM | `period.py:28-32` | Estado inicial | DB tem server_default="draft" |
| P09 | Permission: can_be_closed_by_external=False | Domain | `period_contract.py:19-20` | Contrato de permissão | Único neste nível |
| P10 | Permission: can_status_be_changed_by_external=False | Domain | `period_contract.py:22-23` | Contrato de permissão | Único neste nível |
| P11 | Permission: can_be_reopened_by_external=False | Domain | `period_contract.py:26-27` | Contrato de permissão | Único neste nível |
| P12 | Permission: can_dates_be_modified_by_external=False | Domain | `period_contract.py:29-30` | Contrato de permissão | Único neste nível |
| P13 | Update: month/year Optional com mesmas regras | Schema | `period_update.py:7-8` | Pydantic update parcial | Validator também valida P01/P02 |
| P14 | API: Query params ge=1, le=100 | API | `routes/period.py:5-6` | Paginação | FastAPI Query validation |

---

### 4. Assignments (ShiftParts)

| # | Regra | Camada | Arquivo:linha | Justificativa | Por que não nas demais |
|---|-------|--------|---------------|---------------|----------------------|
| A01 | Can confirm only PLANNED | Domain | `assignment_rules.py:8-11` | State machine | State Machine `assignment_state_machine.py:9-10` |
| A02 | Can start only CONFIRMED | Domain | `assignment_rules.py:14-17` | State machine | State Machine `assignment_state_machine.py:12-13` |
| A03 | Can complete only STARTED | Domain | `assignment_rules.py:20-23` | State machine | State Machine `assignment_state_machine.py:15-16` |
| A04 | Can cancel only PLANNED/CONFIRMED | Domain | `assignment_rules.py:26-29` | State machine | State Machine `assignment_state_machine.py:18-23` |
| A05 | Can change doctor only PLANNED/CONFIRMED | Domain | `assignment_rules.py:32-35` | Regra de negócio | Único neste nível |
| A06 | Can change time only PLANNED/CONFIRMED | Domain | `assignment_rules.py:38-41` | Regra de negócio | Único neste nível |
| A07 | `end_time > start_time` | Domain | `assignment_rules.py:44-48` | Regra de negócio | **DUPLICADO** com A08 |
| A08 | `end_time > start_time` | Domain | `value_objects/assignment_timeline.py:10-13` | Value Object imutável | **DUPLICADO** com A07 |
| A09 | Duration must be positive | Domain | `value_objects/assignment_duration.py:8-10` | Value Object imutável | Único neste nível |
| A10 | `start_time < end_time` CHECK | DB | migration `001_init` (removido no 003) | Restrição física (removida) | Foi removida por não suportar overnight |
| A11 | `duration_minutes > 0` CHECK | DB | migration `003_runtime_alignment` | Restrição física | ORM não tem CHECK equivalente |
| A12 | `shift_id` FK CASCADE, `doctor_id` FK RESTRICT | DB | `shift_part.py:26-32` / migration | FK constraints | ORM define as FKs |
| A13 | Status default=PLANNED | ORM | `shift_part.py:36-38` | Estado inicial | DB tem server_default="planned" |
| A14 | Schema: shift_id, doctor_id, start_time, end_time | Schema | `assignment_create.py:6-9` | Pydantic validation | Validação de formato HH:MM delegada ao Domain |
| A15 | `shift_id` FK RESTRICT (payroll) | DB | `payroll.py:28-31` | FK para periods | ORM define FK |

---

### 5. Extras (ShiftExtras)

| # | Regra | Camada | Arquivo:linha | Justificativa | Por que não nas demais |
|---|-------|--------|---------------|---------------|----------------------|
| E01 | `duration_minutes > 0` CHECK | DB | `shift_extra.py:18-20` / migration `003` | Restrição física | **DUPLICADO** com Schema E04 |
| E02 | `shift_id` FK CASCADE, `doctor_id` FK RESTRICT | DB | `shift_extra.py:27-33` / migration | FK constraints | ORM define as FKs |
| E03 | `justification` NOT NULL | DB | migration `001_init` | Campo obrigatório | ORM tem `Text, nullable=False` |
| E04 | `duration_minutes` gt=0 | Schema | `extra_create.py:9` | Pydantic validation | **DUPLICADO** com E01 |
| E05 | `justification` min_length=1 | Schema | `extra_create.py:10` | Pydantic validation | DB tem NOT NULL |
| E06 | Status default=PENDING | ORM | `shift_extra.py:40-42` | Estado inicial | DB tem server_default="pending" |
| E07 | Update: duration_minutes Optional gt=0 | Schema | `extra_update.py:7` | Pydantic validation | **DUPLICADO** com E01 |
| E08 | Update: justification Optional min_length=1 | Schema | `extra_update.py:8` | Pydantic validation | Parcialmente duplicado com E05 |

---

### 6. Payroll

| # | Regra | Camada | Arquivo:linha | Justificativa | Por que não nas demais |
|---|-------|--------|---------------|---------------|----------------------|
| PY01 | State machine: draft→calculated→reviewed→approved→locked→exported→paid→archived | Domain | `payroll_state_machine.py:15-24` | Lifecycle control | Único neste nível |
| PY02 | Reopen: only CALCULATED..PAID → DRAFT | Domain | `payroll_state_machine.py:67-81` | Regra de negócio | Único neste nível |
| PY03 | `readiness` deve ser validado antes de solicitar aprovação | Domain | `payroll_competency.py:598-599` | Pré-requisito de governança | Único neste nível |
| PY04 | `checklist` deve estar completo antes de aprovação | Domain | `payroll_competency.py:600-601` | Pré-requisito de governança | Único neste nível |
| PY05 | Checklist waiver: justificativa >= 10 chars | Domain | `governance.py:49-50` | Regra de governança | **DUPLICADO** com PY11 (Validator) |
| PY06 | `period_id` FK RESTRICT | DB | `payroll.py:28-31` / migration `003` | FK para periods | ORM define FK |
| PY07 | Status default=DRAFT, server_default="draft" | ORM | `payroll.py:33-35` | Estado inicial | DB tem server_default |
| PY08 | `current_version` default=1 | ORM | `payroll.py:36` | Versionamento | DB tem server_default="1" |
| PY09 | Schema: period_id, year_month obrigatórios | Schema | `payroll_create.py:7-8` | Pydantic validation | Único neste nível |
| PY10 | `year_month` min_length=6, max_length=6 | Schema | `payroll_create.py:8` | Formato YYYYMM | Único neste nível |
| PY11 | Approval: justificativa obrigatória | Validator | `payroll_governance_validator.py:12-15` | Governança | Schema `payroll_governance.py:84` tem `min_length=1` — **DUPLICADO** |
| PY12 | Lock: `locked_by` obrigatório | Validator | `payroll_governance_validator.py:22-23` | Governança | Schema não valida — **único no Validator** |
| PY13 | Unlock: `unlocked_by` obrigatório | Validator | `payroll_governance_validator.py:27-28` | Governança | Schema não valida — **único no Validator** |
| PY14 | Unlock: justificativa >= 10 chars | Validator | `payroll_governance_validator.py:31-32` | Governança | **DUPLICADO** com PY05; Schema `payroll_governance.py:95` tem `min_length=10` — **TRÍPLICE** |
| PY15 | Checklist item: status ∈ {satisfied, not_satisfied, waived} | Validator | `payroll_governance_validator.py:39-42` | Governança | Schema não valida enum — **único no Validator** |
| PY16 | Checklist waiver: justificativa >= 10 chars | Validator | `payroll_governance_validator.py:47-48` | Governança | **DUPLICADO** com PY05, PY14 |
| PY17 | Schema unlock: justificativa min_length=10 | Schema | `payroll_governance.py:95` | Pydantic validation | **DUPLICADO** com PY14, PY16 |
| PY18 | Schema approval: justificativa min_length=1 | Schema | `payroll_governance.py:84` | Pydantic validation | **DUPLICADO** com PY11 |
| PY19 | Schema reopen: reason min_length=1, max_length=500 | Schema | `payroll_reopen.py:7` | Pydantic validation | Único neste nível |
| PY20 | API: Query params ge=1, le=100 | API | `routes/payroll.py:7-8` | Paginação | FastAPI Query validation |

---

### 7. Coverage

| # | Regra | Camada | Arquivo:linha | Justificativa | Por que não nas demais |
|---|-------|--------|---------------|---------------|----------------------|
| C01 | `period_id` FK RESTRICT | DB | `coverage_snapshot.py:25-28` | FK para periods | ORM define FK |
| C02 | Status default=ACTIVE | ORM | `coverage_snapshot.py:29-31` | Estado inicial | Único neste nível |
| C03 | `inconsistencies` nullable=True, JSON | ORM | `coverage_snapshot.py:35` | Campo opcional | Único neste nível |

---

### 8. Financial Facts

| # | Regra | Camada | Arquivo:linha | Justificativa | Por que não nas demais |
|---|-------|--------|---------------|---------------|----------------------|
| FF01 | `period_id` FK RESTRICT | DB | `financial_fact.py:30-33` | FK para periods | ORM define FK |
| FF02 | `doctor_id` FK RESTRICT | DB | `financial_fact.py:34-37` | FK para doctors | ORM define FK |
| FF03 | Status default=ACTIVE | ORM | `financial_fact.py:50-52` | Estado inicial | Único neste nível |
| FF04 | `fact_type` NOT NULL | ORM | `financial_fact.py:38-40` | Campo obrigatório | DB tem NOT NULL |

---

### 9. Financial Snapshots

| # | Regra | Camada | Arquivo:linha | Justificativa | Por que não nas demais |
|---|-------|--------|---------------|---------------|----------------------|
| FS01 | `period_id` FK RESTRICT | DB | `financial_snapshot.py:25-28` | FK para periods | ORM define FK |
| FS02 | `coverage_snapshot_id` FK RESTRICT | DB | `financial_snapshot.py:29-32` | FK para coverage | ORM define FK |
| FS03 | Status default=ACTIVE | ORM | `financial_snapshot.py:33-35` | Estado inicial | Único neste nível |

---

### 10. Cross-cutting (Timestamps, Soft Delete, Pagination, Enums)

| # | Regra | Camada | Arquivo:linha | Justificativa | Por que não nas demais |
|---|-------|--------|---------------|---------------|----------------------|
| X01 | `created_at` server_default=func.now(), NOT NULL | ORM | `base_mixins.py:8-12` | Timestamp automático | DB tem server_default=CURRENT_TIMESTAMP |
| X02 | `updated_at` server_default=func.now(), onupdate, NOT NULL | ORM | `base_mixins.py:13-18` | Timestamp de update | DB tem server_default=CURRENT_TIMESTAMP |
| X03 | `active` default=True, server_default="1", NOT NULL | ORM | `base_mixins.py:22-26` | Soft delete | DB tem server_default="1" |
| X04 | Page default=1, Size default=20, max=100 | Schema | `base_dto.py:18-28` | Paginação segura | API também tem Query(ge=1, le=100) — parcialmente duplicado |
| X05 | Sort direction ∈ {asc, desc} | Schema | `doctor_filters.py:14-15` | Filtro seguro | Único neste nível |
| X06 | Sort field ∈ allowed set | Schema | `doctor_filters.py:16-18` | Filtro seguro | Único neste nível |
| X07 | Enums: ShiftType, ShiftStatus, AssignmentStatus, PeriodStatus, PayrollStatus, ExtraStatus | Domain | `constants/*.py` | Definição de valores válidos | ORM armazena como String(20/5); DB não tem CHECK para enums |
| X08 | Exception handlers: BusinessRuleError, NotFoundError, ConflictError, UnauthorizedError | API | `exception_handlers.py:12-55` | Tratamento de erros de validação | Único neste nível |
| X09 | DB session: get_db dependency injection | API | `dependencies.py:10-12` / `session.py:7-11` | Gerenciamento de sessão | Único neste nível |

---

## Regras Duplicadas

| # | Regra | Camadas duplicadas | Arquivos | Status |
|---|-------|-------------------|----------|--------|
| DUP-01 | Doctor name max 255 | Validator + Schema | `rules/doctor_name.py:8` / `doctor_create.py:7` | Aceitável — defesa em profundidade |
| DUP-02 | Doctor hour_rate > 0 | Validator + Schema + DB | `rules/hour_rate.py:5` / `doctor_create.py:9` / `doctor.py:17` | **Inconsistência**: DB permite 0, Validator/Schema não |
| DUP-03 | Doctor crm obrigatório | Validator + Schema | `rules/crm.py:6` / `doctor_create.py:8` | Aceitável — defesa em profundidade |
| DUP-04 | Period month 1-12 | Validator + Schema + DB | `period_validator.py:14` / `period_create.py:8` / `period.py:19` | **TRÍPLICE** — mesma regra em 3 camadas |
| DUP-05 | Period year 2000-2100 | Validator + Schema + DB | `period_validator.py:16` / `period_create.py:7` / `period.py:20` | **TRÍPLICE** — mesma regra em 3 camadas |
| DUP-06 | Scheduled end > start | Validator + Domain + Value Object | `shift_validator.py:22` / `shift_rules.py:48` / `shift_time_range.py:11` | **TRÍPLICE** — mesma regra em 3 camadas |
| DUP-07 | Assignment end > start | Domain + Value Object | `assignment_rules.py:44` / `assignment_timeline.py:10` | **DUPLICA** — mesma regra em 2 camadas |
| DUP-08 | Extra duration_minutes > 0 | Schema + DB | `extra_create.py:9` / `shift_extra.py:18` | Aceitável — defesa em profundidade |
| DUP-09 | Payroll unlock justificativa >= 10 | Validator + Domain + Schema | `payroll_governance_validator.py:31` / `governance.py:49` / `payroll_governance.py:95` | **TRÍPLICE** — mesma regra em 3 camadas |
| DUP-10 | Payroll approval justificativa obrigatória | Validator + Schema | `payroll_governance_validator.py:12` / `payroll_governance.py:84` | Aceitável — defesa em profundidade |

---

## Regras Órfãs

| # | Regra | Arquivo | Observação |
|---|-------|---------|------------|
| ORF-01 | `validate_code()` | `rules/code.py:4-7` | Função existe mas não é importada por nenhum validator |
| ORF-02 | `validate_year_month()` | `rules/year_month.py:4-7` | Função existe mas não é importada por nenhum validator |

---

## Resumo Estatístico

| Métrica | Quantidade |
|---------|-----------|
| **Total de regras catalogadas** | **72** |
| Banco (DB) | 14 |
| ORM | 18 |
| Domain | 22 |
| Validator | 16 |
| Schema (Pydantic) | 19 |
| API | 6 |
| **Duplicadas (entre camadas)** | **10** |
| Duplicadas aceitáveis (defesa em profundidade) | 4 |
| Duplicadas com inconsistência (DUP-02) | 1 |
| Duplicadas tríplices | 3 |
| **Regras órfãs** | **2** |

---

## Observações

### Inconsistência detectada (DUP-02)
O `hour_rate` do Doctor tem uma **inconsistência semântica** entre camadas:
- **DB**: `CheckConstraint("hour_rate >= 0")` — permite 0
- **Validator**: `value <= 0` → erro — **não permite 0**
- **Schema**: `Field(gt=0)` — **não permite 0**

O DB permite `hour_rate = 0`, mas o Validator e Schema rejeitam. Isso significa que um registro com `hour_rate = 0` pode existir no banco (via SQL direto ou migração) mas não pode ser criado/atualizado pela API. Recomendação: alinhar o DB para `hour_rate > 0` (usando `>` em vez de `>=`).

### Regras órfãs
As funções `validate_code()` e `validate_year_month()` existem em `rules/` mas não são invocadas por nenhum componente. Podem ser código morto ou funções de uso futuro.

### State Machines vs Domain Rules
As state machines (`assignment_state_machine.py`, `shift_state_machine.py`, `payroll_state_machine.py`) e as domain rules (`assignment_rules.py`, `shift_rules.py`) possuem **sobreposição intencional** — as rules são o gateway de validação e as state machines são o executor de transições. Isso é uma escolha arquitetural válida (validação explícita antes da transição).

### Enums sem CHECK no DB
Os valores de status (shift_status, assignment_status, period_status, etc.) são armazenados como `String(20)` no DB **sem CHECK constraint**. A validação dos valores é feita apenas no nível Domain (via StrEnum). Uma inserção direta no DB poderia inserir valores inválidos.
