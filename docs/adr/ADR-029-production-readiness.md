# ADR-029: Production Readiness

**Date:** 2026-06-29
**Status:** Accepted
**Sprint:** 14.3 — Production Readiness & Technical Debt Closure

---

## Context

O Plantão 360 atingiu maturidade técnica que exige definição formal de como o sistema se comporta em cada ambiente. Até a Sprint 14.2, existiam múltiplos padrões concorrentes: seed executava `create_all()` bypassando Alembic, Dockerfile único rodava seed demo em todos os ambientes, `DEMO_MODE` era definido mas nunca lido pelo código Python, e não existia handler de lifespan no FastAPI. A Sprint 14.3 ETAPA 3 consolidou o **RuntimeManager**, o **Lifespan Handler** e o **start.sh** como pontos únicos de inicialização, mas a documentação arquitetural e as definições de responsabilidade ainda não estavam formalizadas em um ADR.

Este ADR formaliza as decisões de Production Readiness já implementadas, documenta as responsabilidades de cada componente e estabelece as Quality Gates que garantem compliance contínua.

---

## Decision

Declaramos a **Production Readiness** do Plantão 360 com os seguintes elementos:

### 1. Runtime Modes

O sistema opera em **quatro modos de execução**, cada um com fluxo de inicialização distinto. A decisão é tomada por um único componente: `RuntimeManager` (`app/core/runtime.py`).

| Modo | Variável | Seed | Migrations | Uvicorn | Uso |
|------|----------|------|------------|---------|-----|
| **DEMO** | `ENVIRONMENT=development` + `DEMO_MODE=true` | Automático (`--dataset demo --clear`) | `alembic upgrade head` | Com `--reload` | Desenvolvimento com dados fictícios |
| **DEVELOPMENT** | `ENVIRONMENT=development` + `DEMO_MODE=false` | Manual (via CLI) | `alembic upgrade head` | Com `--reload` | Desenvolvimento sem dados automáticos |
| **PRODUCTION** | `ENVIRONMENT=production` | Nunca automático | `alembic upgrade head` | Sem `--reload`, com resource limits | Ambiente de produção |
| **TEST** | `ENVIRONMENT=test` | Nunca (fixtures criam dados isolados) | `create_all()` via fixtures | Sem `--reload` | Testes automatizados |

**Detecção:**
- `ENVIRONMENT=test` → TEST
- `ENVIRONMENT=production` → PRODUCTION
- `ENVIRONMENT=development` + `DEMO_MODE=true` → DEMO
- `ENVIRONMENT=development` + `DEMO_MODE=false` → DEVELOPMENT
- Qualquer outro valor → DEVELOPMENT

**Responsabilidade do RuntimeManager:**
- Detectar modo de execução a partir de `ENVIRONMENT` + `DEMO_MODE`
- Executar migrations (`alembic upgrade head`)
- Executar seed (apenas em modo DEMO)
- Reportar status da inicialização

**NÃO é responsável por:**
- Lógica de negócio
- Geração de dados (responsabilidade do seed)
- Definição de schema (responsabilidade do Alembic)

### 2. Alembic Strategy

Alembic é a **única fonte de verdade** para o schema do banco de dados. O seed **nunca** executa `create_all()`.

- **Arquivo de configuração:** `backend/alembic.ini`
- **Script location:** `backend/alembic/`
- **Banco padrão:** `sqlite:///./plantao360.db`
- **Fluxo de schema:**
  1. Alembic mantém o controle de versão do schema
  2. `alembic upgrade head` é executado pelo RuntimeManager em modos DEMO/DEVELOPMENT/PRODUCTION
  3. Modo TEST utiliza `Base.metadata.create_all()` via fixtures (isolamento de testes)
- **Migrações existentes:**
  - `001_init` — Schema inicial (doctors, periods, shifts, shift_parts, shift_extras, payroll, coverage, financial_facts, financial_snapshots)
  - `003_runtime_alignment` — Alinhamento com RuntimeManager (CHECK constraints, FK constraints)
- **Regra:** Todo change de schema requer migration. O seed apenas popula dados — nunca modifica schema.

### 3. Seed Strategy

O módulo de seed (`app/seed/`) é responsável **apenas** pela geração de dados. Schema é responsabilidade do Alembic.

**CLI Unificada:**
```bash
python -m app.seed run <profile> [--clear]
python -m app.seed --dataset <dataset> [--clear]  # backward compatibility
```

**Perfis Disponíveis:**

| Perfil | Descrição | Uso |
|--------|-----------|-----|
| `demo` | Dados fictícios completos para demonstração | Modo DEMO |
| `development` | Dados mínimos para desenvolvimento | Desenvolvimento local |
| `edge` (edge_cases) | Casos de borda para validação | Testes manuais |
| `empty` | Schema vazio, sem dados | Testes limpos |

**Backward Compatibility:**
- `--dataset demo` → mapeia para perfil `demo`
- `--dataset edge_cases` → mapeia para perfil `edge`
- `--dataset showcase` → mapeia para perfil `demo`

**Orquestração:**
- Modo DEMO: seed executado automaticamente a cada startup via RuntimeManager (`--dataset demo --clear`)
- Modo DEVELOPMENT: seed opcional via CLI manual
- Modo PRODUCTION: seed **nunca** executado automaticamente
- Modo TEST: seed **nunca** executado (fixtures cuidam dos dados)

### 4. Docker Strategy

Três compose files para três cenários, cada um com configurações específicas:

| Comando | Arquivo | Uso | Healthcheck | Resource Limits | Restart |
|---------|---------|-----|-------------|-----------------|---------|
| `docker compose up` | `docker-compose.yml` | Padrão (demo) | Backend + Frontend | Não | Não |
| `docker compose -f docker-compose.dev.yml up` | `docker-compose.dev.yml` | Desenvolvimento | Backend apenas | Não | Não |
| `docker compose -f docker-compose.prod.yml up` | `docker-compose.prod.yml` | Produção | Backend + Frontend | `cpus: "1.0"`, `memory: 512M` | `always` |

**Backend (multi-stage build):**
```dockerfile
FROM python:3.12-slim AS base
# ... setup, deps, user ...
CMD ["sh", "start.sh"]
```
- Imagem base: `python:3.12-slim`
- Usuário não-root (`appuser:1000`)
- Healthcheck: `python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')"`
- CMD: `sh start.sh` (delega ao script mode-aware)

**Frontend (multi-stage build):**
```dockerfile
FROM node:20-alpine AS builder
# ... build ...
FROM nginx:alpine
# ... serve ...
```
- Builder: `node:20-alpine` para compilar o Vite
- Runtime: `nginx:alpine` para servir os arquivos estáticos
- Healthcheck: `wget -q --spider http://localhost/nginx-health`
- Depende do backend (`condition: service_healthy`)

**Volumes e Networks:**
- `plantao360_data` / `plantao360_dev_data` / `plantao360_prod_data` — dados persistentes do SQLite
- Networks bridge isoladas por ambiente

### 5. Validation Strategy

O Plantão 360 emprega validação em **5 camadas** (documentado em `docs/architecture/validation-matrix.md`), cada uma com responsabilidade específica:

| Camada | Responsabilidade | Exemplo |
|--------|-----------------|---------|
| **DB** | Restrições físicas — CHECK, UNIQUE, FK, NOT NULL. Última linha de defesa. | `hour_rate >= 0`, `crm` UNIQUE |
| **ORM** | Mapeamento SQLAlchemy — tipos, nullable, defaults, server_defaults. Espelha o DB. | `nullable=False, String(255)` |
| **Domain** | Regras de negócio — state machines, transições, contratos, value objects. | `can_start_only_scheduled`, `shift_time_range` |
| **Validator** | Validação customizada — regras de negócio acionadas pelo service antes do commit. | `validate_crm_format()`, `validate_hour_rate()` |
| **Schema (Pydantic)** | Validação de input — constraints de campo, tipos, tamanhos. Barreira de entrada. | `Field(..., min_length=1, max_length=255)` |
| **API** | Validação de rota — Query params, dependency injection, exception handlers. | `Query(ge=1, le=100)` |

**Estatísticas atuais (72 regras catalogadas):**
- DB: 14 | ORM: 18 | Domain: 22 | Validator: 16 | Schema: 19 | API: 6
- Duplicadas entre camadas: 10 (4 aceitáveis como defesa em profundidade, 1 com inconsistência, 3 tríplices)
- Regras órfãs: 2 (`validate_code()`, `validate_year_month()` — código não importado)

**Inconsistência registrada (DUP-02):**
- `hour_rate` do Doctor: DB permite `>= 0`, Validator/Schema exigem `> 0`
- Recomendação: alinhar DB para `hour_rate > 0`

**Feature Flags** (`app/core/features.py`):
- Flags controladas por variáveis de ambiente
- DARK_MODE (default: true), NOTIFICATIONS, EXPORT_PDF, ENABLE_JWT, ENABLE_AUDIT_LOG, ENABLE_BI, ENABLE_ANALYTICS, ENABLE_TASY_INTEGRATION, ENABLE_EXPORT_PDF, ENABLE_IMPORT_LEGACY

### 6. Bootstrap Strategy

A inicialização do sistema é orquestrada por três componentes em cadeia:

```
Container Start
    │
    ▼
start.sh (shell script — lê ENVIRONMENT + DEMO_MODE)
    │
    ├─── ENVIRONMENT=test? ──► skip migrations/seed → uvicorn
    │
    ├─── ENVIRONMENT=development?
    │        │
    │        ├─── DEMO_MODE=true? ──► alembic → seed demo → uvicorn --reload
    │        └─── DEMO_MODE=false ──► alembic → uvicorn --reload
    │
    └─── ENVIRONMENT=production? ──► alembic → uvicorn (no reload, resource limits)
```

**Componentes:**

1. **start.sh** (`backend/start.sh`) — Script shell que lê variáveis de ambiente e decide o fluxo. Ponto de entrada do container (CMD).

2. **RuntimeManager** (`app/core/runtime.py`) — Componente Python que orquestra:
   - `detect_mode()` → mapeia `ENVIRONMENT` + `DEMO_MODE` para `RuntimeMode`
   - `run_migrations()` → executa `alembic upgrade head` (ou skip em TEST)
   - `seed_data()` → executa seed apenas em DEMO
   - `initialize_database()` → sequência completa: migrations + seed
   - `get_startup_info()` → retorna resumo da configuração

3. **Lifespan Handler** (`app/core/lifespan.py`) — Handler do FastAPI que integra o RuntimeManager ao ciclo de vida:
   - Startup: executa migrations + seed (conforme modo)
   - Shutdown: log de desligamento
   - Lazy initialization: `RuntimeManager` criado no primeiro startup, não no import

**Fluxo por modo:**
- TEST: Lifespan não executa nada (fixtures cuidam do DB)
- DEMO: migrations → seed demo → API
- DEVELOPMENT: migrations → API
- PRODUCTION: migrations → API

### 7. Quality Gates

O sistema possui **12 Quality Gates** que garantem compliance contínua. São executados pelo `tools/release_readiness.py` e pelo pipeline de CI/CD:

| # | Gate | Ferramenta | Descrição |
|---|------|-----------|-----------|
| 1 | **TypeScript** | `tsc --noEmit` | Validação de tipos do Frontend |
| 2 | **ESLint** | `eslint` | Linting do Frontend |
| 3 | **Vitest** | `vitest run` | Testes unitários do Frontend |
| 4 | **Pytest** | `pytest app/tests/` | Testes unitários e de integração do Backend |
| 5 | **Alembic** | `alembic upgrade head` | Validação de migrações |
| 6 | **Manifest** | `tools/manifest_validator.py` | Validação de manifests dos módulos |
| 7 | **Architecture** | `tools/validate_architecture.py --all` | Validação de capacidades arquiteturais |
| 8 | **Golden Guard** | `tools/golden_guard.py` | Validação de compliance com Golden Module |
| 9 | **Frontend Validator** | `tools/validate_frontend.py` | Validação de estrutura do Frontend |
| 10 | **Docker Build** | `docker build` | Build das imagens Backend + Frontend |
| 11 | **Bootstrap** | `tools/test_bootstrap.py` | Validação do fluxo de inicialização |
| 12 | **Smoke** | `tools/smoke_tests.py` | Testes de fumaça (health, endpoints críticos) |

**Release Readiness** (`tools/release_readiness.py`):
- Executa todos os checks em sequência
- Gera relatório em `docs/reports/release-readiness.md`
- Status final: `READY` ou `BLOCKED`
- Checks incluem: Architecture Validator, Architecture Linter, Golden Guard, Template Consistency, ADR Validator, Compliance Report, Architecture Score, Technical Debt, Dependency Check, Pytest

---

## Consequences

### Positivas

1. **Consistência** — Um único ponto de decisão para inicialização (RuntimeManager)
2. **Segurança** — Produção nunca roda seed automaticamente
3. **Testabilidade** — Modo TEST isola completamente do Alembic e seed
4. **Reprodutibilidade** — Docker compose files específicos por ambiente
5. **Visibilidade** — Matriz de validação com 72 regras catalogadas
6. **Automação** — 12 Quality Gates executados antes de qualquer release
7. **Defesa em profundidade** — 5 camadas de validação com responsabilidades claras
8. **Manutenibilidade** — Schema ownership definido (Alembic), data ownership definido (Seed)

### Negativas

1. **Complexidade** — Mais componentes para manter (RuntimeManager, Lifespan, start.sh)
2. **Overhead de build** — Multi-stage builds adicionam tempo ao pipeline
3. **Curva de aprendizado** — Equipe precisa conhecer os 4 modos de execução
4. **Duplicação intencional** — Regras de validação em múltiplas camadas (10 duplicações documentadas)
5. **Dependência de shell** — `start.sh` requer bash; Windows precisa de WSL/Docker

### Riscos

| Risco | Severidade | Mitigação |
|-------|-----------|-----------|
| `get_settings()` é `@lru_cache` — caching antes de env vars configuradas | Média | `get_settings.cache_clear()` em conftest.py e fixtures |
| `start.sh` depende de shell — Windows users | Baixa | Documentado; desenvolvimento local usa venv |
| Engine singleton mantém conexões abertas em testes | Baixa | `base_mod._engine = None` em fixtures de teste |
| DB permite `hour_rate = 0` mas Validator/Schema não | Baixa | Registrar como tech debt; alinhar em sprint futura |
| Enums sem CHECK constraint no DB | Baixa | Validação via Domain (StrEnum); inserção direta pode inserir valores inválidos |
| Regras órfãs (`validate_code`, `validate_year_month`) | Baixa | Código morto — remover ou integrar em sprint futura |

---

## References

- `backend/app/core/runtime.py` — RuntimeManager (single source of truth para inicialização)
- `backend/app/core/lifespan.py` — FastAPI lifespan handler
- `backend/app/core/features.py` — Feature Flags
- `backend/start.sh` — Startup script mode-aware
- `backend/alembic.ini` — Configuração do Alembic
- `backend/app/seed/__init__.py` — CLI unificada de seed
- `backend/app/seed/profiles/` — Perfis: demo, development, edge_cases, empty
- `backend/Dockerfile` — Multi-stage build do Backend
- `frontend/Dockerfile` — Multi-stage build do Frontend (Node + Nginx)
- `docker-compose.yml` — Compose padrão (demo)
- `docker-compose.dev.yml` — Compose de desenvolvimento
- `docker-compose.prod.yml` — Compose de produção (com resource limits)
- `docs/architecture/validation-matrix.md` — Matriz completa de validação (72 regras)
- `docs/architecture/runtime-modes.md` — Documentação detalhada dos modos
- `tools/validate_architecture.py` — Architecture Validator V2
- `tools/golden_guard.py` — Golden Guard
- `tools/release_readiness.py` — Release Readiness (12 Quality Gates)
- `tools/manifest_validator.py` — Manifest Validator
- `tools/manifest_loader.py` — Manifest Loader
- `docs/adr/ADR-028-frontend-platform-governance.md` — ADR anterior
