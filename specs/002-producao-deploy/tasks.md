# Tasks: Produção Confiável & Deploy Simples (Fase 0)

**Feature**: `002-producao-deploy` | **Plan**: [plan.md](./plan.md) | **Spec**: [spec.md](./spec.md)

Tarefas executáveis e ordenadas por dependência. `[P]` = pode rodar em paralelo (arquivos
distintos, sem dependência pendente). Rótulos `[US#]` mapeiam às histórias da spec.

**Convenção de imagens**: `ghcr.io/brodbeck-michel/plantao360-backend` e `-frontend`.

---

## Phase 1 — Setup

- [x] T001 [P] Criar diretório `scripts/` (se não existir) para os scripts de deploy/backup em `plantao360/scripts/`.
- [x] T002 [P] Criar `plantao360/.env.production.example` com todas as chaves SEM valores sensíveis (`ENVIRONMENT`, `DATABASE_URL`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`, `SECRET_KEY`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `DEMO_MODE=false`, `ALLOWED_ORIGINS`, `TAG`, `BACKEND_PORT`, `FRONTEND_PORT`).
- [x] T003 Confirmar o entrypoint real do backend (`app.main:app` vs `app.api.app:app`) lendo `backend/start.sh` e `backend/app/main.py`; anotar o correto para não alterar por engano.

---

## Phase 2 — Foundational (pré-requisitos compartilhados)

- [x] T004 Adicionar `psycopg2-binary` em `backend/requirements.txt` (driver que a URL `postgresql+psycopg2` de `settings/production.py` já espera).
- [x] T005 [P] Revisar `backend/.dockerignore` para garantir exclusão de `.env*`, `*.db`, `*.sqlite3`, `__pycache__/`, `.pytest_cache/` (nenhum segredo/artefato local na imagem).
- [x] T006 [P] Confirmar em `backend/app/core/settings/production.py` que `DATABASE_URL` vem do ambiente (não hardcoded) e que o valor default não é usado quando `.env.production` define a URL.

---

## Phase 3 — [US2] PostgreSQL em produção (P1)

**Meta**: produção roda sobre Postgres, com o backend aguardando o banco antes de migrar/servir.
**Teste independente**: subir o ambiente prod; migrations aplicam; app lê/grava; sem loop de restart.

- [x] T007 [US2] Adicionar serviço `db` (`postgres:16-alpine`) em `plantao360/docker-compose.prod.yml`: volume `plantao360_pg_data`, `env` `POSTGRES_USER/PASSWORD/DB`, `healthcheck` com `pg_isready`, rede `plantao360_prod`, `restart: always`.
- [x] T008 [US2] No `docker-compose.prod.yml`, remover o volume SQLite `plantao360_prod_data` do backend e adicionar `depends_on: db: { condition: service_healthy }`.
- [x] T009 [US2] Atualizar `plantao360/.env.production`: `DATABASE_URL=postgresql+psycopg2://<user>:<senha>@db:5432/<db>`, definir `POSTGRES_USER/PASSWORD/DB` coerentes, e manter `ENVIRONMENT=production`.
- [x] T010 [US2] Adicionar espera ativa pelo banco em `backend/start.sh` antes do `alembic upgrade head` (loop com timeout testando conexão/`pg_isready`), preservando `set -e` para abortar visível em falha de migração.

---

## Phase 4 — [US3] Migrations versionadas no git (P1)

**Meta**: histórico de schema reproduzível a partir do git, validado em Postgres.
**Teste independente**: checkout limpo + `alembic upgrade head` do zero em Postgres → schema íntegro.

- [x] T011 [US3] Remover a exclusão `backend/alembic/versions/*.py` de `plantao360/.gitignore` (manter o `!.gitkeep`).
- [x] T012 [US3] `git add -f` das migrations existentes em `backend/alembic/versions/*.py` e versioná-las.
- [~] T013 (PENDENTE: exige Postgres real; Docker indisponivel nesta maquina) [US3] **Validar migração do zero em Postgres**: subir só o serviço `db`, rodar `alembic upgrade head` a partir de um banco vazio e confirmar schema completo sem erro.
- [~] T014 (PENDENTE: so apos T013) [US3] Corrigir incompatibilidades SQLite→Postgres encontradas em T013 (ex.: `String` sem length, defaults, `Boolean`, `autoincrement`) nas migrations afetadas em `backend/alembic/versions/`. (Só se T013 acusar erro.)

---

## Phase 5 — [US1] Imagens no CI → GHCR e deploy sem build no servidor (P1)

**Meta**: GitHub Actions constrói/publica as imagens; servidor só baixa e sobe.
**Teste independente**: disparar o workflow, ver imagens no GHCR e subir no servidor sem `--build`.

- [x] T015 [US1] Criar `.github/workflows/release-images.yml`: dispara em push de tag `v*` e `workflow_dispatch`; permissões `contents: read`, `packages: write`; login no GHCR com `GITHUB_TOKEN`.
- [x] T016 [US1] No workflow, job do **backend**: `docker/build-push-action` com `context: ./backend`, tags `ghcr.io/brodbeck-michel/plantao360-backend:{version}` e `:latest`.
- [x] T017 [US1] No workflow, job do **frontend**: build com `context: .` e `dockerfile: frontend/Dockerfile`, `build-args: VITE_MVP_MODE=true`, tags `...plantao360-frontend:{version}` e `:latest`.
- [x] T018 [US1] Trocar `build:` por `image: ghcr.io/brodbeck-michel/plantao360-backend:${TAG:-latest}` (e frontend equivalente) em `docker-compose.prod.yml`.

---

## Phase 6 — [US1] Deploy em um comando + rollback (P1)

- [x] T019 [US1] Criar `plantao360/scripts/deploy.sh`: recebe `TAG` (env/arg), roda `docker compose -f docker-compose.prod.yml pull` e `up -d`; ecoa a tag em uso; falha claramente se a tag não existir no registry.
- [x] T020 [US1] Documentar rollback no cabeçalho do `deploy.sh` (rodar com a `TAG` anterior) e validar que `docker-compose.prod.yml` respeita `${TAG}`.

---

## Phase 7 — [US4] Startup determinístico e seed manual (P2)

**Meta**: em produção nenhum seed roda automaticamente; seed é comando manual.
**Teste independente**: logs de boot de produção sem seed; seed manual popula sob demanda em teste.

- [ ] T021 [US4] Garantir `DEMO_MODE=false` em `plantao360/.env.production` e no `.env.production.example`.
- [ ] T022 [US4] Revisar `backend/start.sh` para confirmar que o bloco de seed só executa em `ENVIRONMENT=development` + `DEMO_MODE=true` (nunca em production); ajustar comentário/guarda se necessário.
- [ ] T023 [P] [US4] Documentar o comando de seed manual (`python -m app.seed.seed_data --dataset demo --clear`) no `quickstart.md`/guia de deploy.

---

## Phase 8 — [US5] Segredos fora da imagem e backup (P2)

**Meta**: imagem sem segredos; backup do Postgres restaurável.
**Teste independente**: inspecionar imagem (sem segredo); gerar e restaurar backup em banco limpo.

- [ ] T024 [US5] Confirmar que `.env.production` continua fora do git (`.gitignore`) e que o compose carrega segredos via `env_file` em runtime (não como `ARG`/`build`).
- [ ] T025 [US5] Criar `plantao360/scripts/backup.sh`: `docker exec plantao360_db pg_dump -U <user> <db>` para `backups/plantao360_<data>.sql`; imprimir caminho gerado.
- [ ] T026 [P] [US5] Documentar restauração (`psql < arquivo.sql`) e recomendação de cron no `quickstart.md`.

---

## Phase 9 — Polish & validação transversal

- [ ] T027 Escrever/atualizar o guia de deploy no `README.md` (ou `docs/deploy.md`): pré-requisitos do servidor, `docker login ghcr.io`, criação do `.env.production`, `deploy.sh`, rollback, backup (FR-011).
- [ ] T028 Verificar se os gates de CI existentes (`.github/workflows/architecture.yml`, `release-readiness.yml`) não bloqueiam o novo `release-images.yml`; se bloquearem indevidamente, relaxar o gate (constituição supera os ADRs de freeze).
- [ ] T029 Executar o checklist de validação do [quickstart.md](./quickstart.md) (SC-001 a SC-008) num ambiente de teste e registrar o resultado.
- [ ] T030 Remover artefatos obsoletos de SQLite em produção (referências ao volume `plantao360_prod_data` e ao caminho `/app/data/*.db` no compose/env de produção) após confirmar que Postgres está estável.

---

## Dependências (ordem de conclusão)

```
Setup (P1-T003) → Foundational (T004-T006)
   → US2 Postgres (T007-T010)
        → US3 Migrations/validação (T011-T014)   [T013 exige Postgres de US2]
        → US1 Imagens+compose (T015-T018) → US1 Deploy/rollback (T019-T020)
   → US4 Startup/seed (T021-T023)
   → US5 Segredos/backup (T024-T026)   [T025 exige serviço db de US2]
→ Polish (T027-T030)
```

- **US2 é pré-requisito** de validação de US3 (T013) e do backup US5 (T025).
- **US1 (imagens/deploy)** depende do serviço `db` já existir no compose (US2), pois altera o
  mesmo arquivo `docker-compose.prod.yml`.
- US4 é largamente independente (config/boot), pode andar em paralelo a US1 após Foundational.

## Oportunidades de paralelismo

- Setup: T001, T002 em paralelo.
- Foundational: T005, T006 em paralelo (após T004).
- Documentação: T023, T026 em paralelo dentro de suas fases.

## Escopo de MVP (mínimo que já entrega valor)

**US2 + US1** (Postgres em produção + imagens no CI com deploy por `pull && up -d`) já elimina as
duas dores centrais: banco frágil e build no servidor. US3 (migrations no git) deve acompanhar
US2 por segurança do schema. US4/US5 endurecem operação e podem vir logo em seguida.

## Total

30 tarefas — US1: 6, US2: 4, US3: 4, US4: 3, US5: 3, Setup/Foundational: 6, Polish: 4.
