# Data Model — Log de auditoria das ações do usuário (spec 007)

**Data**: 2026-08-07 | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

## Tabela nova: `audit_logs`

Registro imutável de alteração. **Não** possui FK obrigatória para o recurso auditado — o rastro
precisa sobreviver à remoção do dado (FR-002 / SC-002).

| Coluna | Tipo | Nulo | Descrição |
|---|---|---|---|
| `id` | Integer PK autoincrement | não | — |
| `occurred_at` | DateTime(timezone=True) | não | data/hora do evento em UTC, `server_default=now()` |
| `user_id` | Integer FK → `users.id` | **sim** | nulo quando a origem é `system` |
| `user_label` | String(255) | não | e-mail (ou nome) do autor **no momento da ação** — preserva o rastro se o usuário for removido/renomeado |
| `user_role` | String(20) | não | perfil do autor no momento da ação; `SYSTEM` para origem interna |
| `origin` | String(10) | não | `user` \| `system` |
| `action` | String(10) | não | `create` \| `update` \| `delete` |
| `resource` | String(30) | não | `assignment` \| `shift_extra` \| `doctor` \| `user` \| `period` |
| `resource_id` | Integer | sim | id do recurso afetado (nulo só se a operação falhou antes de gerar id) |
| `period_id` | Integer | sim | competência relacionada, quando aplicável — sustenta o filtro da US2/US3 |
| `before` | JSON | sim | estado anterior (nulo em `create`) |
| `after` | JSON | sim | estado resultante (nulo em `delete`) |
| `summary` | String(255) | sim | descrição curta legível, ex.: `"Removeu Maria Oliveira do T3 de 12/07"` |
| `correlation_id` | String(36) | sim | id de correlação da requisição (liga ao log estruturado) |

**FK `user_id`**: `ON DELETE SET NULL`. O usuário pode ser removido; o registro permanece com
`user_label`/`user_role` preenchidos. (Hoje a exclusão de usuário é lógica — `active=false` — mas
a regra vale para o caso físico.)

### Índices

| Índice | Colunas | Serve a |
|---|---|---|
| `ix_audit_logs_occurred_at` | `occurred_at DESC` | ordenação padrão da consulta (FR-005) |
| `ix_audit_logs_resource` | `resource`, `resource_id` | "histórico deste plantão" |
| `ix_audit_logs_user_id` | `user_id` | filtro por autor |
| `ix_audit_logs_period_id` | `period_id` | aba de histórico da competência (US3) |

### Invariantes

1. Registro é **somente-inserção**: sem endpoint de update/delete (FR-007); nenhum código de
   produção altera linha existente.
2. `action='create'` ⇒ `before IS NULL` e `after IS NOT NULL`.
3. `action='delete'` ⇒ `before IS NOT NULL` e `after IS NULL`.
4. `action='update'` ⇒ ambos preenchidos, contendo **apenas os campos que mudaram**.
5. `origin='system'` ⇒ `user_id IS NULL` e `user_role='SYSTEM'` (FR-008).
6. Nenhum valor de `before`/`after` contém credencial (FR-004) — garantido pela lista explícita
   de campos por recurso (abaixo), não por filtro genérico.

## Campos gravados por recurso (lista explícita — FR-004)

| Recurso | Campos em `before`/`after` |
|---|---|
| `assignment` | `shift_id`, `shift_date`, `shift_type`, `doctor_id`, `doctor_name`, `start_time`, `end_time`, `status` |
| `shift_extra` | `shift_id`, `shift_date`, `doctor_id`, `doctor_name`, `duration_minutes`, `justification`, `status` |
| `doctor` | `name`, `crm`, `specialty`, `doctor_type`, `has_rqe`, `career_start_date`, `active` |
| `user` | `name`, `email`, `role`, `active`, `doctor_id` — **nunca** `password_hash`; troca de senha grava `{"password_changed": true}` |
| `period` | `year`, `month`, `status` |

`doctor_name` é desnormalizado de propósito: mantém o registro legível sem depender de join com um
cadastro que pode mudar de nome depois.

## Impacto nas tabelas existentes

**Nenhum.** Nenhuma coluna é adicionada, alterada ou removida em `shift_parts`, `shift_extras`,
`doctors`, `users` ou `periods`. A trilha é aditiva e isolada — é o que permite tratá-la (expurgo,
particionamento) no futuro sem tocar no operacional.

## Migration

- **Arquivo**: `backend/alembic/versions/20260807_011_audit_logs.py`
- **`down_revision`**: `010_user_doctor_link`
- **`upgrade()`**: cria `audit_logs` + os 4 índices.
- **`downgrade()`**: dropa a tabela (e os índices junto). Perda de dado assumida e esperada — o
  downgrade só faz sentido em rollback imediato, quando a trilha é recente.
- **Compatibilidade SQLite**: a criação é `op.create_table` simples, sem necessidade de
  `batch_alter_table` (só requerido para drop/alter de coluna).

## Estado inicial

A tabela nasce **vazia**. Não há histórico anterior a migrar — a informação nunca foi gravada
(research R1–R3). A interface deve deixar claro que a trilha começa na data do deploy, para não
induzir a leitura de que "nada foi alterado antes".
