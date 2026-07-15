# Data Model — spec 006 (remoção)

Esta feature **remove** entidades; não cria nenhuma. Registro do estado antes/depois.

## Tabelas removidas

### `payrolls` (existe no schema versionado — Postgres de produção)

Criada em `sprint9_add_payroll`, recriada em `20260628_003_runtime_alignment`. Colunas:
`id`, `period_id` (FK periods, unique), `year_month`, `status` (draft/calculated/reviewed/
approved/locked/exported/paid/archived), `current_version`, `created_by`, `created_at`,
`updated_at`, `reopen_count`, `reopen_reason`.

- **Remoção**: migration `008_drop_payroll` → `op.drop_table("payrolls")`.
- **Downgrade**: recria a tabela com o schema da migration 003 (dados não retornam — aceito
  pelo stakeholder; backup prévio obrigatório via `scripts/backup.sh`).

### `coverage_snapshots`, `financial_snapshots`, `financial_facts` (NÃO existem no schema versionado)

Os modelos SQLAlchemy existem, mas **nenhuma migration cria essas tabelas** — em produção elas
não existem; só aparecem em bancos de teste (via `create_all`). A migration 008 faz drop
**condicional** (inspector, mesmo padrão da migration 004) para sanear bancos de dev antigos.

## Modelos Python removidos

`app/models/payroll.py`, `coverage_snapshot.py`, `financial_snapshot.py`, `financial_fact.py`
(+ imports em `models/__init__.py` e import morto em `seed/seed_data.py`).

## Estado final da `domain/`

Apenas fundação com consumidor de produção vivo:

```text
app/domain/
├── constants/   # assignment/extra/period/shift status, shift_types, business_rule_code, competency_dates
├── errors/      # catálogos de erro dos fluxos vivos (assignment, doctor, extra, period, shift)
├── events/      # event_collector + event_names (só nomes vivos)
└── exceptions/  # errors.py (exceções compartilhadas)
```

Zero comportamento (nenhum agregado, engine, state machine, builder ou policy).
