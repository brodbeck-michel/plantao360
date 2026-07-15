# Research — Remoção da superfície payroll/cobertura sem uso (spec 006)

**Data**: 2026-07-15. Todas as verificações abaixo foram feitas por leitura de código e grep no
repositório (métodos: `git ls-files`, grep de imports de produção, leitura dos arquivos-chave).

## R1 · Eventos `PAYROLL_*` / `COVERAGE_*` têm consumidor?

- **Decisão**: remover os nomes de evento mortos junto com o cluster. Nenhum risco.
- **Rationale**: `EventDispatcher.register()` **não é chamado em nenhum código de produção** —
  somente em 4 testes (contracts/patterns) com eventos de doctor/test. Cada service cria sua
  própria instância de dispatcher em nível de módulo; sem `register`, todo `dispatch` é no-op.
  A auditoria não passa pelo dispatcher.
- **Alternativas**: manter os nomes "por segurança" — rejeitado (Princípio I: peso sem função).

## R2 · `/query/payroll`, `/kpi/payroll` e explain têm consumo?

- **Decisão**: remover **`api/routes/query.py` inteiro (13 endpoints, 230 linhas) e
  `services/query_service.py` inteiro (931 linhas)** — não só as partes de payroll.
- **Rationale**: descoberta do research — `query.router` **nunca foi registrado no
  `app.py`**. As rotas `/query/*` de analytics são código inalcançável. O único endpoint vivo
  sob `/api/v1/query` é o do **dashboard** (`dashboard.router` montado com prefixo
  `/api/v1/query`), que tem service próprio e não importa `query_service`. Consumidores de
  `query_service`: apenas `routes/query.py` (morto) e `tests/unit/domain/test_query_domain.py`.
  O frontend chama somente `/query/dashboard`.
- **Alternativas**: remover só os pedaços payroll do `query_service` — rejeitado: manteria ~700
  linhas de analytics inalcançáveis (KPIs, timeline, explains) sem nenhum consumidor.

## R3 · Seed referencia payroll?

- **Decisão**: remover apenas o import morto.
- **Rationale**: `seed/seed_data.py` importa `Payroll` (linha 28) e **nunca o usa**. Nenhum dado
  de payroll/snapshot é semeado.

## R4 · Migrations e tabelas — o que existe de fato no schema versionado?

- **Decisão**: nova migration `008_drop_payroll` que (a) droppa `payrolls` e (b) droppa
  `coverage_snapshots`, `financial_snapshots` e `financial_facts` **somente se existirem**
  (via inspector, padrão da migration 004). Downgrade recria `payrolls` conforme a migration 003.
- **Rationale**: só `payrolls` existe no schema versionado (criada em `sprint9_add_payroll`,
  recriada em `003_runtime_alignment`). **Nenhuma migration cria as 3 tabelas de snapshot** —
  em produção elas não existem (os modelos só viram tabela no ambiente de teste, via
  `create_all`). Ou seja: os 2 endpoints de cobertura **quebrariam em produção** se alguém os
  chamasse — mais uma prova de que o fluxo nunca foi usado. O drop condicional cobre bancos de
  dev antigos que possam ter as tabelas.
- **Backup**: `scripts/backup.sh` antes do deploy (procedimento já documentado em
  `docs/deploy.md`); reforçar no release note da versão.

## R5 · O que mais referencia payroll fora do cluster? (descobertas de escopo)

- **`app/integrations/` (28 arquivos, pacote inteiro)**: scaffolding de ACL/adapters/contracts
  para ERPs hipotéticos (**Senior, SAP, Tasy, TOTVS, MVSoul**...) — exatamente o cenário
  "exportar folha para o ERP oficial" descartado no B-06. **Único consumidor: o próprio teste**
  (`tests/integration/test_integration_architecture.py`). Nenhum código de produção importa o
  pacote. **Decisão: remover o pacote inteiro + o teste de arquitetura** (Princípio I e V; mesmo
  fundamento da decisão do stakeholder de 2026-07-15). É extensão de escopo em relação ao texto
  da spec (que citava só os "resíduos payroll") — justificada aqui e destacada no plan.
- **`validators/payroll_governance_validator.py`**: classe morta (zero referências).
- **Frontend**: constantes/rotas/query-keys mortas (`ROUTES.PAYROLL*`, `queryKeys.payroll`,
  contexto `payroll` do `OperationalEmptyState`). **Exceção deliberada**: o rótulo
  "Payroll: Pendente" (hardcoded) no `OperationalMetricsPanel` **fica** nesta spec — removê-lo
  mudaria a tela (viola FR-005/paridade estrita); fica anotado como candidato ao lote frontend
  (B-02/B-03/B-04).

## R6 · Fundação da `domain/` — o que fica órfão após a remoção?

Consumo verificado de `domain/constants/*` fora do cluster removido:

| Constante | Consumidores vivos | Destino |
|---|---|---|
| `competency_dates` | period routes, create_period, period_response, seed, shift/workspace services | **MANTER** |
| `assignment_status`, `extra_status`, `period_status`, `shift_status`, `shift_types`, `business_rule_code` | services/rotas vivas (verificado nas specs 004/005) | **MANTER** |
| `payroll_status` | só cluster removido + testes do cluster | remover |
| `snapshot_status`, `financial_fact_status`, `financial_fact_type`, `inconsistency_type` | só cluster removido + testes | remover |
| `rule_status` | **nenhum** (já órfã hoje) | remover |

- `domain/errors/payroll_errors.py`: só `payroll_service` (removido) → remover (verificar
  `error_catalog` na implementação).
- `domain/events/event_names.py`: remover apenas os nomes `PAYROLL_*`/`COVERAGE_*`/
  `FINANCIAL_*` mortos; nomes usados por services vivos ficam.
- `domain/base/` (AggregateRoot): consumidores são só `payroll_competency`,
  `payroll_state_machine` e 3 testes → remover junto.

## R7 · Testes afetados (saem junto com o código que testam)

- `tests/unit/domain/`: test_aggregate_root, test_aggregate_version, test_lifecycle_hooks,
  test_coverage_engine, test_financial_constants, test_financial_events, test_financial_snapshot,
  test_governance, test_payroll_competency, test_payroll_errors, test_payroll_events,
  test_payroll_state_machine, test_payroll_status, test_remuneration_events,
  test_remuneration_rule, test_query_domain (16 arquivos).
- `tests/integration/test_integration_architecture.py` (junto com `integrations/`).
- **Nenhum teste de API cobre os endpoints de payroll/cobertura** (verificado: fora de
  `unit/domain`, só o teste de arquitetura menciona payroll) — os 93 testes de API vivos não
  são tocados.
- `tests/unit/patterns/test_events.py` (EventDispatcher genérico) **fica** — o dispatcher segue
  em uso pelos services vivos.

## Inventário consolidado de remoção (produção)

| Bloco | Arquivos | Linhas (aprox.) |
|---|---|---|
| Rotas: payroll.py, coverage.py, query.py + registro no app.py | 3 | ~590 |
| Services: payroll (507), coverage (217), query (931) | 3 | ~1.655 |
| Schemas `schemas/payroll/` | 6 | ~250 |
| Repositories (payroll, coverage_snapshot, financial_snapshot, financial_fact) | 4 | ~250 |
| Models (payroll, coverage_snapshot, financial_snapshot, financial_fact) | 4 | ~200 |
| Validator morto | 1 | ~50 |
| `domain/`: payroll (1.004), coverage, financial, remuneration, base, state_machines | ~14 | ~1.900 |
| Constantes/erros/eventos órfãos | ~7 | ~200 |
| `integrations/` (pacote inteiro) | 28 | ~1.500 |
| **Total produção** | **~70** | **~6.600** |

SC-004 (≥3.000 linhas) é atingido com folga. `domain/` termina com: `constants` (vivas),
`errors` (vivos), `events`, `exceptions` — só fundação com consumidor comprovado.
