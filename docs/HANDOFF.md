# HANDOFF — Plantão 360 (contexto para continuar em outra conversa)

**Atualizado:** 2026-07-13. Leia este arquivo primeiro; ele resume tudo que foi decidido e feito.
Detalhes vivos em `.specify/memory/constitution.md`, `docs/levantamento-domain.md`,
`docs/backlog-melhorias.md` e `specs/00X-*/`.

## O que é o projeto

App interno da **Unimed Tubarão** para gestão de plantões médicos do PS (intranet, dezenas de
usuários). Fica em `plantao360/`. Backend **FastAPI + SQLAlchemy 2 + Alembic**; frontend
**React 18 + TypeScript + MUI + React Query + Vite**. Repo git: `github.com/brodbeck-michel/plantao360`.

## A missão (o "porquê")

O backend estava **super-engenhariado** (~25k linhas, 495 arquivos py, camada `domain/` com 118
arquivos em DDD/CQRS/event-sourcing). O frontend está bem dimensionado. **Decisão: simplificar,
não reescrever** — "simples, mas bem feito", mantível por uma pessoa, com **paridade funcional**
(nada que o usuário usa some).

Papel do assistente: **arquiteto de desenvolvimento**. Trabalho orientado a spec via **Spec Kit**
(skills `speckit-*` em `.claude/skills`; fluxo constitution → specify → plan → tasks → implement).

## Constituição (`.specify/memory/constitution.md`, v1.1.0) — 5 princípios

- **I. Simplicidade Deliberada** (não-negociável): proíbe abstração de consumidor único; máx
  `rota → service → model`; nada de CQRS/engines para o que cabe em função.
- **II. Regra de negócio no backend** (frontend só apresenta).
- **III. Testes do que importa** (testa o que erra caro; não persegue cobertura trivial).
- **IV. Deploy Confiável** (Postgres em prod, migrations no git, build no CI, seed manual, backup).
- **V. Foco no usuário real.**
- **Supera os 31 ADRs de "freeze"** (viram histórico).

## Modelo de produto confirmado (spec 001)

- Papéis: **Médico**, **Gestão** (coordena escala + financeiro), **Admin/TI**.
- **Auto-escala**: Gestão abre período+plantões; médico **se inscreve**. Gestão também aloca/confere.
- **Extras e trocas SEM aprovação prévia** (contam direto; revisão no fechamento).
- **Remuneração**: tabela de valores por médico/tipo; calcular + exportar. ⚠️ **VER B-06 (gap)**.
- 8 capacidades mantidas: períodos/plantões, escala, extras, cobertura/trocas, remuneração,
  dashboard, auditoria, RBAC.

## Progresso por fase

- **Fase 0 — Produção & Deploy: CONCLUÍDA E VALIDADA** (spec 002). Postgres em prod, migrations no
  git, imagens no GitHub Actions → GHCR, `scripts/deploy.sh` (`TAG=vX ./scripts/deploy.sh`),
  `scripts/backup.sh`, seed manual, `docs/deploy.md`. Validado end-to-end com Docker. **Bug real
  corrigido**: migration 004 usava `PRAGMA` (SQLite) → trocado por inspector do SQLAlchemy.
- **Fase 1 — Escopo: CONCLUÍDA** (constituição + spec 001).
- **Fase 2 passo 1 — Baseline de testes: CONCLUÍDA** (spec 003). Suíte de **692✓/52✗/1-erro → 738
  passed / 0 failed / 0 errors**. Fix de causa única: `backend/app/tests/integration/_auth.py`
  (override de `get_current_user` por ADMIN falso). Gate de cobertura 80%→65 (real ~69%).
- **Fase 2 passo 2 — Colapso da `domain/`: EM ANDAMENTO (Grupos A+B parciais concluídos)** (spec
  004). `tasks.md` gerado e executado. **Grupo A (deletar)**: 9 módulos removidos por inteiro;
  `value_objects` e `remuneration` reduzidos só ao que é vivo; `base` adiado. **Grupo B (inline)**:
  6 módulos colapsados (`timeline`, `policies`, `projections`, `explainability`, `kpi`, `analytics`).
  Suíte **738 → 738 → 638 passed / 0 failed** (queda só de testes de módulo morto); `domain/`
  **88 → 53** arquivos; 0 import de produto quebrado; escopo só backend interno.
  **Adiado ao Grupo D**: cluster `coverage → financial → payroll` (acoplado a `state_machines`
  Grupo D e ao agregado `payroll_competency`; inlinar forçaria inversão domain→service persistente)
  + `base` + `value_objects/shift_time_range` + as data classes de `remuneration` (todas ainda
  consumidas por `rules`/`state_machines`/`payroll`). Detalhe em `specs/004-colapso-domain/tasks.md`.

## Levantamento da `domain/` (o mapa do colapso) — `docs/levantamento-domain.md`

- **Grupo A — DELETAR** (prod=0, ~23 arqs): entities, services, reports, calendar, metrics,
  snapshots, transitions, contracts, overlap, value_objects, remuneration, base. (`base` por
  ÚLTIMO — tem 4 usos internos.) Testes deles saem junto (~21 arquivos).
- **Grupo B — INLINE** (consumidor único, ~20 arqs): timeline→query_service,
  policies→use_cases/periods, coverage→coverage_service, financial→coverage_service,
  projections→dashboard_service, kpi→query_service, analytics→query_service,
  explainability→query_service, payroll→payroll_service (2 consumidores).
- **Grupo C — MANTER**: constants, errors, events.
- **Grupo D — DEPOIS**: read_models, query, rules, state_machines + colapsar `use_cases/`.
- Meta: `domain/` **118 → ~30-40 arquivos**.

**Mecânica (plan spec 004):** inline-and-delete **incremental, 1 módulo por commit**, suíte verde
entre passos. Verificação de paridade tripla: suíte 0 falhas + grep sem import de produto quebrado
+ testes de API verdes (contratos idênticos).

## ⚠️ Alertas verificados

- **overlap**: NÃO é gap — detecção existe inline em `assignment_service.create()` (trata plantão
  noturno). `domain/overlap` é duplicata morta → seguro deletar.
- **remuneration**: **GAP REAL (B-06)** — a folha NUNCA calcula valor (`Payroll` sem campo de
  valor; snapshots só somam duração; único `hour_rate×duração` no motor morto `domain/remuneration`).
  A capacidade "calcular+exportar folha" **não existe**. É **feature a construir** (simples), não
  simplificação. Antes de deletar o motor, copiar a fórmula para o rascunho de B-06.

## Backlog (`docs/backlog-melhorias.md`) — todos frontend, exceto B-06

- **B-01** criar usuário: ✅ RESOLVIDO (erro genérico escondido + validação; commit ba5601c).
- **B-02** aba Turno sem separador dia/turno (UI).
- **B-03** dashboard escolher competência (UI + talvez param no endpoint).
- **B-04** dialog "Alterar senha" com mesmo erro-escondido do B-01.
- **B-05** Nginx cacheia `index.html` no deploy → `Cache-Control: no-cache` em `docker/nginx/nginx.conf`.
- **B-06** 🔴 cálculo de remuneração/folha não implementado (ALTA; feature).

## Como rodar/testar (Docker do usuário funciona após reiniciar o PC)

- **App dev** (com dados demo): `docker compose -f docker-compose.yml up -d --build`
  → frontend http://localhost:3001, Swagger http://localhost:8000/api/v1/docs.
  Login admin dev: `admin@plantao360.local` / `admin123`.
- **Suíte de testes**:
  `docker build -t plantao360-backend-test ./backend && docker run --rm -e ENVIRONMENT=test plantao360-backend-test python -m pytest -p no:cacheprovider -q`
- **App dev usa BUILD ESTÁTICO** (nginx), não HMR: mudança no frontend exige
  `docker compose up -d --build frontend`; e o navegador cacheia `index.html` → recarregar com
  cache-buster `?cb=x` (ver B-05).

## Armadilhas conhecidas

- Drive de rede (`\\sfs01\...`) é lento para I/O em massa: em scripts, ler cada arquivo **uma
  vez** (não N×). Git avisa CRLF/LF — inofensivo.
- Dentro do container o path é `app/...` (workdir `/app`), não `backend/app/...`.
- `git commit` já usa `Co-Authored-By: Claude Opus 4.8`. Estamos na branch `master`.
- Spec Kit: sem hooks (`.specify/extensions.yml` não existe). `.specify/feature.json` aponta para
  a feature ativa (hoje `specs/004-colapso-domain`).

## Estado do git (principais commits, mais recente por último)

fase0 (Postgres/deploy/migrations, validado) → spec001 escopo → spec002 fase0 →
spec003 baseline testes (28b0c27 US2, dd10619 US3/4/5) → ba5601c fix B-01 →
e075a70+212bb8b levantamento domain → 872224c spec004 → 3af57e6 plan004.

## PRÓXIMO PASSO IMEDIATO

**Fase 2 dá-se por SUFICIENTE (meta de tamanho atingida).** spec 004 (Grupos A+B) + spec 005
(Grupo D, US1+US2) reduziram `domain/` de **118 → 32** arquivos (meta era 30–40). Suíte **632 verde**;
93 testes de API verdes; 0 inversão domain→service; SC-005 (spec 004) validado no navegador.

**spec 005 — o que foi feito (US1+US2)**: `read_models`/`query` → services; `rules`/`state_machines`
inlinados por vertical (assignments/shift/extra/periods); `use_cases/assignments` (morto) removido;
`use_cases/periods` (orquestração viva) mantido; `value_objects`/`rules` removidos; `BusinessRuleCode`
→ `constants`.

**spec 005 — US3 ADIADA (dívida B-07)**: o cluster `payroll_competency` (agregado 717 linhas) +
`governance` + `coverage`/`financial`/`remuneration`/`base`/`payroll_state_machine` ficou em `domain/`.
Decisão do usuário: a meta de tamanho já foi atingida; colapsar o agregado mecanicamente só
relocaria ~1000 linhas (não reduz). Fazer via análise do fluxo real de folha — casa com B-06.

**Próximos passos possíveis:**
1. **B-06 + B-07 juntos** (recomendado): implementar o cálculo de folha (B-06) e, no mesmo fluxo,
   reduzir/colapsar o cluster payroll (B-07) — mesmo código, uma feature só.
2. **Backlog frontend**: B-02/B-03/B-04/B-05.
3. **Fase 3**: limpeza de docs/ADRs antigos + gates de CI legados + migrations rodando 2×.
