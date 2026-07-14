# Tasks: Colapso da camada `domain/` (Fase 2 — passo 2)

**Input**: Design documents from `specs/004-colapso-domain/` + `docs/levantamento-domain.md`

**Prerequisites**: plan.md, spec.md, research.md, quickstart.md (todos prontos)

**Tests**: NÃO se geram testes novos. A suíte existente (738 passing, spec 003) **é** a rede de
segurança e o juiz de paridade. Testes de módulos mortos (Grupo A) são **removidos junto** com o
módulo (D3). Cada tarefa é um passo do loop de segurança e termina num **commit verde**.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: paralelizável (arquivos diferentes, sem dependência) — raro aqui: o refactor é
  sequencial por design (D1, um módulo por commit, suíte verde entre passos).
- **[Story]**: US1 (deletar Grupo A) · US2 (inline Grupo B) · US3 (paridade final).

## ⚙️ O loop de segurança (aplicar em CADA tarefa de US1/US2)

Definido em [research.md](./research.md) (D2) e [quickstart.md](./quickstart.md):

1. **Confirmar** por grep que o alvo tem 0 consumidor de produto (Grupo A) ou exatamente 1 (Grupo B):
   `grep -rE "app\.domain\.<modulo>" backend/app --include=*.py | grep -v "/domain/" | grep -v "/tests/"`
2. **Aplicar**: Grupo A → deletar módulo + seus testes. Grupo B → mover a lógica para o único
   service consumidor, ajustar o import, adaptar/mover os testes; depois deletar o módulo.
3. **Limpar** qualquer `__init__.py`/reexport que aponte para o removido (senão import quebrado).
4. **Rodar a suíte** (no Docker) → **0 failed / 0 errors**; e
   `grep -rE "app\.domain\.<modulo>\b" backend/app --include=*.py | grep -v /tests/` → **sem
   resultado em produto**.
5. **Commit** do passo (incremento verde e reversível), `Co-Authored-By: Claude Opus 4.8`.

Comando da suíte:
`docker build -t plantao360-backend-test ./backend && docker run --rm -e ENVIRONMENT=test plantao360-backend-test python -m pytest -p no:cacheprovider -q`

---

## Phase 1: Setup (baseline)

**Purpose**: fixar a rede de segurança antes de mexer em qualquer coisa.

- [X] T001 Baseline verde confirmado: **738 passed / 0 failed / 0 errors** (coverage 68.54%).
- [X] T002 Contagem inicial da `domain/`: **88** arquivos `.py` (sem `__init__`).

**Checkpoint**: baseline verde e contagem inicial registrados — o colapso pode começar.

---

## Phase 2: Foundational

Sem trabalho de fundação: não há infraestrutura nova a criar. Os módulos de fundação
(`constants`, `errors`, `events` — Grupo C) **permanecem intocados** (FR-007) e não são
pré-requisito a construir.

---

## Phase 3: User Story 1 — Remover módulos mortos (Grupo A) (Priority: P1) 🎯 MVP

**Goal**: remover os módulos de `domain/` que nenhum código de produto usa (prod=0), junto com
seus testes — a maior redução com o menor risco.

**Independent Test**: após cada remoção, a suíte segue verde e nenhum import de produto quebra;
percorrer escala/extras/folha/dashboard mostra comportamento idêntico.

> Ordem: dos vazios/menores para os maiores; **`base` por ÚLTIMO** (D4 — tem 4 usos internos de
> domain; só cai depois que tudo que o importa já saiu). Cada tarefa segue o loop de segurança.

- [X] T003 [US1] Deletado `domain/entities/` (vazio). Suíte 738.
- [X] T004 [US1] Deletado `domain/services/` (vazio). Suíte 738.
- [X] T005 [US1] Deletado `domain/reports/` + `TestReportDefinitions`. Suíte 735.
- [X] T006 [US1] Deletado `domain/calendar/` + teste; limpo `base/__init__` (BusinessCalendar). Suíte 722.
- [X] T007 [US1] Deletado `domain/metrics/` + teste. Suíte 718.
- [X] T008 [US1] Deletado `domain/snapshots/` + teste. Suíte 713.
- [X] T009 [US1] Deletado `domain/transitions/` + teste. Suíte 709.
- [X] T010 [US1] Deletado `domain/contracts/` + 2 testes. Suíte 696.
- [X] T011 [US1] Deletado `domain/overlap/` + teste (confirmado: overlap real vive inline em
  `assignment_service.create()`, virada de meia-noite +24h). Suíte 690.
- [X] T012 [US1] ⚠️ **PARCIAL**: deletados 5 VOs mortos + 4 testes. **`shift_time_range.py` MANTIDO**
  — usado por `domain/rules/shift_rules` (Grupo D, produto vivo). Cai quando `rules` for tratado. Suíte 675.
- [X] T013 [US1] ⚠️ **PARCIAL**: deletado só o **motor morto** (`remuneration_calculator`,
  `remuneration_engine`, `pricing_policy`) + 3 testes; `__init__` limpo; fórmula resgatada em B-06.
  **MANTIDOS** `remuneration_result`, `remuneration_rule`, `calculation_explanation` — usados por
  `domain/payroll/payroll_competency` (produto vivo via `payroll_service`). Suíte 652.
- [~] T014 [US1] **ADIADO**: `base/aggregate_root` (AggregateRoot) ainda é importado por
  `domain/payroll/payroll_competency` (vivo) e pelos 3 `domain/state_machines/*` (**Grupo D, fora
  de escopo**). O guard do D4 (grep mostra importadores) impede a remoção agora. `base` cai junto
  com a feature do Grupo D (state_machines).

**Checkpoint US1 ✅**: Grupo A concluído. **9 módulos totalmente removidos**; `value_objects` e
`remuneration` reduzidos ao que é vivo; `base` adiado ao Grupo D. Suíte **652 passed / 0 failed**;
`domain/` **88 → 71** arquivos; **0 import de produto quebrado**; escopo só em
`domain/services/use_cases/tests/docs/specs`. As 3 exceções têm a mesma raiz: peças de fundação
ainda consumidas por Grupo D (`rules`, `state_machines`) e pelo agregado `payroll` — coerente com
D4 e o edge case da spec.

---

## Phase 4: User Story 2 — Inline de abstrações de consumidor único (Grupo B) (Priority: P1)

**Goal**: mover a lógica de cada módulo de consumidor único para dentro do seu único service e
deletar o módulo — colapsando a profundidade para `rota → service → model` (D5).

**Independent Test**: após inlinar um módulo, os testes desse service passam e a resposta da API
correspondente é idêntica; a suíte roda verde **entre** cada passo (nunca big-bang).

> Ordem (plan): primeiro os de 1 arquivo (`timeline`, `coverage`, `financial`, `policies`), depois
> os maiores (`projections`, `explainability`, `kpi`, `analytics`) e por fim `payroll` (2
> consumidores). Cada tarefa segue o loop de segurança; a lógica movida deve ser equivalente ao
> comportamento anterior.

- [X] T015 [US2] `timeline` → `query_service` (2 dataclasses embutidas). Suíte 652.
- [~] T016 [US2] `coverage` → **ADIADO** ao Grupo D (ver nota abaixo).
- [~] T017 [US2] `financial` → **ADIADO** ao Grupo D (ver nota abaixo).
- [X] T018 [US2] `policies` → `use_cases/periods/base_period_use_case` (PeriodPolicy inlinada;
  coverage_policy morto removido). Suíte 638.
- [X] T019 [US2] `projections` → `dashboard_service` (só DashboardProjection era vivo; 4 mortos
  removidos). Suíte 648.
- [X] T020 [US2] `explainability` → `query_service` (3 dataclasses). Suíte 648.
- [X] T021 [US2] `kpi` → `query_service` (4 dataclasses). Suíte 648.
- [X] T022 [US2] `analytics` → `query_service` (audit_analytics vivo; 3 audits mortos removidos). Suíte 645.
- [~] T023 [US2] `payroll` → **ADIADO** ao Grupo D (ver nota abaixo).

**⚠️ Cluster adiado (T016/T017/T023)**: `coverage → financial → payroll_competency` formam um
cluster acoplado. `financial_snapshot_builder` importa DTOs de `coverage`; suas DTOs
(`FinancialSnapshotData`) são usadas por `domain/payroll/payroll_competency` (agregado vivo via
`payroll_service`), que por sua vez depende de `state_machines` (**Grupo D, fora de escopo**) e de
`base`. Inlinar `financial` em `coverage_service` forçaria `payroll_competency` (domain) a importar
de um service — inversão domain→service que só se resolve colapsando o payroll, o que exige o
Grupo D. Para não trocar a indireção original por uma inversão pior e persistente, o cluster inteiro
(coverage + financial + payroll + base + state_machines) colapsa junto na **feature do Grupo D**.

**Checkpoint US2 ✅**: 6 dos 9 módulos do Grupo B colapsados (`timeline`, `policies`, `projections`,
`explainability`, `kpi`, `analytics`). Cluster `coverage`/`financial`/`payroll` adiado ao Grupo D.
Suíte **638 passed / 0 failed**; `domain/` **88 → 53** arquivos.

---

## Phase 5: User Story 3 — Garantir paridade e não-regressão (Priority: P1)

**Goal**: comprovar (não presumir) que a aplicação entrega as mesmas funcionalidades e contratos
de API de antes.

**Independent Test**: os checks abaixo passam todos.

- [X] T024 [US3] SC-001 — suíte completa: **638 passed / 0 failed / 0 errors**. Total < baseline
  (738) só pelos testes de módulo morto removidos (D3); zero falhas.
- [X] T025 [US3] SC-002 — **0 import de produto** para módulo removido (A + B). Grep sem resultado.
- [X] T026 [US3] SC-003 — `pytest app/tests/integration`: **93 passed / 0 failed** (contratos
  idênticos; o aviso de gate de cobertura no subconjunto não é falha de teste).
- [~] T027 [US3] SC-004 — `domain/` **88 → 53** arquivos. Ainda acima da meta 30–40 porque o
  cluster coverage/financial/payroll + Grupo D permanecem; a meta será atingida na feature do Grupo D.
- [ ] T028 [US3] SC-005 — subir o app dev e percorrer os fluxos (pendente de validação manual no
  navegador; suíte + API verdes já indicam paridade).
- [X] T029 [US3] Prova de escopo: diff da sessão só toca
  `backend/app/{domain,services,use_cases}/`, `backend/app/tests/` e `docs/`/`specs/` — nenhum
  `models`/`api/routes`/`schemas`/migration/`frontend`.

**Checkpoint US3 ✅ (parcial)**: paridade comprovada por suíte + API + imports + escopo. SC-004 fica
parcial (53, não 30–40) pelo cluster adiado; SC-005 (validação manual no navegador) pendente.

---

## Phase 6: Polish & registro

- [ ] T030 Atualizar `docs/HANDOFF.md` (marcar Fase 2 passo 2 concluída, próximo passo = Grupo D
  ou B-06) e confirmar que o rascunho da fórmula de B-06 (T013) ficou registrado em
  `docs/backlog-melhorias.md`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: sem dependências — começa já.
- **Foundational (Phase 2)**: vazia (nada a construir).
- **US1 (Phase 3)**: depende do baseline verde (T001). É o MVP: maior redução, menor risco.
- **US2 (Phase 4)**: recomendado após US1 (base enxuta), mas independente por módulo.
- **US3 (Phase 5)**: validação final — depende de US1 + US2 concluídas.
- **Polish (Phase 6)**: por último.

### Ordem dentro de cada tarefa (loop de segurança — NÃO paralelizar)

Por D1, o refactor é **sequencial, um módulo por commit, suíte verde entre passos**. Por isso quase
nenhuma tarefa é `[P]`: rodar a suíte entre passos pequenos é o que dá o sinal de qual passo
regrediu. Não avançar para o próximo módulo com a suíte vermelha (quickstart: reverter o commit ou
corrigir o inline).

### Dependência específica

- **T014 (`base`) por último** no Grupo A (D4).
- **T013**: copiar a fórmula de remuneração **antes** de deletar o módulo.
- **T023 (`payroll`)** por último no Grupo B (2 consumidores, D6).

---

## Implementation Strategy

### MVP First (US1 — Grupo A)

1. T001–T002: baseline.
2. T003–T014: deletar peso morto, um módulo por commit, suíte verde a cada passo.
3. **PARAR e VALIDAR**: suíte verde + grep limpo + app sobe igual.

### Incremental Delivery

1. Setup → baseline verde.
2. US1 (Grupo A) → maior redução, risco mínimo → validar.
3. US2 (Grupo B) → inline incremental, um módulo por commit → validar.
4. US3 → provar paridade (suíte + imports + contrato + escopo).
5. Cada módulo é um incremento verde rastreável no histórico (SC-006).

---

## Notes

- Rede de segurança = suíte da spec 003; **não** se escrevem testes novos (a spec não os pediu).
- Drive de rede é lento para I/O em massa: ao inspecionar, ler cada arquivo uma vez.
- Dentro do container o path é `app/...` (workdir `/app`), não `backend/app/...`.
- Fora de escopo (não tocar): Grupo C (`constants`/`errors`/`events`), Grupo D
  (`read_models`/`query`/`rules`/`state_machines` + `use_cases/`) e o cálculo de remuneração (B-06).
