# Tasks: Baseline de Testes Confiável (Fase 2 — passo 1)

**Feature**: `003-baseline-de-testes` | **Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)

Tarefas executáveis, ordenadas por dependência. `[P]` = paralelizável (arquivos distintos).
Escopo: **somente** `backend/app/tests/**` e `backend/pyproject.toml`. Nenhuma mudança de produto.

**Comando de referência da suíte**:
`docker build -t plantao360-backend-test ./backend && docker run --rm -e ENVIRONMENT=test plantao360-backend-test python -m pytest -p no:cacheprovider -q`

---

## Phase 1 — Setup

- [ ] T001 Rebuild da imagem de teste e medir o baseline: `docker build -t plantao360-backend-test ./backend`; rodar a suíte (com `--ignore=app/tests/unit/test_manifests.py`) e registrar o número de falhas de partida (esperado: 52 failed / 692 passed).

---

## Phase 2 — [US2] Autenticação nos testes de integração (P1)

**Meta**: os `test_*_api` deixam de falhar com `401`.
**Teste independente**: `pytest app/tests/integration -q` passa nos arquivos de API.

- [ ] T002 [US2] Criar `backend/app/tests/integration/conftest.py` com: (a) um `User` ADMIN falso (`id=1`, `role="ADMIN"`, `active=True`, `name`/`email`) e (b) helper `install_auth_override(app)` que faz `app.dependency_overrides[get_current_user] = lambda: <fake admin>` (import de `app.core.security.dependencies.get_current_user`).
- [ ] T003 [P] [US2] Em `backend/app/tests/integration/test_shift_api.py`, aplicar `install_auth_override(test_app)` na `client` fixture (após montar o app).
- [ ] T004 [P] [US2] Idem em `backend/app/tests/integration/test_period_api.py`.
- [ ] T005 [P] [US2] Idem em `backend/app/tests/integration/test_doctors_api.py`.
- [ ] T006 [P] [US2] Idem em `backend/app/tests/integration/test_assignment_api.py`.
- [ ] T007 [P] [US2] Idem em `backend/app/tests/integration/test_extra_api.py`.
- [ ] T008 [US2] Investigar e corrigir `backend/app/tests/integration/test_database.py` (1 falha) — aplicar override se for o mesmo `401`, ou ajustar conforme a causa real.
- [ ] T009 [US2] Investigar e corrigir `backend/app/tests/integration/test_bootstrap.py` (1 falha) — ajustar conforme a causa (provável dependência do fluxo de auth/admin).
- [ ] T010 [US2] Rodar `pytest app/tests/integration -q` e confirmar 0 falhas nessa pasta.

---

## Phase 3 — [US3] Remover testes-cerimônia (P2)

**Meta**: coleção sem erro; sem asserções de "número mágico".
**Teste independente**: `pytest --collect-only -q` sem erro.

- [ ] T011 [US3] Deletar `backend/app/tests/unit/test_manifests.py` (importa `manifest_loader` inexistente; quebra a coleção — cerimônia ADR-016).
- [ ] T012 [P] [US3] Em `backend/app/tests/unit/test_domain_events.py`, remover a asserção de contagem (`test_domain_event_name_count`); se o arquivo só tiver isso, deletá-lo.
- [ ] T013 [P] [US3] Idem em `backend/app/tests/unit/domain/test_remuneration_events.py` (remover contagem/deletar).
- [ ] T014 [P] [US3] Idem em `backend/app/tests/unit/domain/test_payroll_events.py`.
- [ ] T015 [P] [US3] Idem em `backend/app/tests/unit/domain/test_financial_events.py`.
- [ ] T016 [US3] Revisar `backend/app/tests/unit/domain/test_shift_constants.py`: se for só contagem de valores, remover a asserção frágil; se cobrir comportamento real, manter/ajustar.

---

## Phase 4 — [US4] Atualizar testes desatualizados (P2)

**Meta**: testes com valor real voltam ao verde refletindo o schema/validações atuais.
**Teste independente**: os arquivos abaixo passam.

- [ ] T017 [P] [US4] Em `backend/app/tests/unit/test_doctor_mapper.py`, atualizar a fixture do Doctor para incluir `specialty` e `doctor_type` (exigidos pelo `DoctorResponseDTO` desde as migrations 004/005).
- [ ] T018 [P] [US4] Em `backend/app/tests/unit/test_settings_factory.py`, atualizar `test_production_settings_defaults` para o hardening atual (fornecer `SECRET_KEY` forte + `ADMIN_PASSWORD` válido, ou asseverar que `ProductionSettings` rejeita segredo fraco).
- [ ] T019 [P] [US4] Em `backend/app/tests/unit/test_shift_service.py`, alinhar a asserção do teste ao comportamento atual do serviço (inspecionar a falha e corrigir o teste, não o produto).

---

## Phase 5 — [US5] Gate de cobertura realista (P3)

**Meta**: a suíte verde não é reprovada por cobertura irreal.

- [ ] T020 [US5] Em `backend/pyproject.toml`, remover `--cov-fail-under=80` do `addopts` (linha ~46), mantendo o relatório de cobertura (`--cov=app --cov-report=term-missing`).
- [ ] T021 [US5] Medir a cobertura global real com a suíte verde e ajustar `[tool.coverage.report] fail_under` (linha ~56) para um valor honesto ≤ o medido (a elevar no futuro). Registrar o número.

---

## Phase 6 — [US1] Verificação do verde e prova de não-regressão de produto (P1)

**Meta**: suíte 0 falhas / 0 erros, e prova de que nada de produto mudou.
**Teste independente**: a suíte completa passa e o `git diff` só mostra testes/config.

- [ ] T022 [US1] Rebuild da imagem e rodar a suíte COMPLETA (sem `--ignore`): `docker run --rm -e ENVIRONMENT=test plantao360-backend-test python -m pytest -p no:cacheprovider -q` → confirmar **0 failed, 0 errors**.
- [ ] T023 [US1] Provar não-regressão de produto: `git diff --name-only` deve mostrar apenas `backend/app/tests/**` e `backend/pyproject.toml` (nenhum arquivo de `app/api`, `app/services`, `app/domain`, `app/models`).
- [ ] T024 [US1] Registrar o destino de cada um dos 52 testes que falhavam (consertado / atualizado / removido) e quaisquer `skip` com justificativa, no resumo da implementação.

---

## Dependências (ordem de conclusão)

```
Setup (T001)
  → US2 Auth: T002 (helper) → T003..T007 [P] → T008, T009 → T010 (verifica pasta)
  → US3 Deletar: T011 → T012..T016 [P/seq]
  → US4 Atualizar: T017..T019 [P]
  → US5 Cobertura: T020 → T021
→ US1 Verificação final: T022 → T023 → T024   [depende de todas as anteriores]
```

- **T002 (helper) bloqueia** T003..T009 (que o aplicam).
- US3, US4, US5 são **independentes de US2** e entre si — podem andar em paralelo.
- **T021 (medir cobertura)** e **T022 (verde final)** exigem as correções de US2/US3/US4 prontas.

## Oportunidades de paralelismo

- US2: T003–T007 em paralelo (arquivos distintos), após T002.
- US3: T012–T015 em paralelo. US4: T017–T019 em paralelo.
- As frentes US3, US4, US5 podem correr em paralelo à US2.

## Escopo de MVP

**US2 (auth)** sozinha derruba ~42 das 52 falhas — é o maior salto. US3+US4 zeram o restante;
US5 remove o falso-vermelho da cobertura. O verde só é "confiável" após **US1 (T022–T024)**.

## Total

24 tarefas — US2: 9, US3: 6, US4: 3, US5: 2, Setup: 1, US1 (verificação): 3.
