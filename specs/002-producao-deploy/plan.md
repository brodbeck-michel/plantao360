# Implementation Plan: Produção Confiável & Deploy Simples (Fase 0)

**Branch**: `002-producao-deploy` | **Date**: 2026-07-13 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/002-producao-deploy/spec.md`

## Summary

Tornar o deploy de produção **previsível e simples**, movendo o build das imagens para o
GitHub Actions (publicando no GHCR) e migrando o banco de produção de SQLite para PostgreSQL.
No servidor, o deploy passa a ser `docker compose pull && up -d` — sem compilar nada. Migrations
vão para o git e aplicam no boot aguardando o banco; o seed deixa de ter qualquer chance de
rodar em produção; segredos ficam fora da imagem; há backup por `pg_dump`. Nenhuma mudança
funcional (paridade total).

## Technical Context

**Language/Version**: Python 3.12 (backend), Node 20 (build do frontend), imagens Docker.

**Primary Dependencies**: FastAPI, SQLAlchemy 2.0, Alembic (backend); Vite + Nginx (frontend);
Docker Compose; GitHub Actions; GHCR. **Novo**: driver `psycopg2-binary` no backend.

**Storage**: PostgreSQL 16 em produção (serviço no compose). SQLite permanece só em dev/test.

**Testing**: pytest (suíte existente); validação de deploy via `quickstart.md`.

**Target Platform**: Servidor Linux com Docker + Docker Compose, acesso à internet (GHCR).

**Project Type**: Web (backend FastAPI + frontend Nginx) — foco desta feature é operação/deploy.

**Performance Goals**: N/A específico; objetivo é estabilidade (sem loops de restart, sem lock
de banco sob concorrência de dezenas de usuários).

**Constraints**: Simplicidade (constituição): sem Kubernetes, sem orquestradores, sem registries
externos pagos. Apenas GitHub Actions → GHCR e Docker Compose no servidor.

**Scale/Scope**: Aplicação interna, dezenas de usuários; um servidor de produção.

## Constitution Check

*GATE: deve passar antes da pesquisa (Phase 0) e ser reavaliado após o design (Phase 1).*

| Princípio | Avaliação |
|---|---|
| **I. Simplicidade Deliberada** | ✅ Ferramentas mínimas: Actions + GHCR + Compose. Nenhuma camada nova de app. |
| **II. Regra no Backend** | ✅ N/A — mudança operacional, não toca regra de negócio. |
| **III. Testes do que Importa** | ✅ Suíte existente roda no CI; validação de deploy no `quickstart.md`. |
| **IV. Deploy Confiável** | ✅ É a materialização direta deste princípio (Postgres, migrations no git, build no CI, startup determinístico, backup). |
| **V. Foco no Usuário Real** | ✅ Resolve a dor concreta do operador/TI (subir versão sem sofrer). |

**Resultado do gate**: PASS. Nenhuma violação — nenhuma entrada em Complexity Tracking.

## Project Structure

### Documentation (this feature)

```text
specs/002-producao-deploy/
├── plan.md              # Este arquivo
├── research.md          # Decisões técnicas (Phase 0)
├── quickstart.md        # Runbook de deploy e validação (Phase 1)
└── checklists/          # Checklist de qualidade da spec
```

**data-model.md / contracts/**: não se aplicam — feature puramente operacional, sem novas
entidades de domínio nem contratos de API. (Registrado aqui em vez de criar arquivos vazios,
conforme Princípio I.)

### Source Code (arquivos afetados no repositório)

```text
plantao360/
├── docker-compose.prod.yml         # + serviço postgres; image: GHCR (remove build:); depends_on healthy
├── .env.production                 # DATABASE_URL Postgres; POSTGRES_*; DEMO_MODE=false; TAG
├── .env.production.example         # (novo) modelo sem segredos, versionado
├── .gitignore                      # remove exclusão de backend/alembic/versions/*.py
├── backend/
│   ├── requirements.txt            # + psycopg2-binary
│   ├── start.sh                    # + espera do banco antes do alembic upgrade
│   ├── .dockerignore               # garantir exclusão de .env/*.db locais
│   └── alembic/versions/*.py       # passam a ser versionados (git add)
├── scripts/
│   ├── deploy.sh                   # (novo) pull + up -d por TAG (com rollback)
│   └── backup.sh                   # (novo) pg_dump do Postgres
└── .github/workflows/
    └── release-images.yml          # (novo) build + push das imagens para o GHCR
```

**Structure Decision**: manter a estrutura atual do repo; a Fase 0 altera apenas arquivos de
infraestrutura/operação (compose, env, workflow, scripts, requirements, start.sh) e o
versionamento das migrations. Nenhum código de aplicação muda.

## Complexity Tracking

> Sem violações da constituição — seção intencionalmente vazia.

## Fases de execução (visão de alto nível)

O detalhamento em tarefas é do `/speckit-tasks`. Ordem lógica pretendida:

1. **Banco Postgres** (FR-004/005): driver em requirements; serviço postgres no compose; espera
   do banco no `start.sh`; `DATABASE_URL` de produção.
2. **Migrations no git** (FR-007): remover exclusão do `.gitignore`; commitar as migrations
   existentes; validar migração do zero.
3. **Imagens no CI → GHCR** (FR-001/002): workflow `release-images.yml`; trocar `build:` por
   `image:` no compose de produção.
4. **Deploy em um comando + rollback** (FR-003): `scripts/deploy.sh` parametrizado por `TAG`.
5. **Startup seguro / seed manual** (FR-006/008): garantir seed nunca-em-produção; `DEMO_MODE=false`.
6. **Segredos fora da imagem** (FR-009): `.env.production` fora do git (já é), `.example`
   versionado; validar `.dockerignore`.
7. **Backup** (FR-010) e **documentação** (FR-011): `scripts/backup.sh` + `quickstart.md`.

Ver [research.md](./research.md) para as decisões e [quickstart.md](./quickstart.md) para o
runbook de validação.
