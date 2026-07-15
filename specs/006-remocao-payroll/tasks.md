# Tasks: Remoção da superfície payroll/cobertura sem uso (B-07)

**Input**: Design documents from `/specs/006-remocao-payroll/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [quickstart.md](quickstart.md)

**Tests**: nenhum teste novo — é remoção. O "teste" de cada passo é o gate de paridade
(suíte verde + grep de imports + testes de API vivos intactos), executado como task explícita
antes de cada commit. Comando da suíte no [quickstart.md](quickstart.md) §1.

**Organization**: ordem **de fora para dentro** (borda HTTP → services → dados → domain →
resíduos): cada commit remove só código já inalcançável, então a suíte fica verde em todos os
passos. Por isso as fases são **sequenciais** ([P] só dentro da mesma fase).

## Format: `[ID] [P?] [Story] Description`

---

## Phase 1: Setup (baseline)

**Purpose**: ponto de retorno limpo e número de referência da suíte

- [X] T001 Registrar baseline: rodar a suíte no Docker (quickstart §1) e anotar a contagem
  (esperado: 632 passed / 0 failed) neste arquivo; confirmar `git status` limpo (checkpoint git
  é o próprio commit anterior)

---

## Phase 2: Foundational

**N/A** — feature de remoção pura; não há infraestrutura a construir. As fases seguem em ordem
de prioridade das user stories.

---

## Phase 3: User Story 1 — Remover a superfície payroll/cobertura de ponta a ponta (P1) 🎯 MVP

**Goal**: nenhuma rota/service/tabela de payroll ou cobertura no backend; jornadas vivas intactas.

**Independent Test**: suíte verde; `/api/v1/payrolls` e `/api/v1/coverage/*` respondem 404;
Swagger sem os grupos Payrolls/Coverage; migration sobe e desce num banco limpo (quickstart §2).

### Passo 1a — Borda HTTP (commit 1)

- [X] T002 [US1] Editar `backend/app/api/app.py`: remover `coverage` e `payroll` do import
  (linha 9) e os `include_router` correspondentes (linhas 48–49)
- [X] T003 [P] [US1] Deletar `backend/app/api/routes/payroll.py`,
  `backend/app/api/routes/coverage.py` e `backend/app/api/routes/query.py` (router de query
  nunca foi registrado — research R2); verificar `backend/app/api/routes/__init__.py`
- [X] T004 [US1] Gate + commit: suíte verde; `grep -rn "routes.payroll\|routes.coverage\|routes.query"
  backend/app` sem hits de produção; commit `refactor(api): remove rotas payroll/coverage/query (spec 006, US1)`

### Passo 1b — Services, schemas, repositories (commit 2)

- [X] T005 [P] [US1] Deletar `backend/app/services/payroll_service.py`,
  `backend/app/services/coverage_service.py` e `backend/app/services/query_service.py`
- [X] T006 [P] [US1] Deletar `backend/app/validators/payroll_governance_validator.py` (morto,
  research R5) e o pacote `backend/app/schemas/payroll/` (6 arquivos); verificar re-exports em
  `backend/app/schemas/__init__.py` e `backend/app/validators/__init__.py`
- [X] T007 [P] [US1] Deletar `backend/app/repositories/{payroll_repository,
  coverage_snapshot_repository,financial_snapshot_repository,financial_fact_repository}.py`;
  verificar `backend/app/repositories/__init__.py`
- [X] T008 [P] [US1] Deletar `backend/app/tests/unit/domain/test_query_domain.py` (testa o
  query_service removido)
- [X] T009 [US1] Gate + commit: suíte verde; `grep -rn "payroll_service\|coverage_service\|query_service"
  backend/app` sem hits de produção; commit `refactor(services): remove payroll/coverage/query services (spec 006, US1)`

### Passo 1c — Modelos e migration (commit 3)

- [X] T010 [US1] Deletar `backend/app/models/{payroll,coverage_snapshot,financial_snapshot,
  financial_fact}.py`; remover as linhas 9–12 de `backend/app/models/__init__.py`; remover o
  import morto `from app.models.payroll import Payroll` de `backend/app/seed/seed_data.py:28`
- [X] T011 [US1] Criar migration `backend/alembic/versions/20260715_008_drop_payroll.py`:
  upgrade droppa `payrolls` e droppa condicionalmente (via `sa.inspect`, padrão da migration
  004) `coverage_snapshots`, `financial_snapshots`, `financial_facts`; downgrade recria
  `payrolls` com o schema da migration 003 ([data-model.md](data-model.md))
- [X] T012 [US1] Gate + commit: suíte verde; ciclo de migration num banco limpo (quickstart §2:
  `upgrade head → downgrade -1 → upgrade head`); commit
  `refactor(models)!: remove payroll/snapshots + migration 008 drop (spec 006, US1)`

**Checkpoint US1**: superfície removida; app sobe (`python -c "import app.main"`); 404 nas rotas.

---

## Phase 4: User Story 2 — Remover o cluster `domain/` e a fundação órfã (P2)

**Goal**: `domain/` só com fundação viva (`constants`, `errors`, `events`, `exceptions`) —
zero comportamento. Encerra formalmente o B-07.

**Independent Test**: suíte verde; todo arquivo restante em `domain/` tem consumidor de
produção comprovável por grep.

### Passo 2a — Cluster (commit 4)

- [X] T013 [P] [US2] Deletar `backend/app/domain/{payroll,coverage,financial,remuneration,base,
  state_machines}/` (pacotes inteiros)
- [X] T014 [P] [US2] Deletar os 15 testes do cluster em `backend/app/tests/unit/domain/`:
  test_aggregate_root, test_aggregate_version, test_lifecycle_hooks, test_coverage_engine,
  test_financial_constants, test_financial_events, test_financial_snapshot, test_governance,
  test_payroll_competency, test_payroll_errors, test_payroll_events, test_payroll_state_machine,
  test_payroll_status, test_remuneration_events, test_remuneration_rule (research R7)
- [X] T015 [US2] Gate + commit: suíte verde; `grep -rn "domain.payroll\|domain.coverage\|
  domain.financial\|domain.remuneration\|domain.base\|domain.state_machines" backend/app` sem
  hits; commit `refactor(domain): remove cluster payroll/coverage/financial/base (spec 006, US2)`

### Passo 2b — Fundação órfã (commit 5)

- [X] T016 [US2] Deletar constantes órfãs `backend/app/domain/constants/{payroll_status,
  snapshot_status,financial_fact_status,financial_fact_type,inconsistency_type,rule_status}.py`
  (tabela research R6); verificar `constants/__init__.py`
- [X] T017 [US2] Deletar `backend/app/domain/errors/payroll_errors.py`; verificar/editar
  `errors/__init__.py` e `errors/error_catalog.py`; editar
  `backend/app/domain/events/event_names.py` removendo os nomes `PAYROLL_*`, `COVERAGE_*` e
  `FINANCIAL_*` mortos (research R1: dispatch é no-op — sem `register` em produção)
- [X] T018 [US2] Gate + commit: suíte verde; para cada arquivo restante em `domain/`, grep
  comprova ≥1 consumidor de produção (SC-003); commit
  `refactor(domain): remove constantes/erros/eventos orfaos (spec 006, US2)`

**Checkpoint US2**: `domain/` = fundação pura; B-07 tecnicamente encerrado.

---

## Phase 5: User Story 3 — Limpeza cruzada de resíduos (P3)

**Goal**: `payroll` só existe em histórico (docs/specs/migrations); frontend sem constantes mortas.

**Independent Test**: `git grep -il payroll -- backend/app frontend/src` retorna apenas os
resíduos aceitos (rótulo hardcoded do painel e literais de navegação — ver T020); build do
frontend verde.

- [X] T019 [P] [US3] Deletar o pacote `backend/app/integrations/` inteiro (28 arquivos —
  scaffolding de ERPs, research R5) e `backend/app/tests/integration/test_integration_architecture.py`
  (único consumidor)
- [X] T020 [P] [US3] Frontend — remover somente o comprovadamente morto, sem mudança visual:
  entradas `PAYROLL`, `PAYROLL_NEW`, `PAYROLL_DETAIL`, `PAYROLL_APPROVE`, `COVERAGE`,
  `COVERAGE_NEW`, `COVERAGE_DETAIL`, `READINESS` em `frontend/src/routes/routes.ts` (conferir
  cada uma por grep antes de remover); rota `READINESS` em `frontend/src/App.tsx:106`;
  `queryKeys.payroll`, `queryKeys.query.payroll` e `queryKeys.kpi.payroll` em
  `frontend/src/services/query-keys.ts`; contexto `payroll` em
  `frontend/src/shared/components/operational/OperationalEmptyState.tsx`.
  **NÃO tocar**: rótulo "Payroll: Pendente" em `OperationalMetricsPanel.tsx` e literais de
  navegação em `dashboard-page.tsx` (paridade visual — anotados para o lote B-02/B-04)
- [X] T021 [US3] Gate + commit: suíte backend verde; `cd frontend && npx vite build` verde;
  `git grep -il payroll -- backend/app frontend/src` só com resíduos aceitos; commit
  `refactor: remove integrations mortas e residuos payroll do frontend (spec 006, US3)`

**Checkpoint US3**: repositório limpo do conceito payroll fora de histórico.

---

## Phase 6: Polish & Encerramento

- [X] T022 Validação no navegador conforme [quickstart.md](quickstart.md) §3: jornadas vivas,
  relatórios PDF/Excel/CSV idênticos (SC-001/SC-002), Swagger sem grupos removidos, 404 em
  `/api/v1/payrolls`
- [X] T023 [P] Docs: marcar B-07 ✅ encerrado em `docs/backlog-melhorias.md` (apontando para a
  spec 006); atualizar `docs/HANDOFF.md` (Fase 2 100% encerrada, próximos passos); anotar na
  spec 001 (`specs/001-baseline-funcional/spec.md`) o escopo real de "remuneração" (relatório,
  não folha); nota de release: **backup obrigatório antes do deploy** (migration droppa `payrolls`)
- [X] T024 Medir resultado e registrar neste arquivo: linhas de produção removidas
  (`git diff --stat <baseline>..HEAD`, esperado ≥3.000 — SC-004), arquivos finais em `domain/`
  (SC-003) e contagem final da suíte (SC-005); commit final de docs

---

## Dependencies & Execution Order

- **Fases sequenciais**: 1 → 3 (US1) → 4 (US2) → 5 (US3) → 6. A ordem de fora para dentro é
  **obrigatória**: US2 depende de US1 (o cluster `domain/` só fica morto após remover os
  services); US3/T019 é independente tecnicamente, mas fica após US2 para manter commits coesos.
- **Dentro de cada passo**, tasks [P] tocam arquivos disjuntos e podem ser feitas juntas; o
  gate (suíte + grep + commit) fecha o passo.
- **1 commit por passo** (6 commits de código + docs), suíte verde em todos — FR-007.

## Parallel Example: Passo 1b

```text
# Juntas (arquivos disjuntos):
T005 deletar 3 services
T006 deletar validator + schemas/payroll/
T007 deletar 4 repositories
T008 deletar test_query_domain.py
# Depois, sequencial: T009 (gate + commit)
```

## Implementation Strategy

- **MVP = US1** (fases 1+3): remove a superfície inteira e a tabela; já entrega o valor
  principal com app validável de ponta a ponta. Parar e validar no checkpoint US1.
- **Incremental**: US2 encerra o B-07; US3 é acabamento. Cada checkpoint é um ponto de parada
  seguro e demonstrável.
- **Rollback**: qualquer passo reverte com `git revert` do commit do passo; a migration tem
  downgrade.

## Baseline (T001)

- Suíte antes: **632 passed / 0 failed** (cobertura 69%)
- Commit baseline: **d75ea29**

## Progresso

- **US1 concluída** (3 commits): passo 1a rotas (632✓), passo 1b services (608✓ — saem os 24
  do test_query_domain), passo 1c modelos + migration 008 (608✓ + ciclo upgrade/downgrade/upgrade OK).
  Achados dos gates, corrigidos junto: relationship `Period.payrolls` (cascade) em
  `models/period.py` e import de `Payroll` em `alembic/env.py`.
- **US2 concluída** (2 commits): cluster domain (437✓) + fundação órfã (429✓). Achados dos gates:
  `EventCollector` órfão removido; bug latente pré-existente `PERIOD_DEACTIVATED_V1` (membro
  inexistente no enum, DELETE de período → 500) registrado como tarefa separada — fora de escopo.
- **US3 concluída** (1 commit): `integrations/` + teste (404✓); frontend só o comprovadamente
  morto. Descoberta do gate: `ROUTES.PAYROLL`/`COVERAGE` são rotas SPA VIVAS (menu Financeiro/
  Operacional → ShiftListPage) — mantidas; removidos só `_NEW/_DETAIL/_APPROVE`, `READINESS`,
  queryKeys e contexto de empty-state. Resíduos aceitos (UI visível): rota SPA `/app/payroll`,
  rótulo "Payroll: Pendente" e ação "Processar folha" do dashboard (strings).

## Resultado final (T024)

- **Suíte**: 632 → **404 passed / 0 failed** (–228, todos de código removido); cobertura 65,5%
  (gate 65) — SC-005 ✓
- **Produção removida**: **5.885 linhas / 84 arquivos** (+79 inseridas: migration + ajustes) —
  SC-004 ✓ (meta ≥3.000); testes de código morto: +2.315 linhas / 18 arquivos
- **`domain/`**: 20 arquivos (13 sem `__init__`) — só `constants`, `errors`, `events`,
  `exceptions`, todos com consumidor de produção — SC-003 ✓
- **Navegador** (SC-001/SC-002 ✓): login, dashboard com dados, workspace/grade, aba Financeiro
  (valores por médico), aba Relatórios (4 geradores), rota SPA `/app/payroll` renderizando como
  antes; `/api/v1/payrolls` e `/api/v1/coverage/*` → 404; OpenAPI sem os grupos removidos
- **Backend**: 205 arquivos .py de produção (era 281 no início da spec 006)
- ⚠️ **Deploy**: backup obrigatório antes (migration 008 droppa `payrolls`) — avisado em
  `docs/deploy.md` e no HANDOFF
