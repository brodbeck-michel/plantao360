# Runtime Modes — Plantão 360

**Data:** 2026-06-28
**Sprint:** 14.3 — Production Readiness (ETAPA 3)
**Status:** Aprovado

---

## Visão Geral

O Plantão 360 opera em **quatro modos de execução**, cada um com fluxo de inicialização distinto. A decisão é tomada por um único componente: **`RuntimeManager`** (`app/core/runtime.py`).

```
┌─────────────────────────────────────────────────────────────────┐
│                    RuntimeManager                               │
│                                                                 │
│  ENVIRONMENT=development + DEMO_MODE=true  → DEMO               │
│  ENVIRONMENT=development + DEMO_MODE=false → DEVELOPMENT        │
│  ENVIRONMENT=production                   → PRODUCTION          │
│  ENVIRONMENT=test                         → TEST                │
└─────────────────────────────────────────────────────────────────┘
```

---

## Modos de Execução

### DEMO
- **Uso:** Desenvolvimento com dados fictícios
- **Fluxo:** `alembic upgrade head` → `seed --dataset demo --clear` → API
- **Seed:** Automático (executa a cada startup)
- **Migrations:** Automático
- **Uvicorn:** Com `--reload`

### DEVELOPMENT
- **Uso:** Desenvolvimento sem dados automáticos
- **Fluxo:** `alembic upgrade head` → API
- **Seed:** Manual (via CLI quando necessário)
- **Migrations:** Automático
- **Uvicorn:** Com `--reload`

### PRODUCTION
- **Uso:** Ambiente de produção
- **Fluxo:** `alembic upgrade head` → API
- **Seed:** Nunca automático
- **Migrations:** Automático
- **Uvicorn:** Sem `--reload`, com resource limits

### TEST
- **Uso:** Testes automatizados
- **Fluxo:** `create_all()` via fixtures de teste
- **Seed:** Nunca (fixtures criam dados isolados)
- **Migrations:** Não utilizadas (schema via `Base.metadata.create_all`)
- **Uvicorn:** Sem `--reload`

---

## Diagrama de Inicialização

```
Container Start
    │
    ▼
start.sh
    │
    ├─── ENVIRONMENT=test? ──► skip migrations/seed → uvicorn
    │
    ├─── ENVIRONMENT=development?
    │        │
    │        ├─── DEMO_MODE=true? ──► alembic → seed demo → uvicorn --reload
    │        └─── DEMO_MODE=false ──► alembic → uvicorn --reload
    │
    └─── ENVIRONMENT=production? ──► alembic → uvicorn (no reload)
```

---

## Componentes

### RuntimeManager (`app/core/runtime.py`)

Componente central que orquestra a inicialização.

**Responsabilidades:**
- Detectar o modo de execução a partir de `ENVIRONMENT` + `DEMO_MODE`
- Executar migrations (`alembic upgrade head`)
- Executar seed (apenas em modo DEMO)
- Reportar status da inicialização

**NÃO é responsável por:**
- Lógica de negócio
- Geração de dados (responsabilidade do seed)
- Definição de schema (responsabilidade do Alembic)

### Lifespan Handler (`app/core/lifespan.py`)

Handler do FastAPI que integra o RuntimeManager ao ciclo de vida da aplicação.

**Startup:**
- TEST mode: sem ações (fixtures cuidam do DB)
- DEMO/DEVELOPMENT/PRODUCTION: executa migrations + seed (se DEMO)

**Shutdown:**
- Log de desligamento

### Startup Script (`backend/start.sh`)

Script shell que lê `ENVIRONMENT` e `DEMO_MODE` e executa o fluxo correto.

---

## Arquivos Modificados

| Arquivo | Mudança |
|---------|---------|
| `app/core/runtime.py` | **NOVO** — RuntimeManager |
| `app/core/lifespan.py` | **NOVO** — FastAPI lifespan handler |
| `app/api/app.py` | Adicionado `lifespan=create_lifespan()` |
| `app/seed/seed_data.py` | Removido `Base.metadata.create_all()` |
| `backend/Dockerfile` | CMD → `sh start.sh` |
| `backend/start.sh` | **NOVO** — Script de inicialização mode-aware |
| `docker-compose.dev.yml` | Removido `command` override (usa start.sh) |
| `app/tests/conftest.py` | Adicionado `get_settings.cache_clear()` |
| `app/tests/integration/test_bootstrap.py` | Atualizado para engine reset |

---

## Impacto na Infraestrutura

### Antes (Sprint 14.2)
- Seed executava `create_all()` internamente (bypass Alembic)
- Dockerfile sempre rodava seed demo em TODOS os ambientes
- `DEMO_MODE` definido mas nunca lido pelo código Python
- Sem handler de lifespan no FastAPI
- Dockerfile único com CMD hardcoded

### Depois (Sprint 14.3 ETAPA 3)
- Seed apenas popula dados (schema é responsabilidade do Alembic)
- `start.sh` decide o fluxo baseado em `ENVIRONMENT` + `DEMO_MODE`
- `DEMO_MODE` é lido pelo `RuntimeManager` para decidir DEMO vs DEVELOPMENT
- FastAPI tem lifespan handler que orquestra inicialização
- Produção não roda seed automaticamente

---

## Riscos Remanescentes

| Risco | Severidade | Mitigação |
|-------|-----------|-----------|
| `get_settings()` é `@lru_cache` — se caching occurs before env vars are set, wrong config is used | Média | `get_settings.cache_clear()` em conftest.py e test fixtures |
| `start.sh` depende de shell — windows users precisam de WSL/Docker | Baixa | Documentado; desenvolvimento local usa venv |
| Engine singleton pode manter conexões abertas em testes | Baixa | `base_mod._engine = None` em fixtures de teste |

---

## Melhorias Futuras

1. **CI Pipeline:** Incluir teste de bootstrap na pipeline oficial
2. **Alembic head check:** Validar que migrations estão aplicadas no readiness check
3. **Seed dry-run:** Flag `--dry-run` para validar dados sem escrever no DB

---

**Autor:** Sprint 14.3 ETAPA 3
**Aprovação:** Pendente
