# Frontend Production Review — Plantao 360

**Data:** 2026-06-29
**Etapa:** 7 — Frontend Production Review
**Escopo:** Auditoria completa de production readiness do frontend

---

## Visão Geral

| Item | Valor |
|------|-------|
| **Stack** | React 18, TypeScript 5, Vite 5, Vitest 1, MUI 5, React Query 5, Axios 1 |
| **Rotas definidas** | 37 rotas |
| **Rotas implementadas** | 5 rotas funcionais (HomePage, HealthPage, DashboardPage, DoctorListPage, DoctorDetailPage) |
| **Rotas ComingSoon** | 32 rotas (placeholder) |
| **Componentes compartilhados** | 16 componentes |
| **Hooks compartilhados** | 3 hooks (useApi, usePagination, useDebounce) |
| **Features** | 2 (dashboard, doctor) |
| **Testes** | 5 arquivos de teste |
| **Provider stack** | ThemeProvider → QueryProvider → ToastProvider → BrowserRouter |

---

## 1. Feature Flags

### Análise

O frontend define **10 feature flags** em `src/config/feature-flags.ts`, lidos de variáveis `VITE_*` no build time.

O backend define **10 feature flags** em `backend/app/core/features.py`, lidos de env vars em runtime.

**Não há sobreposição** entre os nomes dos flags frontend e backend. Os flags são independentes.

### Flags Definidas (Frontend)

| Flag | Variável | Default | Valor Atual (.env) | Usada em Componentes |
|------|----------|---------|---------------------|---------------------|
| `DEMO_MODE` | `VITE_DEMO_MODE` | `false` | `true` | Sim (`dashboard-page.tsx:132`) |
| `MOCK_API` | `VITE_MOCK_API` | `false` | `false` | **NÃO** |
| `REAL_API` | `VITE_REAL_API` | `true` | `true` | **NÃO** |
| `SHOW_DEBUG_PANEL` | `VITE_SHOW_DEBUG_PANEL` | `false` | (não definida) | **NÃO** |
| `ENABLE_EXPERIMENTAL_UI` | `VITE_ENABLE_EXPERIMENTAL_UI` | `false` | (não definida) | **NÃO** |
| `TIMELINE` | `VITE_TIMELINE` | `true` | (não definida) | **NÃO** |
| `HEALTH_CARDS` | `VITE_HEALTH_CARDS` | `true` | (não definida) | **NÃO** |
| `DRAG_AND_DROP` | `VITE_DRAG_AND_DROP` | `false` | (não definida) | **NÃO** |
| `EXPORT_PDF` | `VITE_EXPORT_PDF` | `false` | (não definida) | **NÃO** |
| `NOTIFICATIONS` | `VITE_NOTIFICATIONS` | `false` | (não definida) | **NÃO** |

### Flags Ativas

| Flag | Uso |
|------|-----|
| `DEMO_MODE` | Controla `refetchInterval` no dashboard (30s quando não é demo) |

### Flags Mortas (definidas mas nunca lidas)

| Flag | Motivo |
|------|--------|
| `MOCK_API` | Definida mas nenhum componente verifica seu valor |
| `REAL_API` | Definida mas nenhum componente verifica seu valor |
| `SHOW_DEBUG_PANEL` | Definida mas nenhum componente a renderiza |
| `ENABLE_EXPERIMENTAL_UI` | Definida mas nenhum componente a verifica |
| `TIMELINE` | Definida mas não condiciona nenhuma renderização |
| `HEALTH_CARDS` | Definida mas não condiciona nenhuma renderização |
| `DRAG_AND_DROP` | Definida mas feature não implementada |
| `EXPORT_PDF` | Definida mas feature não implementada |
| `NOTIFICATIONS` | Definida mas feature não implementada |

### Flags Backend (para referência)

| Flag Backend | Default |
|-------------|---------|
| `DARK_MODE` | `true` |
| `NOTIFICATIONS` | `false` |
| `EXPORT_PDF` | `false` |
| `ENABLE_JWT` | `false` |
| `ENABLE_AUDIT_LOG` | `false` |
| `ENABLE_BI` | `false` |
| `ENABLE_ANALYTICS` | `false` |
| `ENABLE_TASY_INTEGRATION` | `false` |
| `ENABLE_EXPORT_PDF` | `false` |
| `ENABLE_IMPORT_LEGACY` | `false` |

### Sobreposição Backend × Frontend

Não há sobreposição de nomes. Flags `NOTIFICATIONS` e `EXPORT_PDF` existem em ambos, mas são sistemas independentes (backend usa env vars, frontend usa `VITE_*`).

### Issues

1. **9 de 10 flags são mortas** — definidas mas nunca consumidas por componentes
2. **Duplicação de helpers** — `feature-flags.ts` expõe `isFeatureEnabled()`, `getEnabledFlags()`, `getDisabledFlags()` E `feature-flag-service.ts` expõe `featureFlags.isEnabled()`, `featureFlags.getEnabled()`, etc. São funções idênticas em dois módulos
3. **Hook `useFeatureFlagService`** — não é um hook React real (não usa estado/efeito), apenas retorna um singleton

### Status: **COM RESSALVAS**

---

## 2. React Query

### Análise

**Provider** (`query-provider.tsx`):
- `staleTime`: 5 minutos
- `gcTime`: 10 minutos
- `retry`: 2 (queries), 1 (mutations)
- `refetchOnWindowFocus`: false
- `refetchOnReconnect`: always

**Query Factory** (`query-factory.ts`):
- `createQuery` — queries simples
- `createPaginatedQuery` — queries paginadas
- `createMutation` — mutations CRUD
- `createDynamicMutation` — mutations com endpoint dinâmico
- Todos usam `apiClient` centralizado e `mapError` para tratamento de erros

**Query Keys** (`query-keys.ts`):
- Estrutura hierárquica bem definida: `doctors.all`, `doctors.lists()`, `doctors.list(filters)`, `doctors.details()`, `doctors.detail(id)`
- Domínios: doctors, periods, shifts, assignments, extras, coverage, payroll, dashboard, kpi, analytics
- Keys para `query.*` domain (dashboard, coverage, financial, etc.)

**Uso real:**
- `DashboardPage` — usa `queryKeys.dashboard.summary` com `fetchDashboard` via `fetch()` nativo
- `MainLayout` — usa `queryKeys['dashboard', 'context']` com `fetchDashboardContext` via `fetch()` nativo
- `HealthPage` — usa `['health']` inline (não usa `queryKeys.health`)
- Doctor module — usa `doctorQueries`/`doctorMutations` via factories

### Status: **APROVADO**

### Issues

1. **Inconsistência de fetch** — Dashboard e MainLayout usam `fetch()` nativo ao invés de `apiClient`. Isso bypassa interceptors (request ID, error mapping)
2. **HealthPage inline key** — Usa `['health']` hardcoded ao invés de `queryKeys.health`
3. **MainLayout stale time override** — Configura `staleTime: 30000` (30s) para o contexto operacional, diferente do global (5min). Não é um problema, mas deveria ter comentário justificativo
4. **Testes desatualizados** — `query-keys.test.ts` referencia `queryKeys.kpis.list()` e `queryKeys.explainability.entity()` que não existem na definição atual

---

## 3. Error Boundaries

### Análise

**Implementação** (`error-boundary.tsx`):
- Class component `ErrorBoundary` extends `React.Component`
- `getDerivedStateFromError` para catch de erros de renderização
- `componentDidCatch` para logging (apenas `console.error`)
- Fallback UI padronizado: ícone de erro + "Algo deu errado" + botão "Tentar Novamente"
- Suporte a `fallback` customizado via props
- Suporte a `onReset` callback

**Uso:**
- `DashboardPage` — wrapping o conteúdo
- `DoctorListPage` — wrapping o conteúdo
- `DoctorDetailPage` — wrapping o conteúdo
- `DoctorAuditPage` — wrapping o conteúdo
- `DoctorHistoryPage` — wrapping o conteúdo

### Status: **COM RESSALVAS**

### Issues

1. **Sem error tracking** — `componentDidCatch` apenas faz `console.error`. Em produção deveria enviar para serviço de error tracking (Sentry, etc.)
2. **Sem ErrorBoundary global** — Não há ErrorBoundary no nível de `App.tsx` ou `main.tsx`. Um erro em qualquer página não capturada derruba a app inteira
3. **Fallback não personalizado** — Todos os usos usam o fallback padrão. Poderia ter fallbacks específicos por feature

---

## 4. Suspense & Lazy Loading

### Análise

**React.lazy** (`App.tsx`):
- `HomePage` — lazy
- `HealthPage` — lazy
- `DashboardPage` — lazy
- `DoctorListPage` — lazy (com `.then()` para named export)
- `DoctorDetailPage` — lazy (com `.then()` para named export)

**Suspense:**
- Componente `LazyPage` wrapping cada lazy page com `<Suspense fallback={<PageLoader />}>`
- `PageLoader` — `CircularProgress` centralizado

**Code Splitting:**
- Vite gera chunks automaticamente para cada `React.lazy()`
- 5 chunks principais: home, health, dashboard, doctor-list, doctor-detail
- Rotas ComingSoon NÃO usam lazy loading (inline components)

### Status: **APROVADO**

### Issues

1. **ComingSoon components não são lazy** — 9 componentes `*ComingSoon` são definidos inline no `App.tsx`. Embora sejam leves, violam o padrão de code splitting
2. **Sem preload** — Não há preload de chunks para rotas prováveis (ex: DoctorList antes de DoctorDetail)

---

## 5. Cache Strategy

### Análise

**Configuração Global** (`query-provider.tsx`):
- `staleTime`: 5 minutos (dados considerados frescos por 5 min)
- `gcTime`: 10 minutos (dados em cache por 10 min após desmontagem)
- `retry`: 2 retries automáticos
- `refetchOnWindowFocus`: false (evita refetch desnecessário)
- `refetchOnReconnect`: always (recarrega ao reconectar)

**Invalidation:**
- `useCreateDoctor` → invalida `queryKeys.doctors.all`
- `useUpdateDoctor` → invalida `queryKeys.doctors.all` + `queryKeys.doctors.detail(id)`
- `useDeleteDoctor` → invalida `queryKeys.doctors.all`

**Polling:**
- `DashboardPage`: `refetchInterval: 30000` (30s) quando não é demo mode
- `MainLayout OperationalContextPanel`: `refetchInterval: 60000` (60s), `staleTime: 30000` (30s)

### Status: **APROVADO**

### Issues

1. **Invalidation limitada** — Apenas o módulo doctor implementa invalidação. Dashboard e outros módulos não invalidam cache
2. **Sem optimistic updates** — Mutations esperam resposta do servidor para atualizar UI
3. **gcTime vs staleTime** — Configuração adequada para o caso de uso (MVP operacional)

---

## 6. API Client

### Análise

**Implementação** (`client.ts`):
- Factory `createApiClient(config)` — cria instância Axios
- Instance singleton `apiClient` com baseURL `/api/v1` e timeout 30s
- **Request interceptor**: gera `X-Request-ID` único, armazena contexto
- **Response interceptor**: mapeia erros via `mapError()`
- **Error mapping** (`mapError()`): traduz erros Axios em `AppError` padronizado
  - Network error → `NETWORK_ERROR`
  - Server error com `message` → usa mensagem do backend
  - Status codes → mensagens em português (400, 401, 403, 404, 409, 422, 429, 500, 502, 503)
- **Sem retry no client** — retry é tratado pelo React Query

**Uso:**
- `doctor-api.ts` — usa `apiClient` corretamente
- `health.ts` — usa `apiClient` corretamente
- `query-factory.ts` — usa `apiClient` corretamente
- `DashboardPage` — **NÃO** usa `apiClient`, usa `fetch()` nativo
- `MainLayout OperationalContextPanel` — **NÃO** usa `apiClient`, usa `fetch()` nativo

### Status: **COM RESSALVAS**

### Issues

1. **`fetch()` nativo bypassa o client** — Dashboard e MainLayout usam `fetch()` ao invés de `apiClient`, perdendo request ID, error mapping e interceptors
2. **Sem auth headers** — O client não configura headers de autenticação (Authorization). Embora `ENABLE_JWT` esteja desativado no backend, o client deveria estar preparado
3. **Testes desatualizados** — `client.test.ts` importa `mapErrorToMessage` que **não existe** no `client.ts` (a função se chama `mapError`). Os testes falharão
4. **`createApiClient` sem config obrigatória** — `createApiClient()` aceita ser chamado sem argumentos (testes fazem isso), mas `baseURL` é obrigatório na interface

---

## 7. Environment Variables

### Análise

**Arquivo `.env`:**
```
VITE_DEMO_MODE=true
VITE_REAL_API=true
VITE_MOCK_API=false
VITE_API_URL=http://localhost:8000
```

**Variáveis usadas no código:**
- `VITE_DEMO_MODE` → lida em `feature-flags.ts` (DEMO_MODE)
- `VITE_REAL_API` → lida em `feature-flags.ts` (REAL_API)
- `VITE_MOCK_API` → lida em `feature-flags.ts` (MOCK_API)
- `VITE_API_URL` → lida em `vite.config.ts` para proxy

**Variáveis NÃO definidas no .env mas referenciadas:**
- `VITE_SHOW_DEBUG_PANEL`
- `VITE_ENABLE_EXPERIMENTAL_UI`
- `VITE_TIMELINE`
- `VITE_HEALTH_CARDS`
- `VITE_DRAG_AND_DROP`
- `VITE_EXPORT_PDF`
- `VITE_NOTIFICATIONS`

### Status: **COM RESSALVAS**

### Issues

1. **8 variáveis referenciadas mas não definidas** — Flags que dependem de defaults
2. **Hardcoded values no código**:
   - `vite.config.ts:4` — `apiTarget` usa `process.env.VITE_API_URL || 'http://localhost:8000'` (ok, é dev proxy)
   - `MainLayout.tsx:124` — URL hardcoded: `/api/v1/query/dashboard?include_health_cards=false&...`
   - `dashboard-page.tsx:61` — URL hardcoded: `/api/v1/query/dashboard`
3. **`.env` com DEMO_MODE=true** — Em produção, este arquivo NÃO deve ter `DEMO_MODE=true`

---

## 8. Dead Code Analysis

### Código Morto Encontrado

#### Hooks não utilizados

| Hook | Arquivo | Exportado mas nunca importado por componentes |
|------|---------|----------------------------------------------|
| `useApi` | `hooks/use-api.ts` | Exportado em `hooks/index.ts`, mas nenhum componente o importa |
| `usePagination` | `hooks/use-pagination.ts` | Exportado em `hooks/index.ts`, mas nenhum componente o importa |
| `useDebounce` | `hooks/use-debounce.ts` | Exportado em `hooks/index.ts`, mas nenhum componente o importa |
| `useToast` | `shared/providers/toast-provider.tsx` | Exportado mas nenhum componente o importa |

#### Componente não utilizado

| Componente | Arquivo | Motivo |
|-----------|---------|--------|
| `AppLayout` | `layouts/app-layout.tsx` | Layout alternativo. `MainLayout` é o usado em `App.tsx`. `AppLayout` não é importado por nenhum outro arquivo |

#### Funções/módulos não utilizados

| Item | Arquivo | Motivo |
|------|---------|--------|
| `feature-validator.ts` | `shared/utils/feature-validator.ts` | Usa `fs`/`path` do Node.js — não funciona no browser. Nunca é importado |
| `isFeatureEnabled()` | `config/feature-flags.ts` | Função standalone duplicada pelo `featureFlags.isEnabled()` |
| `getEnabledFlags()` | `config/feature-flags.ts` | Nunca chamada |
| `getDisabledFlags()` | `config/feature-flags.ts` | Nunca chamada |
| `useFeatureFlagService()` | `config/feature-flag-service.ts` | Só usada em `dashboard-page.tsx` |
| `healthApi` barrel | `api/index.ts` | `healthApi` NÃO é exportado pelo barrel (apenas `apiClient`, `createApiClient`, `mapError`) |

#### Tipos duplicados

| Tipo | Local 1 | Local 2 | Conflito |
|------|---------|---------|----------|
| `ApiError` | `types/api.ts` (status, detail, type) | `types/index.ts` (code, message, status, details, requestId) | Sim — definições diferentes |
| `PaginatedResponse<T>` | `types/api.ts` (items) | `types/index.ts` (data) | Sim — campo de items difere |
| `PaginationParams` | `types/api.ts` | `types/index.ts` | Não — idênticos |

**Nota:** `api.ts` parece ser a versão legada. `index.ts` é a versão atual usada pelo código.

#### Empty __init__.ts files

| Arquivo | Conteúdo |
|---------|----------|
| `api/__init__.ts` | Vazio |
| `hooks/__init__.ts` | Vazio |
| `routes/__init__.ts` | Vazio |
| `types/__init__.ts` | Vazio |
| `contexts/__init__.ts` | Vazio |
| `components/__init__.ts` | Vazio |
| `layouts/__init__.ts` | Vazio |
| `pages/__init__.ts` | Vazio |

Esses arquivos são desnecessários em projetos TypeScript/ES modules.

#### Testes com referências quebradas

| Teste | Problema |
|-------|----------|
| `api/__tests__/client.test.ts` | Importa `mapErrorToMessage` que **não existe** em `client.ts` |
| `services/__tests__/query-keys.test.ts` | Referencia `queryKeys.kpis.list()` e `queryKeys.explainability.entity()` que **não existem** na definição atual |
| `shared/components/__tests__/kpi-card.test.tsx` | Testa props (`trend="neutral"`, `target`, `description`) que **não existem** na interface `KPICardProps` atual |
| `shared/components/__tests__/status-chip.test.tsx` | Testa `status="in-progress"` que não existe no tipo `StatusType` (deveria ser `in_progress`) |

#### Código não utilizado no doctor module

| Export | Arquivo | Importado externamente? |
|--------|---------|------------------------|
| `DoctorHistoryPage` | `doctor/index.ts` | Não (apenas exportado) |
| `DoctorAuditPage` | `doctor/index.ts` | Não (apenas exportado) |
| `DoctorProfileDrawer` | `doctor/index.ts` | Não (apenas exportado) |
| `useDoctorSearch` | `doctor/index.ts` | Não (apenas exportado) |
| `fetchDoctors`, `fetchDoctor`, etc. | `doctor/index.ts` | Não (apenas exportado) |

**Nota:** Esses exports são legítimos para uso futuro. São parte da API pública do módulo doctor.

### Status: **COM RESSALVAS**

### Issues

1. **`feature-validator.ts` é incompatível com browser** — Usa `fs`/`path` do Node.js. Deveria ficar em `tools/` ou ser removido do bundle
2. **3 hooks compartilhados não usados** — `useApi`, `usePagination`, `useDebounce` são exportados mas nenhum componente os consome
3. **`AppLayout` é código morto** — Layout completo (~236 linhas) não utilizado
4. **4 arquivos de teste com referências quebradas** — Testes falharão ao serem executados
5. **Tipos `api.ts` duplicados** — `types/api.ts` e `types/index.ts` definem `ApiError` e `PaginatedResponse` com assinaturas diferentes

---

## Resumo

| Área | Status | Issues |
|------|--------|--------|
| **Feature Flags** | COM RESSALVAS | 9/10 flags mortas; helpers duplicados |
| **React Query** | APROVADO | Configuração sólida; fetch nativo em 2 locais |
| **Error Boundaries** | COM RESSALVAS | Sem error tracking; sem boundary global |
| **Suspense & Lazy Loading** | APROVADO | 5 rotas com code splitting adequado |
| **Cache Strategy** | APROVADO | Configuração apropriada para MVP |
| **API Client** | COM RESSALVAS | fetch() bypassa client; testes quebrados |
| **Environment Variables** | COM RESSALVAS | .env com DEMO_MODE=true; 8 vars não definidas |
| **Dead Code** | COM RESSALVAS | 3 hooks + 1 layout + 1 util + 4 testes quebrados |

### Geral: **COM RESSALVAS**

---

## Pendências

### Críticas (bloqueiam produção)

1. **Corrigir testes quebrados** — `client.test.ts` (mapErrorToMessage), `query-keys.test.ts` (kpis, explainability), `kpi-card.test.tsx` (props inexistentes), `status-chip.test.tsx` (status in-progress)
2. **Remover DEMO_MODE=true do .env de produção** — Risco de mostrar dados mock em prod
3. **Unificar fetch** — Dashboard e MainLayout devem usar `apiClient` ao invés de `fetch()` nativo

### Importantes (devem ser resolvidas)

4. **Adicionar ErrorBoundary global** — Em `App.tsx` ou `main.tsx` para capturar erros não tratados
5. **Limpar feature flags mortas** — Remover 9 flags não utilizadas ou implementar seu uso
6. **Remover código morto** — `AppLayout`, `feature-validator.ts`, hooks não usados
7. **Resolver tipos duplicados** — `types/api.ts` vs `types/index.ts`
8. **Adicionar error tracking** — Sentry ou similar no `componentDidCatch`

### Desejáveis (melhorias)

9. **Preload de chunks** — Para rotas prováveis (ex: doctor-detail após doctor-list)
10. **Documentar variáveis de ambiente** — Criar `.env.example` com todas as variáveis
11. **Remover empty `__init__.ts`** — São desnecessários em TypeScript/ES modules
12. **Consolidar helpers de feature flags** — `isFeatureEnabled()` vs `featureFlags.isEnabled()`
