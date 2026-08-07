# Tasks: Log de auditoria das ações do usuário

**Input**: Design documents from `/specs/007-log-auditoria/`

**Prerequisites**: [plan.md](plan.md), [spec.md](spec.md), [research.md](research.md), [data-model.md](data-model.md), [quickstart.md](quickstart.md)

**Tests**: feature de comportamento novo — testes são parte da entrega, não opcionais (FR-012).
Cada fase tem seus testes escritos **junto** com o código da fase, e o gate de commit exige a
suíte verde. Comando e baseline no [quickstart.md](quickstart.md) §1.

**Organization**: ordem **de dentro para fora** (fundação → gravação → consulta → interface).
Cada fase é um commit. As fases são sequenciais; `[P]` marca tarefas paralelizáveis dentro da
mesma fase (arquivos diferentes, sem dependência entre si).

## Format: `[ID] [P?] [Story] Description`

---

## Phase 1: Setup (baseline)

**Purpose**: ponto de retorno limpo e número de referência da suíte

- [ ] T001 Registrar baseline: rodar a suíte (quickstart §1) e anotar a contagem neste arquivo
  (esperado: **411 passed / 2 failed ambientais** — as 2 falhas de `test_settings_factory` são
  pré-existentes, confirmadas em 2026-08-07 por `git stash`; **não** corrigir nesta spec);
  confirmar `git status` limpo

---

## Phase 2: Foundational — tabela, modelo e service de gravação (commit 1)

**Purpose**: infraestrutura que todas as user stories consomem. Bloqueia US1, US2 e US3.

**Goal**: `audit_logs` existe, o service grava na transação da chamadora, e o esqueleto morto sai.

**Independent Test**: teste unitário do service grava `create`/`update`/`delete` num banco em
memória e valida as invariantes do [data-model.md](data-model.md); ciclo de migration OK.

- [ ] T002 [P] Criar `backend/app/models/audit_log.py` com o modelo `AuditLog` conforme
  [data-model.md](data-model.md) (colunas, FK `user_id` com `ON DELETE SET NULL`, 4 índices);
  registrar em `backend/app/models/__init__.py`
- [ ] T003 [P] Criar migration `backend/alembic/versions/20260807_011_audit_logs.py`
  (`down_revision = "010_user_doctor_link"`): upgrade cria a tabela + índices; downgrade dropa
- [ ] T004 Criar `backend/app/services/audit_service.py` com `record(...)` e `record_many(...)`:
  recebem o `session` e o usuário autenticado, fazem `add`/`add_all` **sem commit** (a rota
  chamadora commita — D1/D2 do plan); montam `before`/`after` a partir da lista explícita de
  campos por recurso e geram o `summary` legível (D5)
- [ ] T005 Deletar os contratos mortos `backend/app/audit/models.py` e
  `backend/app/audit/service.py` e os testes que só os exercitam
  (`app/tests/unit/test_audit_models.py`, `test_audit_interface.py`); **manter**
  `backend/app/audit/events.py` (enum `AuditAction`) e `test_audit_actions.py` (D3 do plan)
- [ ] T006 [P] Criar `backend/app/tests/unit/test_audit_service.py`: grava as 3 ações; valida
  invariantes 2–5 do data-model (`create` sem `before`, `delete` sem `after`, `update` só com
  campos alterados, `origin='system'` ⇒ `user_id` nulo)
- [ ] T007 Gate + commit: suíte verde; ciclo de migration num banco limpo (quickstart §2);
  commit `feat(audit): tabela audit_logs + service de gravação (spec 007)`

**Checkpoint**: fundação pronta — as fases seguintes só chamam o service.

---

## Phase 3: User Story 1 — Registrar alterações da escala e horas extras (P1) 🎯 MVP

**Goal**: toda inclusão, alteração e remoção de plantão e de hora extra fica registrada com autor.

**Independent Test**: quickstart §3 — criar/alterar/remover atribuição e conferir os 3 registros,
incluindo o `before` preservado na remoção (SC-002).

### Passo 3a — Escala (commit 2)

- [ ] T008 [US1] Instrumentar `backend/app/api/routes/assignment.py`: gravar `create` no POST,
  `update` no PUT (com o estado anterior lido **antes** da alteração) e `delete` no DELETE (com o
  estado lido **antes** da exclusão), sempre no mesmo `session`, antes do `db.commit()`
- [ ] T009 [US1] Instrumentar as rotas de lote (duplicar dia / duplicar semana) usando
  `record_many` — um registro por atribuição criada (D2 do plan)
- [ ] T010 [P] [US1] Criar `backend/app/tests/integration/test_audit_assignment_api.py`: um teste
  por ação provando o registro (SC-003) + teste de **rollback** (operação que falha não deixa
  registro — SC-004)
- [ ] T011 [US1] Gate + commit: suíte verde; validação manual do quickstart §3.1;
  commit `feat(audit): registra alterações da escala (spec 007, US1)`

### Passo 3b — Horas extras (commit 3)

- [ ] T012 [US1] Instrumentar `backend/app/api/routes/extra.py`: `create` no POST, `delete` no
  DELETE e `update` nas transições de status (aprovar/rejeitar/cancelar)
- [ ] T013 [P] [US1] Criar `backend/app/tests/integration/test_audit_extra_api.py` cobrindo as
  ações acima
- [ ] T014 [US1] Gate + commit: suíte verde; validação manual do quickstart §3.2;
  commit `feat(audit): registra alterações de horas extras (spec 007, US1)`

### Passo 3c — Cadastros (commit 4)

- [ ] T015 [P] [US1] Instrumentar `backend/app/api/routes/doctors.py` (create, update,
  ativar/inativar) — incluindo mudanças de RQE e data de carreira, que alteram o valor/hora
- [ ] T016 [P] [US1] Instrumentar `backend/app/api/routes/users.py` (create, update,
  ativar/inativar, troca de senha). A troca de senha grava **apenas**
  `{"password_changed": true}` — nunca a senha ou o hash (FR-004)
- [ ] T017 [P] [US1] Instrumentar `backend/app/api/routes/period.py` (create, update, mudança de
  status/fechamento)
- [ ] T018 [P] [US1] Criar `backend/app/tests/integration/test_audit_cadastros_api.py`, com um
  teste dedicado que inspeciona o conteúdo gravado ao criar/alterar usuário e falha se encontrar
  qualquer credencial (SC-006)
- [ ] T019 [US1] Gate + commit: suíte verde; quickstart §4 (senha não aparece);
  commit `feat(audit): registra alterações de médicos, usuários e competências (spec 007, US1)`

**Checkpoint**: a trilha já responde "quem alterou este turno" — valor principal entregue.

---

## Phase 4: User Story 2 — Consultar o histórico (P2)

**Goal**: gestão consulta a trilha por API, com filtros, paginação e bloqueio por perfil.

**Independent Test**: quickstart §3 (consulta com filtros) e §5 (403 para MEDICO).

- [ ] T020 [P] [US2] Criar `backend/app/schemas/audit/`: `AuditLogResponseDTO` e o DTO de filtros
  (usuário, recurso, id de recurso, competência, intervalo de datas, paginação)
- [ ] T021 [US2] Adicionar ao `audit_service` a consulta paginada, ordenada por `occurred_at`
  decrescente, usando os índices do data-model
- [ ] T022 [US2] Criar `backend/app/api/routes/audit.py` com **apenas** `GET /audit`
  (somente-leitura — FR-007), protegido por `require_role("ADMIN", "COORDENADOR")`; registrar o
  router em `backend/app/api/app.py`
- [ ] T023 [P] [US2] Criar `backend/app/tests/integration/test_audit_api.py`: filtros (por autor,
  por recurso, por intervalo), paginação/ordenação, e **403** para MEDICO, CONSULTA e FINANCEIRO
  (SC-005)
- [ ] T024 [US2] Gate + commit: suíte verde; quickstart §3 e §5;
  commit `feat(audit): endpoint de consulta da trilha (spec 007, US2)`

**Checkpoint**: trilha consultável sem acesso ao banco (SC-001).

---

## Phase 5: User Story 3 — Aba de histórico no workspace (P3)

**Goal**: o gestor investiga sem sair da tela onde monta a escala; o médico não vê a aba.

**Independent Test**: quickstart §6 — como ADMIN vê a aba com os eventos; como MEDICO a aba não
existe.

- [ ] T025 [P] [US3] Criar `frontend/src/features/operational/services/audit-api.ts` (cliente da
  consulta, com paginação)
- [ ] T026 [P] [US3] Adicionar o módulo `auditoria` em `frontend/src/rbac.ts` (`full` para ADMIN,
  `view` para COORDENADOR, `none` para os demais)
- [ ] T027 [US3] Criar `frontend/src/features/operational/components/tabs/AuditTab.tsx`: lista
  paginada por competência (autor, ação, alvo, horário, resumo), com estado vazio que informa
  desde quando a trilha existe (edge case da spec)
- [ ] T028 [US3] Registrar a aba em `WorkspaceTabs.tsx` (novo índice em `WORKSPACE_TAB`) e
  renderizá-la em `workspace-page.tsx` apenas para os perfis autorizados, reaproveitando o
  mecanismo `visibleTabs` já existente
- [ ] T029 [US3] Gate + commit: build do frontend sem erro de tipo; validação no navegador como
  ADMIN e como MEDICO com screenshot (quickstart §6);
  commit `feat(audit): aba de histórico da competência no workspace (spec 007, US3)`

---

## Phase 6: Fechamento

- [ ] T030 Validar a paridade das jornadas (quickstart §7), incluindo o tempo de resposta da
  duplicação de semana (D2 do plan)
- [ ] T031 Atualizar documentação: `docs/HANDOFF.md` (a trilha existe, quais rotas gravam e a
  **regra para novas rotas**: toda rota que alterar as 5 entidades precisa gravar) e
  `docs/backlog-melhorias.md` (dívidas registradas: expurgo/retenção da trilha; `user_id` nos logs
  estruturados + volume de logs em produção; trilha visível ao próprio médico)
- [ ] T032 Registrar o resultado final na seção **Progresso** deste arquivo (contagem da suíte,
  linhas adicionadas/removidas, evidências dos SC) e commitar

---

## Dependências

```text
Phase 1 (baseline)
   └── Phase 2 (fundação: tabela + service)   ← bloqueia todo o resto
         ├── Phase 3 (US1 — gravação)  🎯 MVP entregue aqui
         │     └── Phase 4 (US2 — consulta)   ← precisa de dados gravados para testar
         │           └── Phase 5 (US3 — interface)  ← consome o endpoint da US2
         └── Phase 6 (fechamento)
```

**Paralelização**: dentro de cada fase, as tarefas `[P]` tocam arquivos distintos e podem ser
feitas em qualquer ordem. Entre fases, não — cada uma depende do checkpoint anterior.

**Parada segura**: ao final da **Phase 3** a feature já entrega o valor central (a pergunta
original do stakeholder é respondida, ainda que via banco/API). Phases 4 e 5 são acesso e
conveniência.

---

## Progresso

*(preencher durante a execução)*

## Resultado final

*(preencher em T032)*
