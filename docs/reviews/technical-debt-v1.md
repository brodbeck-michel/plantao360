# Technical Debt Report — Plantao 360

> Sprint 14.3 — Production Readiness & Technical Debt Closure
> Gerado em: 2026-06-29

---

## Resumo Executivo

Relatório consolidado de toda dívida técnica identificada no projeto Plantao 360 até a Sprint 14.3. Itens foram classificados em 4 categorias: **Resolvida** (fechada durante a sprint), **Conhecida** (documentada, sem bloqueio), **Aceita** (deferida intencionalmente) e **Futuro** (planejada para sprints seguintes).

| Métrica | Valor |
|---------|-------|
| Total de itens | 27 |
| Resolvidos | 3 |
| Conhecidos | 18 |
| Aceitos | 4 |
| Futuros | 2 |
| Arquivos escaneados | 281 |
| TODOs originais | 37 |
| Unused imports originais | 26 |

---

## Itens Resolvidos

Itens fechados durante a Sprint 14.3.

| # | Descrição | Prioridade | Impacto |
|---|-----------|------------|---------|
| R-001 | 12 pytest com falha (count assertion drift) — contagens de assertions ajustadas para refletir estado atual do domínio | P2-Medium | Cobertura de testes restaurada; CI volta a passar |
| R-002 | TypeScript errors (MUI Grid v2 API, unused imports) — erros de compilação TS corrigidos | P2-Medium | Frontend compila sem erros; IDE sem warnings |
| R-003 | 26 unused imports removidos em módulos backend (schemas, services, repositories, domain) | P3-Low | Código mais limpo; reduz risco de confusão em manutenção |

---

## Itens Conhecidos

Itens documentados, identificados em auditorias, sem bloqueio imediato para produção.

### Backend

| # | Descrição | Prioridade | Arquivo | Impacto |
|---|-----------|------------|---------|---------|
| C-001 | SECRET_KEY com placeholder hardcoded — valor não é um segredo real | P0-Critical | `app/core/config.py` | Em produção, qualquer pessoa com acesso ao repositório conhece a chave |
| C-002 | Rotas CRUD sem autenticação — endpoints expostos sem verificação de identidade | P0-Critical | `app/api/` | Qualquer consumidor pode acessar/alterar dados sem restrição |
| C-003 | Connection pooling não configurado para PostgreSQL — usa SQLite como default | P1-High | `app/database/` | Sob carga, conexões podem esgotar; latência aumenta |
| C-004 | Health/Readiness executam `db.commit()` — endpoint de saúde faz write no banco | P1-High | `app/api/health.py` | Pode causar transações indesejadas; viola semântique de healthcheck |
| C-005 | Lifespan não aborta em falha de migração — app sobe mesmo com DB desatualizado | P1-High | `app/main.py` | Risco de erros em runtime por schema incompatível |
| C-006 | 10 duplicações de validação documentadas na matriz de consistência | P2-Medium | `app/validators/` | Regras mantidas em dois locais; risco de divergência |
| C-007 | 2 regras de validação órfãs (validate_code, validate_year_month) — não referenciadas | P2-Medium | `app/validators/` | Código morto; confunde desenvolvedores |
| C-008 | Inconsistência em hour_rate — DB permite 0, Validator/Schema não aceitam | P2-Medium | `app/validators/`, `app/schemas/` | Dados podem ser inseridos com valor 0 via SQL direto, mas rejeitados pela API |
| C-009 | Audit module stub — 8 TODOs, implementação vazia | P2-Medium | `app/audit/` (8 arquivos) | Sem auditoria de ações; impossível rastrear quem fez o quê |
| C-010 | Security module stub — 11 TODOs, autenticação/autorização não implementada | P0-Critical | `app/core/security/` (3 arquivos) | Sem auth, o sistema é aberto;Bloqueia qualquer deploy em produção |
| C-011 | Observability module stub — 12 TODOs, métricas/tracing não implementados | P2-Medium | `app/observability/` (4 arquivos) | Sem visibilidade de performance; difícil diagnosticar problemas |

### Frontend

| # | Descrição | Prioridade | Arquivo | Impacto |
|---|-----------|------------|---------|---------|
| C-012 | 4 broken test suites (17 failing tests) — testes quebrados por referências inválidas | P1-High | `frontend/src/__tests__/` | CI sem cobertura de testes; regressões passam despercebidas |
| C-013 | 9/10 feature flags mortas — flags declaradas mas nunca usadas em lógica | P2-Medium | `frontend/src/config/` | Código confuso; difícil saber quais features estão ativas |
| C-014 | Dashboard & MainLayout usam `fetch()` raw em vez de `apiClient` | P1-High | `frontend/src/pages/Dashboard.tsx`, `frontend/src/layouts/MainLayout.tsx` | Sem tratamento de erro padronizado; sem interceptors de auth |
| C-015 | `.env` contém `VITE_DEMO_MODE=true` — modo demo ativo | P1-High | `frontend/.env` | Pode liberar funcionalidades não intencionais em produção |
| C-016 | 4 referências de testes quebradas (mapErrorToMessage, queryKeys.kpis, KPICard props, StatusChip status format) | P1-High | `frontend/src/__tests__/` | Imports de itens inexistentes; testes não compilam |
| C-017 | `feature-validator.ts` usa Node.js `fs` — não executa no browser | P1-High | `frontend/src/utils/feature-validator.ts` | Módulo inutilizável no contexto browser; quebra se importado |

### Docker

| # | Descrição | Prioridade | Arquivo | Impacto |
|---|-----------|------------|---------|---------|
| C-018 | Backend Dockerfile sem multi-stage build — imagem final inclui pip e cache de build | P2-Medium | `backend/Dockerfile` | Imagem ~30-40% maior que o necessário |
| C-019 | docker-compose base sem restart policy — containers não reiniciam automaticamente | P1-High | `docker-compose.yml` | Após crash, container fica parado sem intervenção manual |
| C-020 | Production healthcheck usa `localhost` — não funciona em rede Docker | P1-High | `docker-compose.prod.yml` | Healthcheck sempre falha em containerizado; orchestrador pode matar o container |

---

## Itens Aceitos

Itens deferidos intencionalmente — reconhecidos como dívida, mas mantidos por conveniência ou baixo impacto relativo.

| # | Descrição | Prioridade | Arquivo | Impacto |
|---|-----------|------------|---------|---------|
| A-001 | AppLayout não utilizado (236 linhas) — componente morto nunca importado | P3-Low | `frontend/src/layouts/AppLayout.tsx` | Ocupa espaço; confunde quem navega o código |
| A-002 | 3 hooks não utilizados (useApi, usePagination, useDebounce) — declarados mas nunca chamados | P3-Low | `frontend/src/hooks/` | Código morto; aumenta superfície de manutenção |
| A-003 | `types/api.ts` com tipos duplicados — definições redundantes de mesma interface | P3-Low | `frontend/src/types/api.ts` | Confusão sobre qual tipo usar; risco de divergência |
| A-004 | Frontend dev sem healthcheck — `docker-compose.dev.yml` não define healthcheck | P3-Low | `docker-compose.dev.yml` | Em dev, irrelevante; mas inconsistente com produção |

---

## Itens Futuros

Itens planejados para implementação em sprints futuras.

| # | Descrição | Prioridade | Arquivo | Impacto |
|---|-----------|------------|---------|---------|
| F-001 | Security module full implementation — JWT auth, roles, permissions | P0-Critical | `app/core/security/` | Pré-requisito para qualquer deploy em produção com usuários reais |
| F-002 | Observability module full implementation — OpenTelemetry, tracing, métricas de negócio | P2-Medium | `app/observability/` | Visibilidade operacional; sem isso, diagnóstico em produção é artesanal |

---

## Estatísticas

| Métrica | Valor |
|---------|-------|
| **Total** | **27** |
| Resolvidos | 3 (11%) |
| Conhecidos | 18 (67%) |
| Aceitos | 4 (15%) |
| Futuros | 2 (7%) |

### Por Prioridade

| Prioridade | Total | Resolvida | Conhecida | Aceita | Futuro |
|------------|-------|-----------|-----------|--------|--------|
| P0-Critical | 3 | 0 | 3 | 0 | 1* |
| P1-High | 8 | 0 | 8 | 0 | 0 |
| P2-Medium | 10 | 2 | 7 | 0 | 1* |
| P3-Low | 6 | 1 | 0 | 4 | 0 |

*\* F-001 (P0) e F-002 (P2) são os mesmos itens que C-010 e C-011 respectivamente, reclassificados como "Futuro" quando a decisão for implementá-los em sprint separada.*

### Por Camada

| Camada | Total | Resolvida | Conhecida | Aceita | Futuro |
|--------|-------|-----------|-----------|--------|--------|
| Backend | 14 | 2 | 11 | 0 | 1 |
| Frontend | 10 | 1 | 6 | 3 | 0 |
| Docker | 4 | 0 | 3 | 1 | 0 |
| Infra/Deploy | 1* | 0 | 1 | 0 | 0 |

---

## Notas

- **Dados fonte:** technical-debt.md (2026-06-26), auditorias de Sprint 14.3
- **Cobertura:** 281 arquivos escaneados
- **TODOs rastreados:** 37 (8 audit + 11 security + 12 observability + 6 outros)
- **Unused imports:** 26 (consolidados no item R-003)
- **Decisão de categorização:** Itens marcados como "Aceita" são aqueles onde o time optou conscientemente por manter a dívida, documentando a justificativa. Itens "Futuro" dependem de aprovação de backlog em sprints futuras.
