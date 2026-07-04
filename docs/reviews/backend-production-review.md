# Backend Production Review — Plantao 360

**Data da Revisão:** 2026-06-29
**Escopo:** Revisão completa de prontidão do backend para produção
**Stack:** Python 3.12, FastAPI, SQLAlchemy 2.0, Alembic, SQLite (dev) / PostgreSQL (prod)

---

## Visão Geral

O backend do Plantao360 é uma API REST construída com FastAPI e SQLAlchemy, utilizando uma arquitetura em camadas (routes → services/use_cases → repositories → models). O sistema gerencia plantões médicos, escalas, folhas de pagamento e cobertura, com suporte a múltiplos modos de execução (DEMO, DEVELOPMENT, PRODUCTION, TEST).

---

## 1. Settings

### Análise

**BaseAppSettings** (`base.py:4-27`):
- Utiliza `pydantic_settings.BaseSettings` para configuração tipada
- Define campos essenciais: `APP_NAME`, `APP_VERSION`, `ENVIRONMENT`, `DATABASE_URL`, `SECRET_KEY`, `LOG_LEVEL`, `ALLOWED_ORIGINS`
- Feature flags: `ENABLE_JWT`, `ENABLE_AUDIT_LOG`, `ENABLE_BI`, `ENABLE_ANALYTICS`, `ENABLE_TASY_INTEGRATION`, `DEMO_MODE`
- `allowed_origins_list` converte string CSV para lista
- Configuração `case_sensitive = True` para variáveis de ambiente

**Environment-specific** (`development.py`, `production.py`, `test.py`):
- Development: SQLite local, LOG_LEVEL=DEBUG
- Production: PostgreSQL, LOG_LEVEL=WARNING
- Test: SQLite em memória, SECRET_KEY dedicada
- Todos herdam de `BaseAppSettings` e usam `env_file` específico

**Factory** (`factory.py:10-21`):
- `lru_cache` para singleton
- Mapeia `ENVIRONMENT` para classe de settings
- Fallback para `DevelopmentSettings`

### Status: COM RESSALVAS

### Issues

| # | Severidade | Descrição | Arquivo:Linha |
|---|-----------|-----------|---------------|
| 1 | **CRÍTICO** | `SECRET_KEY` em `base.py:9` tem valor placeholder `"change-me-in-production-use-a-real-secret"` — se `ENVIRONMENT=production` e o .env não definir SECRET_KEY, a app inicia com chave previsível | `base.py:9` |
| 2 | **CRÍTICO** | `ProductionSettings` não valida se `SECRET_KEY` foi alterado do padrão — deveria falhar no startup se for o placeholder | `production.py:4-13` |
| 3 | **MÉDIO** | `DATABASE_URL` em `production.py:7` contém credenciais hardcoded (`user:pass`) — embora o `.env` sobrescreva, o valor padrão é inseguro | `production.py:7` |
| 4 | **BAIXO** | Feature flags duplicadas entre `BaseAppSettings` e `FeatureFlags` em `features.py` — duas fontes de verdade para as mesmas flags (ENABLE_JWT, ENABLE_AUDIT_LOG, etc.) | `base.py:13-17`, `features.py:4-15` |
| 5 | **BAIXO** | `DEMO_MODE` não está presente em `ProductionSettings` — se definido via env em produção, será ignorado (herda de Base) | `production.py` |
| 6 | **BAIXO** | `model_config` não define `env_prefix` — todas as variáveis são lidas sem prefixo, potencialmente conflitando com variáveis do sistema | `base.py:24-27` |

---

## 2. RuntimeManager

### Análise

**RuntimeMode** (`runtime.py:29-41`):
- `StrEnum` com 4 modos: TEST, DEMO, DEVELOPMENT, PRODUCTION
- Documentação clara de cada fluxo de inicialização

**detect_mode** (`runtime.py:44-69`):
- Mapeia ENVIRONMENT → RuntimeMode
- DEMO detectado via `DEMO_MODE=true` em ambiente development
- Import circular potencial: `from app.core.config import get_settings` dentro da função

**RuntimeManager** (`runtime.py:72-180`):
- `_detect_backend_dir()` usa `Path(__file__)` — correto
- `run_migrations()` usa `subprocess.run()` com timeout de 120s
- `seed_data()` só executa em modo DEMO
- `initialize_database()` executa migrations + seed sequencialmente
- `get_startup_info()` retorna dict com informações do runtime

**create_runtime** (`runtime.py:183-198`):
- Factory function que lê settings e cria RuntimeManager

### Status: COM RESSALVAS

### Issues

| # | Severidade | Descrição | Arquivo:Linha |
|---|-----------|-----------|---------------|
| 1 | **MÉDIO** | `detect_mode()` importa `get_settings` dentro da função para evitar circular import — mas `create_runtime()` na linha 191 também importa `get_settings`, inconsistência | `runtime.py:63`, `runtime.py:191` |
| 2 | **MÉDIO** | `subprocess.run()` não levanta exceção em falha — retorna `CompletedProcess` com `returncode != 0`, mas o caller precisa checar manualmente | `runtime.py:101-120` |
| 3 | **BAIXO** | `_seed_module = "app.seed.seed_data"` hardcodado — se o módulo mudar de nome, falha silenciosa | `runtime.py:89` |
| 4 | **BAIXO** | `timeout=120` no `subprocess.run` é fixo — migrações complexas podem precisar de mais tempo | `runtime.py:106` |
| 5 | **BAIXO** | `initialize_database()` sempre chama `seed_data(dataset="demo", clear=True)` independentemente do modo — mas `seed_data()` já tem guard clause para DEMO, então é redundante | `runtime.py:166` |
| 6 | **INFO** | `engine` parameter em `initialize_database()` é aceito mas nunca usado — parâmetro morto | `runtime.py:153` |

---

## 3. Lifespan

### Análise

**app_lifespan** (`lifespan.py:19-54`):
- Async context manager que orquestra startup/shutdown
- TEST mode: sem ações (fixtures cuidam do DB)
- Outros modos: roda migrations, depois seed (apenas DEMO)
- Trata falhas de migrations e seed com log de erro, mas não aborta
- Shutdown: apenas log

**create_lifespan** (`lifespan.py:57-80`):
- Factory com lazy initialization do RuntimeManager
- Usa closure para caching do runtime
- Evita import time initialization

### Status: APROVADO

### Issues

| # | Severidade | Descrição | Arquivo:Linha |
|---|-----------|-----------|---------------|
| 1 | **MÉDIO** | Se migrations falham, a app continua rodando (`logger.error` mas `yield` executa) — em produção, deveria falhar o startup | `lifespan.py:39-40` |
| 2 | **BAIXO** | Shutdown não resources cleanup (ex: pool de conexões) — depende do GC | `lifespan.py:53-54` |
| 3 | **INFO** | `create_lifespan` aceita `environment` parameter mas não é usado no padrão (sempre None) | `lifespan.py:57` |

---

## 4. Dependency Injection

### Análise

**API Dependencies** (`dependencies.py:1-22`):
- `get_database()`: wrapper sobre `get_db()` — injeta Session
- `get_config()`: retorna settings
- `get_flags()`: retorna feature flags
- `get_current_user`: importado mas não usado em rotas atuais

**Security Dependencies** (`security/dependencies.py:1-35`):
- `get_current_user()`: stub — retorna `request.state.user` ou None
- `require_role()`: stub — retorna None
- `require_permission()`: stub — retorna None
- Todos marcados com TODO para implementação futura

**Session Injection** (`database/session.py:7-12`):
- `get_db()` é generator que cria e fecha sessão
- Usa `SessionLocal()` diretamente

### Status: COM RESSALVAS

### Issues

| # | Severidade | Descrição | Arquivo:Linha |
|---|-----------|-----------|---------------|
| 1 | **CRÍTICO** | **Todas as rotas CRUD estão completamente abertas** — sem autenticação, sem autorização. Qualquer pessoa pode criar/editar/deletar médicos, plantões, folhas de pagamento | `dependencies.py`, rotas |
| 2 | **MÉDIO** | `get_current_user` retorna None — não há validação de token JWT | `security/dependencies.py:16-21` |
| 3 | **MÉDIO** | `require_role` e `require_permission` são pass — não fazem nada | `security/dependencies.py:25-35` |
| 4 | **MÉDIO** | `dependencies.py:7` importa `get_current_user` mas não é usado em nenhuma rota | `dependencies.py:7` |
| 5 | **BAIXO** | `get_database()` é wrapper desnecessário sobre `get_db()` — poderia usar `get_db` diretamente | `dependencies.py:10-12` |
| 6 | **BAIXO** | Não há rate limiting configurado | N/A |

---

## 5. Logging

### Análise

**JSONFormatter** (`logging.py:10-41`):
- Formata logs em JSON estruturado
- Inclui: event, level, logger, message, timestamp (UTC), request_id, correlation_id
- Extras opcionais: method, path, status, duration_ms
- Trata exceções com `formatException`

**setup_logging** (`logging.py:44-53`):
- Configura root logger
- Remove handlers existentes (avoid duplicate)
- Cria StreamHandler para stdout
- Usa JSONFormatter

**Context** (`common/context.py`):
- ContextVars para request_id e correlation_id
- Thread-safe e async-safe

### Status: APROVADO

### Issues

| # | Severidade | Descrição | Arquivo:Linha |
|---|-----------|-----------|---------------|
| 1 | **MÉDIO** | Não há handler de arquivo — logs só vão para stdout. Em produção com containers, stdout é aceitável, mas não há rotação de logs | `logging.py:51` |
| 2 | **BAIXO** | `logging.py:33-36` — `request_id` e `correlation_id` são sobrescritos dos ContextVars e do `record` — redundante | `logging.py:33-36` |
| 3 | **BAIXO** | Não há configuração de log level por módulo — tudo usa o mesmo level | `logging.py:46` |
| 4 | **INFO** | Audit log (`ENABLE_AUDIT_LOG`) não está integrado ao sistema de logging | `logging.py` |

---

## 6. Health Endpoint

### Análise

**Implementação** (`health.py:15-36`):
- Endpoint `GET /api/v1/health`
- Verifica database: `SELECT 1` + `commit()`
- Retorna JSON com: status, version, environment, database, timestamp
- Status code: 200 (ok) ou 503 (error)

### Status: COM RESSALVAS

### Issues

| # | Severidade | Descrição | Arquivo:Linha |
|---|-----------|-----------|---------------|
| 1 | **MÉDIO** | `db.commit()` no health check (`health.py:22`) — health check deveria ser read-only, não deveria commitar | `health.py:22` |
| 2 | **BAIXO** | `settings = get_settings()` executado no module level (`health.py:12`) — settings são carregados no import, antes do startup | `health.py:12` |
| 3 | **BAIXO** | Não verifica memória, disco, ou CPU — apenas database | `health.py` |
| 4 | **INFO** | Resposta não segue padrão Kubernetes liveness probe (apenas `{"status": "ok"}` seria suficiente) | `health.py:28-34` |

---

## 7. Readiness Endpoint

### Análise

**Implementação** (`readiness.py:16-61`):
- Endpoint `GET /api/v1/readiness`
- 4 checks: database, settings, storage, migrations
- Database: `SELECT 1` + `commit()`
- Settings: verifica se DATABASE_URL, SECRET_KEY, APP_NAME existem
- Storage: cria diretórios `data/` e `data/backups/` se não existirem
- Migrations: verifica se `Base.metadata` existe
- Retorna `ready: bool` + `checks: dict` + `timestamp`

### Status: COM RESSALVAS

### Issues

| # | Severidade | Descrição | Arquivo:Linha |
|---|-----------|-----------|---------------|
| 1 | **MÉDIO** | `db.commit()` no readiness check (`readiness.py:28`) — deveria ser read-only | `readiness.py:28` |
| 2 | **MÉDIO** | `os.makedirs()` no readiness check (`readiness.py:43-44`) — endpoint de verificação não deveria ter efeitos colaterais (criar diretórios) | `readiness.py:43-44` |
| 3 | **MÉDIO** | Check de migrations (`readiness.py:49-53`) apenas verifica se `Base.metadata` existe — não verifica se as migrations foram aplicadas | `readiness.py:49-53` |
| 4 | **BAIXO** | `settings = get_settings()` no module level — mesmo problema do health | `readiness.py:13` |
| 5 | **BAIXO** | Check de settings é trivial — apenas verifica se atributos existem, não se são válidos | `readiness.py:32-37` |

---

## 8. Database

### Análise

**Engine Configuration** (`base.py:11-23`):
- Lazy initialization com proxy pattern (`_EngineProxy`, `_SessionLocalProxy`)
- `pool_pre_ping=True` — verifica conexões antes de usar
- SQLite: `check_same_thread=False`
- Não configura `pool_size`, `max_overflow`, `pool_timeout` para PostgreSQL

**Session Management** (`session.py:7-12`):
- `get_db()` é generator FastAPI dependency
- Cria sessão, yield, fecha no finally

**Unit of Work** (`unit_of_work.py:8-40`):
- Pattern clássico com `__enter__`/`__exit__`
- Auto-commit em sucesso, auto-rollback em exceção
- Utilizado nas rotas via `uow._session = db` (injeção manual)

### Status: COM RESSALVAS

### Issues

| # | Severidade | Descrição | Arquivo:Linha |
|---|-----------|-----------|---------------|
| 1 | **CRÍTICO** | **Não há connection pooling configurado para PostgreSQL** — `create_engine` usa defaults (pool_size=5, max_overflow=10). Em produção com múltiplos workers, pode esgotar conexões | `base.py:18-22` |
| 2 | **MÉDIO** | `_EngineProxy` e `_SessionLocalProxy` são patterns não-idiomáticos — poderiam ser simplesmente `lazy` properties ou functions | `base.py:37-48` |
| 3 | **MÉDIO** | `uow._session = db` nas rotas (`doctors.py:38` etc.) — acessa atributo privado, quebra encapsulamento do UnitOfWork | `doctors.py:38`, etc. |
| 4 | **MÉDIO** | `db.commit()` é chamado nas rotas diretamente (`doctors.py:81`), não pelo UnitOfWork — padrão inconsistente com o UoW pattern | `doctors.py:81`, etc. |
| 5 | **BAIXO** | `pool_pre_ping=True` é bom, mas não há métricas de pool (conexões ativas, timeout, etc.) | `base.py:21` |
| 6 | **BAIXO** | `autocommit=False, autoflush=False` no sessionmaker — correto, mas não documentado por quê | `base.py:29` |

---

## 9. Middleware

### Análise

**AccessLogMiddleware** (`access_log.py:13-36`):
- Registra cada request com method, path, status, duration_ms
- Inclui request_id e correlation_id
- Usa JSON structured logging

**CorrelationIDMiddleware** (`correlation.py:11-38`):
- Gera ou lê X-Request-ID do header
- Propaga via ContextVars e request.state
- Retorna headers na response

**CORS** (`app.py:26-32`):
- Configuração via `ALLOWED_ORIGINS`
- `allow_credentials=True`, `allow_methods=["*"]`, `allow_headers=["*"]`

**Exception Handlers** (`exception_handlers.py:12-66`):
- Handlers para: BusinessRuleError, NotFoundError, ConflictError, UnauthorizedError
- Handler genérico para Exception (500)
- Resposta padronizada com status, detail, type

### Status: APROVADO

### Issues

| # | Severidade | Descrição | Arquivo:Linha |
|---|-----------|-----------|---------------|
| 1 | **MÉDIO** | CORS `allow_methods=["*"]` e `allow_headers=["*"]` — deveria ser restritivo em produção | `app.py:30-31` |
| 2 | **BAIXO** | `CorrelationIDMiddleware` e `AccessLogMiddleware` ambos registram log de request — log duplicado para cada request | `correlation.py:26-36`, `access_log.py:23-34` |
| 3 | **BAIXO** | `exception_handlers.py:57-66` — handler genérico não loga a exceção, apenas retorna 500 | `exception_handlers.py:57-66` |
| 4 | **BAIXO** | Não há middleware de rate limiting | N/A |
| 5 | **INFO** | Não há middleware de compressão (gzip) | N/A |

---

## 10. Alembic

### Análise

**Configuration** (`alembic.ini`):
- `script_location = alembic`
- `sqlalchemy.url` hardcoded como SQLite (sobrescrita por `env.py`)
- Logging configurado para root, sqlalchemy, alembic

**env.py** (`alembic/env.py:1-57`):
- Sobrescreve `sqlalchemy.url` com `settings.DATABASE_URL`
- Importa modelos explicitamente para registrar com `Base.metadata`
- Suporta offline e online migrations
- Usa `NullPool` para migrações

**Migrations** (4 arquivos):
- `001_init`: Schema inicial (doctors, periods, shifts, shift_parts, shift_extras)
- `002_add_shift_extra_duration`: Adiciona duration_minutes
- `sprint9_payroll`: Tabela payrolls (com bug de colunas duplicadas)
- `003_runtime_alignment`: Corrige constraints e remove colunas duplicadas

### Status: COM RESSALVAS

### Issues

| # | Severidade | Descrição | Arquivo:Linha |
|---|-----------|-----------|---------------|
| 1 | **MÉDIO** | `alembic.ini:4` — `sqlalchemy.url = sqlite:///./plantao360.db` é hardcoded mas sobrescrito por `env.py` — configuração confusa | `alembic.ini:4` |
| 2 | **MÉDIO** | `003_runtime_alignment` usa `op.drop_table("payrolls")` + `op.create_table()` — destructive migration, sem backup dos dados | `003_runtime_alignment.py:41-74` |
| 3 | **BAIXO** | `downgrade()` do `003_runtime_alignment` restaura schema com colunas duplicadas (`created_at_ts`, `updated_at_ts`) — inconsistente | `003_runtime_alignment.py:77-117` |
| 4 | **BAIXO** | Não há `downgrade()` no `001_init` (sim, existe na linha 223, está correto) — OK | `001_init.py:223-228` |
| 5 | **BAIXO** | Nomeclatura de revision IDs inconsistente: `001_init`, `002_...`, `sprint9_...`, `003_...` | Vários |
| 6 | **INFO** | `env.py:11` importa modelos explicitamente — se esquecer de importar um modelo, a migration não o detecta | `env.py:11` |

---

## Resumo

| Área | Status | Issues Críticos | Issues Médios | Issues Baixos |
|------|--------|----------------|---------------|---------------|
| 1. Settings | COM RESSALVAS | 2 | 1 | 3 |
| 2. RuntimeManager | COM RESSALVAS | 0 | 2 | 4 |
| 3. Lifespan | APROVADO | 0 | 1 | 2 |
| 4. Dependency Injection | COM RESSALVAS | 1 | 3 | 2 |
| 5. Logging | APROVADO | 0 | 1 | 2 |
| 6. Health Endpoint | COM RESSALVAS | 0 | 1 | 3 |
| 7. Readiness Endpoint | COM RESSALVAS | 0 | 3 | 2 |
| 8. Database | COM RESSALVAS | 1 | 3 | 2 |
| 9. Middleware | APROVADO | 0 | 1 | 3 |
| 10. Alembic | COM RESSALVAS | 0 | 2 | 3 |

---

## Pendências Críticas (devem ser resolvidas ANTES de produção)

| # | Issue | Impacto | Esforço |
|---|-------|---------|---------|
| **P1** | **SECRET_KEY hardcoded** — Se production não definir SECRET_KEY no .env, a app inicia com chave previsível. Qualquer JWT (futuro) seria forjável. | Segurança total comprometida | Baixo |
| **P2** | **Rotas sem autenticação** — Todas as rotas CRUD (doctors, periods, shifts, assignments, extras, payrolls) estão completamente abertas. Qualquer pessoa pode acessar. | Acesso não autorizado a dados sensíveis | Alto |
| **P3** | **Connection pooling não configurado** — PostgreSQL production usa defaults do SQLAlchemy (pool_size=5, max_overflow=10). Com múltiplos workers Uvicorn, conexões serão insuficientes. | Erros de conexão sob carga | Baixo |
| **P4** | **Health/Readiness fazem commit** — Endpoints de verificação executam `db.commit()`, podendo causar efeitos colaterais em transações paralelas. | Comportamento inesperado | Baixo |
| **P5** | **Readiness cria diretórios** — Endpoint de verificação cria `data/` e `data/backups/` no filesystem. Em containers read-only, isto falha. | Falha em ambientes containerizados | Baixo |
| **P6** | **Lifespan não aborta em falha de migration** — Se migrations falham, a app continua rodando sem banco funcional. | API返回500 para todas as requisições | Baixo |

## Pendências Médias (devem ser resolvidas antes de produção)

| # | Issue | Impacto |
|---|-------|---------|
| M1 | CORS muito permissivo (`allow_methods=["*"]`, `allow_headers=["*"]`) | Segurança |
| M2 | Feature flags duplicadas (BaseAppSettings + FeatureFlags) | Manutenção |
| M3 | `db.commit()` nas rotas ao invés do UnitOfWork | Consistência |
| M4 | `uow._session = db` acessa atributo privado | Design |
| M5 | Log duplicado (CorrelationID + AccessLog) | Performance |
| M6 | Handler genérico de exceção não loga erros | Observabilidade |
| M7 | Alembic migration destructiva sem backup | Dados |

## Pendências Baixas (melhorias futuras)

| # | Issue |
|---|-------|
| B1 | Adicionar rate limiting |
| B2 | Adicionar middleware de compressão |
| B3 | Configurar log rotation / file handler |
| B4 | Adicionar métricas de connection pool |
| B5 | Adicionar health checks de memória/disco |
| B6 | padronizar nomes de alembic revisions |
| B7 | Remover `_EngineProxy`/`_SessionLocalProxy` em favor de pattern mais idiomático |
| B8 | Documentar por que `autocommit=False, autoflush=False` |
| B9 | Integrar audit logging com ENABLE_AUDIT_LOG |
| B10 | Configurar `pool_size` e `max_overflow` para PostgreSQL |

---

## Conclusão

O backend do Plantao360 possui uma **arquitetura sólida** com separação clara de responsabilidades, logging estruturado, middleware de correlação, e padrões de design (Unit of Work, Use Cases). A documentação das rotas está excelenta com descrições detalhadas no OpenAPI.

No entanto, **não está pronto para produção** devido a:
1. Falta total de autenticação/autorização
2. SECRET_KEY hardcoded
3. Connection pooling não configurado
4. Endpoints de health com efeitos colaterais

**Recomendação:** Resolver P1-P6 antes de qualquer deploy em produção. Os itens M1-M7 podem ser resolvidos em sprint dedicado de hardening.
