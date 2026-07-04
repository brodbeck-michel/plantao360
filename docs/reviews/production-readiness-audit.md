# Production Readiness Audit — Sprint 14.3 ETAPA 0

**Data:** 2026-06-27
**Escopo:** Auditoria técnica completa do sistema Plantão 360
**Objetivo:** Transformar demo funcional em arquitetura production-ready com zero workarounds

---

## Resumo Executivo

| Métrica | Valor |
|---------|-------|
| Problemas encontrados | 23 |
| Críticos | 5 |
| Alto | 8 |
| Médio | 7 |
| Baixo | 3 |
| Arquivos afetados | ~15 |
| Etapas necessárias | 14 |

---

## Regras de Execução (aprovadas em 2026-06-27)

### Regra 1 — Nenhuma correção arquitetural automática

Itens que exigem proposta técnica antes da implementação:
- **P05** — Remoção do `Base.metadata.create_all()`
- **P08** — Restauração das CheckConstraints

Para cada um: motivo da solução atual, impacto da alteração, estratégia definitiva, risco de regressão, plano de rollback.

### Regra 2 — Classificação por tipo de problema

Cada problema é classificado em uma das categorias:
- **Correção de bug** — Erro funcional que produz comportamento incorreto
- **Correção de infraestrutura** — Configuração, build, deploy, Docker
- **Dívida técnica** — Solução temporária que precisa ser substituída
- **Evolução arquitetural** — Mudança estrutural que altera como o sistema opera
- **Decisão de negócio** — Requer definição de regra ou política

---

## Problemas Encontrados

### P01 — Build script do frontend sem type-checking

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `frontend/package.json:8` |
| **Severidade** | **CRÍTICO** |
| **Tipo** | **Correção de infraestrutura** |
| **Causa raiz** | `tsc -b` foi removido do build script porque o projeto tinha erros TS |
| **Impacto técnico** | TypeScript erros passam silenciosamente; builds de produção podem conter bugs de tipo que só aparecem em runtime |
| **Estratégia** | Corrigir TODOS os erros TypeScript do frontend, restaurar `tsc -b` no build script |
| **Risco** | Alto — pode haver dezenas de erros TS espalhados no código |
| **Ordem** | ETAPA 1 |

---

### P02 — `skipLibCheck: true` no tsconfig.json

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `frontend/tsconfig.json:9` |
| **Severidade** | **CRÍTICO** |
| **Tipo** | **Correção de infraestrutura** |
| **Causa raiz** | Usado para esconder erros de tipagem em dependências ou código próprio |
| **Impacto técnico** | Erros em `.d.ts` ou bibliotecas são ignorados; problemas de compatibilidade de tipos passam despercebidos |
| **Estratégia** | Remover `skipLibCheck: true`, corrigir erros resultantes |
| **Risco** | Médio — pode revelar erros em dependências externas |
| **Ordem** | ETAPA 1 |

---

### P03 — `sourcemap: true` em produção

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `frontend/vite.config.ts:19` |
| **Severidade** | **ALTO** |
| **Tipo** | **Correção de infraestrutura** |
| **Causa raiz** | Configuração deixada do desenvolvimento |
| **Impacto técnico** | Expõe código-fonte completo em produção; risco de segurança (engenharia reversa) |
| **Estratégia** | Condicionar sourcemap ao modo: `sourcemap: mode === 'development'` ou usar variável de ambiente |
| **Risco** | Baixo — mudança isolada |
| **Ordem** | ETAPA 7 |

---

### P04 — `process.env.VITE_API_URL` em vez de `import.meta.env`

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `frontend/vite.config.ts:4` |
| **Severidade** | **MÉDIO** |
| **Tipo** | **Dívida técnica** |
| **Causa raiz** | `process.env` funciona em Vite para arquivos de config, mas é inconsistente com o resto do frontend que usa `import.meta.env` |
| **Impacto técnico** | Inconsistência; em ambientes que não processam `process.env` (SSG, testes), a variável pode não estar disponível |
| **Estratégia** | Usar `import.meta.env.VITE_API_URL` ou `loadEnv()` do Vite |
| **Risco** | Baixo |
| **Ordem** | ETAPA 7 |

---

### P05 — Dockerfile backend usa `Base.metadata.create_all()` como CMD

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `backend/Dockerfile:26` |
| **Severidade** | **CRÍTICO** |
| **Tipo** | **Evolução arquitetural** (requer proposta técnica — Regra 1) |
| **Causa raiz** | Alembic migrations estavam quebradas; `create_all()` foi usado como workaround |
| **Impacto técnico** | Criação de tabelas sem migrations = sem versionamento de schema; dados podem ser perdidos em updates; não suporta ALTER TABLE, ADD COLUMN, etc. |
| **Estratégia** | Restaurar `alembic upgrade head` como CMD; corrigir todas as migrations |
| **Risco** | Alto — migrations precisam ser 100% funcionais |
| **Ordem** | ETAPA 2 |

---

### P06 — Migrations incompletas vs modelos ORM

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `backend/alembic/versions/20260624_init_database.py` |
| **Severidade** | **ALTO** |
| **Tipo** | **Correção de bug** |
| **Causa raiz** | Colunas foram adicionadas aos modelos mas não às migrations |
| **Colunas faltantes** | `shifts.status`, `shifts.scheduled_start/end`, `shifts.actual_start/end`, `shifts.total_duration_minutes`, `shifts.doctor_count`; `shift_parts.status`, `shift_parts.duration_minutes`; `shift_extras.status`, `shift_extras.duration_minutes` |
| **Impacto técnico** | Alembic cria tabelas incompletas; `create_all()` funciona (cria colunas extras) mas Alembic não |
| **Estratégia** | Unificar: migrations devem criar TODAS as colunas dos modelos; criar migration de fix para colunas faltantes |
| **Risco** | Médio — precisa sincronizar modelos ↔ migrations ↔ seed |
| **Ordem** | ETAPA 2 |

---

### P07 — CheckConstraint removida do migration mas presente no modelo

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `backend/app/models/shift_extra.py:18-20` vs `backend/alembic/versions/20260624_002_add_shift_extra_duration.py` |
| **Severidade** | **ALTO** |
| **Tipo** | **Correção de bug** |
| **Causa raiz** | `create_check_constraint` foi removido do migration por incompatibilidade com SQLite |
| **Impacto técnico** | Modelo define `CheckConstraint("duration_minutes > 0")` mas migration não a cria; divergência schema ↔ model |
| **Estratégia** | Usar `op.execute()` com SQL direto para SQLite, ou remover constraint do modelo e validar em application-level |
| **Risco** | Médio — SQLite não suporta `ALTER TABLE ADD CONSTRAINT`; precisa de workaround adequado |
| **Ordem** | ETAPA 4 |

---

### P08 — CheckConstraint `start_time < end_time` removida do modelo

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `backend/app/models/shift_part.py` (removida) vs `backend/alembic/versions/20260624_init_database.py:170-172` (presente na migration) |
| **Severidade** | **ALTO** |
| **Tipo** | **Evolução arquitetural** (requer proposta técnica — Regra 1) |
| **Causa raiz** | CheckConstraint não funciona para turns noturnos (T2: 19:00→07:00); start > end |
| **Impacto técnico** | Migration cria constraint que o modelo não tem; dados inválidos podem ser inseridos |
| **Estratégia** | Substituir por validação baseada em `duration_minutes` (que é calculado corretamente pelo seed) |
| **Risco** | Médio — precisa de lógica para overnight shifts |
| **Ordem** | ETAPA 4 |

---

### P09 — Seed script duplica `Base.metadata.create_all()`

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `backend/app/seed/seed_data.py:387` |
| **Severidade** | **MÉDIO** |
| **Tipo** | **Dívida técnica** |
| **Causa raiz** | Seed chama `create_all()` internamente; Dockerfile também chama |
| **Impacto técnico** | Tabelas são criadas duas vezes; em produção com Alembic, o `create_all()` do seed pode criar tabelas fora de ordem |
| **Estratégia** | Remover `create_all()` do seed; assumir que tabelas já existem (via Alembic ou Dockerfile) |
| **Risco** | Baixo |
| **Ordem** | ETAPA 5 |

---

### P10 — Seed T3 usa workaround `time(7,0)==time(7,0)`

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `backend/app/seed/seed_data.py:313-314` |
| **Severidade** | **MÉDIO** |
| **Tipo** | **Dívida técnica** |
| **Causa raiz** | T3 shift tem start==end (24h); CheckConstraint exige start < end |
| **Impacto técnico** | `end_t = time(23, 59)` é semanticamente incorreto; deveria ser `time(7, 0)` do dia seguinte |
| **Estratégia** | Após ETAPA 4 (remover CheckConstraint inadequada), restaurar `end=time(7,0)` e usar `duration_minutes` para validação |
| **Risco** | Baixo |
| **Ordem** | ETAPA 5 |

---

### P11 — Seed dedup via `seen_keys` set

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `backend/app/seed/seed_data.py:287-295` |
| **Severidade** | **BAIXO** |
| **Tipo** | **Dívida técnica** |
| **Causa raiz** | UniqueConstraint `(shift_date, shift_type)` causa erro em inserts duplicados |
| **Impacto técnico** | Funcional mas frágil; depende de ordenação do seed |
| **Estratégia** | Usar `INSERT OR IGNORE` ou `ON CONFLICT DO NOTHING` do SQLAlchemy |
| **Risco** | Baixo |
| **Ordem** | ETAPA 5 |

---

### P12 — `docker-compose.dev.yml` usa `sh -c "alembic upgrade head && ..."`

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `docker-compose.dev.yml:16-19` |
| **Severidade** | **ALTO** |
| **Tipo** | **Correção de infraestrutura** |
| **Causa raiz** | Assume que Alembic funciona; migrations ainda estão quebradas |
| **Impacto técnico** | Comando falha se migrations não estão corretas; bind mount `./backend:/app` pode causar conflitos |
| **Estratégia** | Corrigir migrations primeiro (ETAPA 2), depois validar compose dev |
| **Risco** | Médio |
| **Ordem** | ETAPA 6 |

---

### P13 — `docker-compose.dev.yml` usa `app.api.app:app` (wrong path)

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `docker-compose.dev.yml:19` |
| **Severidade** | **MÉDIO** |
| **Tipo** | **Correção de bug** |
| **Causa raiz** | Path incorreto: `app.api.app:app` em vez de `app.main:app` |
| **Impacto técnico** | Container não inicia; erro de import |
| **Estratégia** | Corrigir para `app.main:app` |
| **Risco** | Baixo |
| **Ordem** | ETAPA 6 |

---

### P14 — `docker-compose.prod.yml` healthcheck usa `localhost` (IPv6)

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `docker-compose.prod.yml:42` |
| **Severidade** | **MÉDIO** |
| **Tipo** | **Correção de infraestrutura** |
| **Causa raiz** | `wget --spider http://localhost/nginx-health` pode resolver para IPv6 |
| **Impacto técnico** | Healthcheck pode falhar em ambientes onde IPv6 não está disponível |
| **Estratégia** | Usar `127.0.0.1` em vez de `localhost` (já corrigido em `docker-compose.yml`) |
| **Risco** | Baixo |
| **Ordem** | ETAPA 6 |

---

### P15 — Dockerfile frontend copia `frontend/` com paths relativos

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `frontend/Dockerfile:5-8` |
| **Severidade** | **MÉDIO** |
| **Tipo** | **Correção de infraestrutura** |
| **Causa raiz** | `COPY frontend/package.json ./` e `COPY frontend/ .` — funciona quando context é `.` (docker-compose.yml) mas não quando context é `./backend` |
| **Impacto técnico** | Funciona corretamente no compose atual (context `.`); não há problema imediato |
| **Estratégia** | Verificar se o context está correto em todos os compose files |
| **Risco** | Baixo |
| **Ordem** | ETAPA 6 |

---

### P16 — Falta `docker-compose.prod.yml` com volume para banco de dados

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `docker-compose.prod.yml` |
| **Severidade** | **ALTO** |
| **Tipo** | **Evolução arquitetural** |
| **Causa raiz** | Produção usa volume named `plantao360_prod_data` mas o Dockerfile CMD usa `create_all()` — dados são recriados a cada restart |
| **Impacto técnico** | Dados do banco são perdidos a cada `docker compose down && up` a menos que o volume persista; mas `create_all()` + seed com `--clear` apaga tudo |
| **Estratégia** | Para produção: remover seed do CMD; usar apenas `alembic upgrade head`; para dev/demo: manter seed |
| **Risco** | Alto — mudança crítica de comportamento |
| **Ordem** | ETAPA 6 |

---

### P17 — Falta `.env.production` com configurações adequadas

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `.env.production` |
| **Severidade** | **BAIXO** |
| **Tipo** | **Correção de infraestrutura** |
| **Causa raiz** | `.env.production` existe mas pode não ter todas as configs necessárias para produção |
| **Impacto técnico** | Pode faltar `DEMO_MODE=false`, `SECRET_KEY`, `DATABASE_URL` adequado |
| **Estratégia** | Revisar `.env.production` e garantir que todas as configs de produção estão definidas |
| **Risco** | Baixo |
| **Ordem** | ETAPA 3 |

---

### P18 — Falta `docs/architecture/runtime-modes.md`

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `docs/architecture/` |
| **Severidade** | **MÉDIO** |
| **Tipo** | **Correção de infraestrutura** |
| **Causa raiz** | Não existe documentação formal dos modos DEMO/DEV/PROD |
| **Impacto técnico** | Equipe não sabe como configurar cada modo; risco de usar config errada |
| **Estratégia** | Criar documento definindo cada modo, variáveis necessárias, comportamento esperado |
| **Risco** | Baixo |
| **Ordem** | ETAPA 3 |

---

### P19 — `app/database/base.py` usa proxy pattern para engine

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `backend/app/database/base.py:37-48` |
| **Severidade** | **BAIXO** |
| **Tipo** | **Dívida técnica** |
| **Causa raiz** | `_EngineProxy` e `_SessionLocalProxy` são patterns não-convencionais |
| **Impacto técnico** | Funcional mas pode confundir desenvolvedores; tipagem pobre (`__getattr__` dinâmico) |
| **Estratégia** | Manter por enquanto — não é bloqueante para produção; documentar |
| **Risco** | Baixo |
| **Ordem** | Não aplicável (documentação) |

---

### P20 — `alembic/versions/sprint9_add_payroll.py` tem colunas duplicadas

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `backend/alembic/versions/sprint9_add_payroll.py:28-33` |
| **Severidade** | **ALTO** |
| **Tipo** | **Correção de bug** |
| **Causa raiz** | Migration cria `created_at` e `updated_at` E `created_at_ts` e `updated_at_ts` — duplicatas |
| **Impacto técnico** | Tabela payrolls tem 4 colunas de timestamp em vez de 2; conflito com modelo ORM |
| **Estratégia** | Remover `created_at_ts` e `updated_at_ts` da migration |
| **Risco** | Médio — precisa verificar se existem dados com essas colunas |
| **Ordem** | ETAPA 2 |

---

### P21 — Payroll model `created_at`/`updated_at` são `DateTime` sem timezone

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `backend/app/models/payroll.py:38-39` |
| **Severidade** | **MÉDIO** |
| **Tipo** | **Dívida técnica** |
| **Causa raiz** | Todos os outros modelos usam `DateTime(timezone=True)` via `TimestampMixin`; Payroll não usa mixin |
| **Impacto técnico** | Inconsistência; problemas de timezone em produção |
| **Estratégia** | Fazer Payroll usar `TimestampMixin` como os outros modelos; ajustar migration |
| **Risco** | Médio |
| **Ordem** | ETAPA 2 |

---

### P22 — `docker-compose.dev.yml` não tem healthcheck para frontend

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `docker-compose.dev.yml` |
| **Severidade** | **BAIXO** |
| **Tipo** | **Correção de infraestrutura** |
| **Causa raiz** | Frontend dev usa `node:20-alpine` com `npm run dev` — sem healthcheck definido |
| **Impacto técnico** | `depends_on` não pode usar `condition: service_healthy` para frontend |
| **Estratégia** | Adicionar healthcheck para frontend dev ou usar `condition: service_started` |
| **Risco** | Baixo |
| **Ordem** | ETAPA 6 |

---

### P23 — Backend `app/api/health.py` endpoint de healthcheck

| Campo | Detalhe |
|-------|---------|
| **Arquivo** | `backend/app/api/health.py` |
| **Severidade** | **MÉDIO** |
| **Tipo** | **Correção de infraestrutura** |
| **Causa raiz** | Healthcheck atual pode não verificar conectividade com banco de dados |
| **Impacto técnico** | Container reporta "healthy" mesmo com banco indisponível |
| **Estratégia** | Adicionar verificação de DB connection no healthcheck |
| **Risco** | Baixo |
| **Ordem** | ETAPA 8 |

---

## Ordem Recomendada de Implementação

| ETAPA | Problemas | Prioridade | Dependências | Status |
|-------|-----------|------------|--------------|--------|
| **ETAPA 0** | Auditoria (este documento) | Alta | Nenhuma | ✅ Completo |
| **ETAPA 1** | P01, P02 | Crítica | Nenhuma | ✅ Completo |
| **ETAPA 2** | P05, P06, P07, P20, P21 | Crítica | Nenhuma | ✅ Completo |
| **ETAPA 3** | P17, P18 | Alta | ETAPA 2 | ✅ Completo |
| **ETAPA 4** | P07, P08 | Alta | ETAPA 2 | Pendente |
| **ETAPA 5** | P09, P10, P11 | Média | ETAPA 4 | Pendente |
| **ETAPA 6** | P12, P13, P14, P15, P16, P22 | Alta | ETAPA 2 | Pendente |
| **ETAPA 7** | P03, P04 | Média | ETAPA 1 | Pendente |
| **ETAPA 8** | P23 | Média | ETAPA 2 | Pendente |
| **ETAPA 9** | Quality Gates | Média | ETAPA 1, 2 | Pendente |
| **ETAPA 10** | Smoke Tests | Média | ETAPA 6 | Pendente |
| **ETAPA 11** | Tech Debt Report | Baixa | Todas | Pendente |
| **ETAPA 12** | ADR-029 | Baixa | ETAPA 11 | Pendente |
| **ETAPA 13** | Testes | Média | ETAPA 1, 2 | Pendente |
| **ETAPA 14** | Aceite Final | Alta | Todas | Pendente |

---

## Mapa de Impacto

```
ETAPA 1 (TypeScript) ──────────► ETAPA 7 (Frontend Review)
                                  ETAPA 9 (Quality Gates)
                                  ETAPA 13 (Testes)

ETAPA 2 (Alembic) ─────────────► ETAPA 3 (Runtime Modes)
                                  ETAPA 4 (Constraints)
                                  ETAPA 6 (Docker)
                                  ETAPA 8 (Backend Review)
                                  ETAPA 10 (Smoke Tests)

ETAPA 4 (Constraints) ─────────► ETAPA 5 (Seed)

ETAPA 6 (Docker) ──────────────► ETAPA 10 (Smoke Tests)

Todas ─────────────────────────► ETAPA 14 (Aceite Final)
```

---

## Decisões Arquiteturais Pendentes

1. **SQLite vs PostgreSQL**: Sistema atual usa SQLite; para produção real, deve migrar para PostgreSQL? (Recomendado: manter SQLite para demo/dev, suportar PostgreSQL via env var)

2. **Seed strategy**: Para produção, seed deve ser executado manualmente ou automaticamente? (Recomendado: automático em DEMO_MODE, manual em PROD)

3. **Sourcemap em produção**: Desabilitar completamente ou manter para debugging? (Recomendado: desabilitar em PROD, manter em DEV)

4. **Healthcheck com DB**: Verificar apenas HTTP ou também conectividade com banco? (Recomendado: verificar ambos)

---

**Próximo passo:** ETAPA 4 (Constraints) — restaurar CheckConstraints com implementações corretas.
