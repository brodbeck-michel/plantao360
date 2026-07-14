# Tasks: Colapso final da camada `domain/` (Fase 2 — passo 3)

**Input**: Design de `specs/005-colapso-domain-final/` + `docs/levantamento-domain.md` + achados da spec 004.

**Prerequisites**: plan.md, spec.md, research.md, quickstart.md (prontos).

**Tests**: NÃO se geram testes novos. A suíte existente (**638 passing**, spec 003/004) é a rede de
segurança e o juiz de paridade — aqui com peso extra nos testes de **comportamento** (transições de
estado, decisões de regra) e de **API**. Testes de módulo morto saem junto (D3 da spec 004). Cada
tarefa é um passo (ou poucos passos) do loop de segurança e termina em **commit verde**.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: paralelizável — praticamente nenhum aqui (refactor sequencial por design; suíte verde
  entre passos).
- **[Story]**: US1 (read_models/query) · US2 (rules/state_machines) · US3 (cluster payroll) ·
  US4 (use_cases) · US5 (paridade).

## ⚙️ O loop de segurança QUÁDRUPLO (aplicar em CADA tarefa) — research D1/D2

1. **Confirmar** por grep os consumidores do alvo (produto / domain / tests).
2. **Aplicar**: mover a lógica para o service/local certo (inclui ajustar **rotas de API** para
   importarem os `query` do service); adaptar/mover testes.
3. **Limpar** `__init__`/reexports que apontem para o removido.
4. **Verificar (quádruplo)**: suíte `0 failed / 0 errors`; `grep app.domain.<modulo>` em produto → 0;
   testes de API verdes; **`grep -rE "app\.services" backend/app/domain` → 0** (anti-inversão).
5. **Commit** do passo. `Co-Authored-By: Claude Opus 4.8`.

Suíte: `docker build -t plantao360-backend-test ./backend && docker run --rm -e ENVIRONMENT=test plantao360-backend-test python -m pytest -p no:cacheprovider -q`

> ⚠️ **Comportamento, não só dados**: ao mover `rules`/`state_machines`, preservar transições
> permitidas/proibidas, erros/mensagens e **efeitos colaterais** (eventos, auditoria) — não só a
> checagem "pode transicionar" (research D6).

---

## Phase 1: Setup (baseline)

- [X] T001 Baseline verde confirmado: **638 passed / 0 failed / 0 errors**.
- [X] T002 Contagem inicial da `domain/`: **53** arquivos.

**Checkpoint**: baseline verde e contagem registrados.

---

## Phase 2: Foundational (desbloqueio para deletar `rules`)

**⚠️ CRÍTICO**: precede a remoção de `rules` (Phase 4).

- [X] T003 `BusinessRuleCode` movido para `domain/constants/business_rule_code.py` (padrão dos
  enums); `error_catalog` e testes apontam para o novo lar; `rules/__init__` esvaziado;
  `business_rules.py` deletado. Suíte 638. `errors` não depende mais de `rules`.

**Checkpoint**: `errors` não depende mais de `rules`. ✅

---

## Phase 3: User Story 1 — Consolidar read_models e query nos services (Priority: P1) 🎯

**Goal**: mover os objetos de leitura/consulta para `query_service`/`dashboard_service` e removê-los
de `domain/`; peso morto sai. Padrão de data classes (validado na spec 004), menor risco.

**Independent Test**: após mover, a suíte segue verde e os endpoints de dashboard/consulta retornam
o mesmo resultado.

- [X] T004 [US1] `query` (6): DashboardQuery → dashboard_service; as outras 5 → query_service;
  rotas `api/routes/query.py`+`dashboard.py` importam do service (api→service). Módulo deletado. Suíte 638.
- [X] T005 [US1] `read_models` (8): dashboard_summary (7 classes) → dashboard_service;
  doctor/coverage/financial/payroll_summary → query_service; period/shift/assignment_summary mortos
  removidos com seus testes (D3). Módulo deletado. Suíte 635.

**Checkpoint US1 ✅**: `read_models`/`query` fora de `domain/`; suíte **635 passed / 0 failed**;
`domain/` **53 → 39** arquivos; 0 import quebrado; **0 inversão domain→service**; contratos idênticos
(rotas de API importam os query objects do service). Restam em `domain/`: base, constants, coverage,
errors, events, exceptions, financial, payroll, remuneration, rules, state_machines, value_objects.

---

## Phase 4: User Stories 2 + 4 — rules/state_machines por vertical, com use_cases (Priority: P1/P2)

**Goal**: colapsar cada vertical (regra + máquina de estado + use_cases) no seu service, preservando
comportamento. `rules`/`state_machines` são compartilhados com `use_cases` → tratar o vertical como
unidade (research D4). Cada vertical pode ser **mais de um commit** (loop de segurança por passo).

**Independent Test**: por vertical, transições válidas/inválidas e decisões de regra ficam idênticas;
testes de comportamento + API verdes.

- [X] T006 [US4][US2] **Vertical assignments**: `use_cases/assignments` (10) era **camada paralela
  MORTA** (a API usa `AssignmentService`; ninguém importava os use_cases) → removida inteira. Depois
  `assignment_rules` + `assignment_state_machine` inlinados no `assignment_service` (consumidor único).
  Anotação `AggregateRoot` removida (só hint). Suíte 635.
- [X] T007 [US4][US2] **Vertical periods**: `use_cases/periods` é orquestração **viva** (rota period
  a usa) → mantida (D8). `period_state_machine` inlinado em `base_period_use_case` (junto da
  PeriodPolicy da spec 004). Suíte 632.
- [X] T008 [US2] **Vertical shift**: `shift_rules` + `shift_state_machine` → `shift_service`.
  `shift_rules` importava `ShiftTimeRange` mas **nunca o usava** (import morto) → `value_objects`
  (só `shift_time_range`) deletado como peso morto + seu teste; pacote removido. Suíte 632.
- [X] T009 [US2] **Vertical extra**: `extra_state_machine` → `extra_service`. Suíte 632.
- [X] T010 [US2] `domain/rules/` removido (vazio após inlines + move do BusinessRuleCode).
  `domain/state_machines/` restou só `payroll_state_machine` (cai no cluster payroll, US3). Suíte 632.

**Checkpoint US2/US4 ✅**: 4 verticais colapsados; `rota→service→model`; suíte **632 passed / 0 failed**;
`domain/` **39 → 32** arquivos (já na meta 30-40); **0 inversão domain→service**; comportamento
idêntico (testes de transição/regra + API verdes). Achado: `use_cases/assignments` era camada morta;
`use_cases/periods` é orquestração viva (mantida). Restam em `domain/`: base, constants, coverage,
errors, events, exceptions, financial, payroll, remuneration, state_machines(payroll).

---

## Phase 5: User Story 3 — Colapsar o cluster do agregado payroll (Priority: P1)

**Goal**: colapsar o cluster acoplado nos services sem inversão (research D7).

**Independent Test**: folha (draft→review→approve→export, versões, selo, auditoria, governança) e
cobertura produzem os mesmos resultados; suíte + API verdes; nenhum import domain→service.

- [ ] T011 [US3] Inlinar `domain/coverage/coverage_engine` e `domain/financial/financial_snapshot_builder`
  em `coverage_service` (consumidor único de produto); mover as DTOs compartilhadas
  (CoverageResult/Fact, FinancialSnapshotData/FactData) para o service; adaptar testes.
- [ ] T012 [US3] Colapsar o agregado `domain/payroll` (`payroll_competency` + `governance`) e
  `domain/state_machines/payroll_state_machine` em `payroll_service`; o
  `validators/payroll_governance_validator` passa a chamar o service; preservar versões/selo/eventos/
  auditoria (D6). `FinancialSnapshotData` (do T011) passa a ser referenciada service→service.
- [ ] T013 [US3] Remover/mover as data classes de `domain/remuneration` (RemunerationResult/Rule/
  CalculationExplanation) para onde o payroll as usa (payroll_service) e `domain/value_objects/shift_time_range`
  (se ainda não caiu no T008). ⚠️ Isto **não** implementa a folha em R$ — o gap B-06 permanece.
- [ ] T014 [US3] **(ÚLTIMO)** Deletar `domain/base/aggregate_root` (AggregateRoot): confirmar por
  `grep app.domain.base` que nenhum consumidor remanescente existe (payroll_competency + as
  state_machines que o herdavam já colapsaram); adaptar/mover testes de base.

**Checkpoint US3**: cluster colapsado; `base` fora; 0 inversão; folha/cobertura idênticas.

---

## Phase 6: User Story 5 — Paridade e não-regressão (Priority: P1)

- [ ] T015 [US5] SC-001 — suíte completa: **0 failed / 0 errors**.
- [ ] T016 [US5] SC-002 — grep sem import de produto quebrado **e** `grep -rE "app\.services" backend/app/domain` → 0 (anti-inversão).
- [ ] T017 [US5] SC-003 — `pytest app/tests/integration -q` (test_*_api) verdes (contratos idênticos).
- [ ] T018 [US5] SC-004 — `find backend/app/domain -name '*.py' -not -name '__init__.py' | wc -l` → **~30–40**.
- [ ] T019 [US5] SC-005 — subir o app dev e percorrer escala/extras/cobertura/dashboard/períodos-folha/
  usuários → comportamento idêntico.
- [ ] T020 [US5] Prova de escopo: `git diff --name-only <baseline>..HEAD` só toca
  `backend/app/{domain,services,use_cases,validators}/`, `backend/app/tests/`, `docs/`/`specs/` —
  nenhum `models`/`schemas`/migration/`frontend`; só ajuste de import em `api/routes`.

**Checkpoint US5**: paridade comprovada (suíte + API + imports + anti-inversão + escopo + app).

---

## Phase 7: Polish & registro

- [ ] T021 Atualizar `docs/HANDOFF.md` (Fase 2 CONCLUÍDA; `domain/` no tamanho final), a memória do
  projeto, e confirmar que B-06 segue registrado no backlog (não tocado).

---

## Dependencies & Execution Order

- **Setup (P1)** → **Foundational (P2, T003 move BusinessRuleCode)** → **US1 (P3)** → **US2/US4 por
  vertical (P4)** → **US3 cluster payroll (P5)** → **US5 paridade (P6)** → **Polish (P7)**.
- **T003 antes de deletar `rules`** (T010).
- **`base` (T014) por último** — depois de payroll_competency + state_machines colapsados.
- **T011 antes de T012** (payroll referencia as DTOs financeiras).
- Refactor **sequencial** (não paralelizar): a suíte verde entre passos pequenos é o sinal de qual
  passo regrediu. Não avançar com a suíte vermelha.

## Implementation Strategy

### MVP incremental

1. Setup + Foundational → baseline verde + `errors` desacoplado de `rules`.
2. US1 (read_models/query) → menor risco, valida o padrão → checkpoint.
3. US2/US4 por vertical → comportamento preservado, um vertical por vez → checkpoint.
4. US3 cluster payroll → dissolve o nó adiado, `base` por último → checkpoint.
5. US5 → provar paridade. Cada passo é um incremento verde rastreável (SC-006).

## Notes

- Rede de segurança = suíte spec 003/004; **não** se escrevem testes novos.
- Dentro do container o path é `app/...` (workdir `/app`).
- Drive de rede lento: ler cada arquivo uma vez; grep escopado em `services`/`api`/`use_cases`/`domain`.
- Fora de escopo (não tocar): `constants`/`errors`/`events`/`exceptions` (fundação); cálculo de
  remuneração em R$ (B-06); frontend; contratos de API.
