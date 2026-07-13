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

- [ ] T001 Rebuild da imagem de teste e rodar a suíte completa para confirmar o baseline verde
  (esperado ~738 passed / 0 failed / 0 errors), registrando o número exato de `passed` como
  referência: `docker build -t plantao360-backend-test ./backend && docker run --rm -e ENVIRONMENT=test plantao360-backend-test python -m pytest -p no:cacheprovider -q`
- [ ] T002 Registrar a contagem inicial de arquivos da `domain/` (linha de base para SC-004):
  `find backend/app/domain -name '*.py' -not -name '__init__.py' | wc -l` (esperado ~118).

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

- [ ] T003 [US1] Deletar `backend/app/domain/entities/` (módulo vazio, prod=0) + limpar reexports.
- [ ] T004 [US1] Deletar `backend/app/domain/services/` (vazio; confunde com `app/services`) + reexports.
- [ ] T005 [US1] Deletar `backend/app/domain/reports/` (vazio, prod=0) + seu teste, se houver.
- [ ] T006 [US1] Deletar `backend/app/domain/calendar/` (prod=0) + seu teste (1) em `backend/app/tests/`.
- [ ] T007 [US1] Deletar `backend/app/domain/metrics/` (prod=0) + seu teste (1).
- [ ] T008 [US1] Deletar `backend/app/domain/snapshots/` (prod=0) + seu teste (1).
- [ ] T009 [US1] Deletar `backend/app/domain/transitions/` (prod=0) + seu teste (1).
- [ ] T010 [US1] Deletar `backend/app/domain/contracts/` (prod=0) + seus testes (2).
- [ ] T011 [US1] Deletar `backend/app/domain/overlap/` (prod=0) + seus testes (3). ⚠️ Confirmar
  antes que a detecção de sobreposição real vive inline em `assignment_service.create()` (trata
  plantão que passa da meia-noite) — `domain/overlap` é duplicata morta, seguro deletar.
- [ ] T012 [US1] Deletar `backend/app/domain/value_objects/` (prod=0, 6 arqs) + seus testes (5).
- [ ] T013 [US1] 🔴 **Antes de deletar**: copiar a fórmula útil `hour_rate × duração = R$` de
  `backend/app/domain/remuneration/remuneration_calculator.py` para o rascunho de B-06 em
  `docs/backlog-melhorias.md` (para não reinventar). **Depois** deletar
  `backend/app/domain/remuneration/` (prod=0, 6 arqs) + seus testes (~14 refs). Deletar o motor
  morto **não** implementa a folha — o gap B-06 permanece registrado (feature separada).
- [ ] T014 [US1] **(ÚLTIMO do grupo)** Confirmar por `grep -rE "app\.domain\.base" backend/app --include=*.py | grep -v /tests/`
  que nenhum módulo remanescente importa `base`; então deletar `backend/app/domain/base/`
  (aggregate_root, prod=0) + seus testes (3).

**Checkpoint**: Grupo A removido. Suíte verde; `find backend/app/domain -name '*.py'` mostra queda
substancial de arquivos. US1 entregue de forma independente e testável (MVP).

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

- [ ] T015 [US2] Inlinar `backend/app/domain/timeline/` (1 consumidor) em
  `backend/app/services/query_service.py`; adaptar teste; deletar o módulo + reexports.
- [ ] T016 [US2] Inlinar `backend/app/domain/coverage/` (1 consumidor) em
  `backend/app/services/coverage_service.py`; adaptar testes; deletar o módulo + reexports.
- [ ] T017 [US2] Inlinar `backend/app/domain/financial/` (1 consumidor) em
  `backend/app/services/coverage_service.py`; adaptar testes; deletar o módulo + reexports.
- [ ] T018 [US2] Inlinar `backend/app/domain/policies/` (2 arqs, 1 consumidor) em
  `backend/app/use_cases/periods` (a camada `use_cases/` fica — Grupo D; só o `policies` entra
  agora); adaptar testes; deletar o módulo + reexports.
- [ ] T019 [US2] Inlinar `backend/app/domain/projections/` (5 arqs, 1 consumidor) em
  `backend/app/services/dashboard_service.py`; adaptar testes; deletar o módulo + reexports.
- [ ] T020 [US2] Inlinar `backend/app/domain/explainability/` (3 arqs, 1 consumidor) em
  `backend/app/services/query_service.py`; adaptar testes; deletar o módulo + reexports.
- [ ] T021 [US2] Inlinar `backend/app/domain/kpi/` (4 arqs, 1 consumidor) em
  `backend/app/services/query_service.py`; adaptar testes; deletar o módulo + reexports.
- [ ] T022 [US2] Inlinar `backend/app/domain/analytics/` (4 arqs, 1 consumidor) em
  `backend/app/services/query_service.py`; adaptar testes; deletar o módulo + reexports.
- [ ] T023 [US2] Inlinar `backend/app/domain/payroll/` (2 arqs, **2 consumidores**: `payroll_service`
  + `payroll_governance_validator`) (D6): embutir a parte de cada um; se a lógica for genuinamente
  compartilhada, mantê-la em **um** lugar (o `payroll_service`) e o validator passa a chamá-lo —
  sem recriar módulo `domain/payroll`. Adaptar testes; deletar o módulo + reexports.

**Checkpoint**: Grupo B colapsado. Suíte verde; `rota → service → model` sem camada de consumidor
único. Grupo C (`constants`/`errors`/`events`) e Grupo D (`read_models`/`query`/`rules`/
`state_machines` + `use_cases/`) permanecem intactos (fora de escopo, FR-008).

---

## Phase 5: User Story 3 — Garantir paridade e não-regressão (Priority: P1)

**Goal**: comprovar (não presumir) que a aplicação entrega as mesmas funcionalidades e contratos
de API de antes.

**Independent Test**: os checks abaixo passam todos.

- [ ] T024 [US3] SC-001 — rodar a suíte completa no Docker: **0 failed / 0 errors** (≥ baseline
  útil; total menor só pelos testes de módulo morto removidos — explicar a diferença).
- [ ] T025 [US3] SC-002 — nenhum import de produto para módulo removido:
  `grep -rE "app\.domain\.(entities|services|reports|calendar|metrics|snapshots|transitions|contracts|overlap|value_objects|remuneration|base|timeline|policies|coverage|financial|projections|analytics|explainability|kpi|payroll)" backend/app --include=*.py | grep -v /tests/`
  → **sem resultado**.
- [ ] T026 [US3] SC-003 — contratos idênticos: `pytest app/tests/integration -q` (test_*_api) verdes.
- [ ] T027 [US3] SC-004 — contar arquivos: `find backend/app/domain -name '*.py' -not -name '__init__.py' | wc -l`
  → **~30–40** (de ~118).
- [ ] T028 [US3] SC-005 — subir o app dev (`docker compose -f docker-compose.yml up -d --build`) e
  percorrer escala/extras/cobertura/dashboard/usuários → comportamento idêntico (usar cache-buster
  `?cb=x` no navegador; ver B-05).
- [ ] T029 [US3] Prova de escopo: `git diff --name-only <baseline>..HEAD` só toca
  `backend/app/{domain,services,use_cases}/`, `backend/app/tests/` e `specs/` — **nenhum** arquivo
  de `models`, `api/routes`, `schemas`, migrations ou `frontend/`.

**Checkpoint**: paridade comprovada pelos três checks (comportamento + imports + contrato) e pela
prova de escopo.

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
