> ⚠️ **ADR HISTÓRICO — SUPERADO.** Registro mantido para rastreabilidade. A
> [Constituição](../../.specify/memory/constitution.md) (v1.1.0) supera os 31 ADRs onde houver
> conflito — em especial os de *freeze* e a arquitetura DDD/CQRS/event-sourcing, desmontada nas
> specs 003–006 (a `domain/` foi de 118 → ~13 arquivos; payroll/cobertura removidos). Índice e
> contexto em [docs/adr/README.md](README.md).

# ADR-026: Frontend Enterprise Architecture

**Date:** 2026-06-27
**Status:** Accepted
**Sprint:** 12

---

## Context

O Plantão 360 possui backend completo, domínio congelado e especificação funcional de 28 telas. A implementação do Frontend React requer uma arquitetura que suporte:

1. **Escalabilidade** — 20+ módulos futuros sem refatoração estrutural
2. **Consistência** — Mesmas regras em todas as features
3. **Manutenibilidade** — Facilidade de alterar componentes isoladamente
4. **Performance** — Carregamento otimizado e cache inteligente
5. **Testabilidade** — Componentes independentes e testáveis

---

## Decision

Declaramos a **Frontend Enterprise Architecture** com os seguintes elementos:

### 1. Feature-Based Architecture
- Organização por domínio (doctor, period, shift, etc.)
- Cada feature é um módulo independente
- Nunca organizar por tipo de componente

### 2. Query Layer (React Query)
- Query Keys padronizadas por feature
- Query Factories para queries e mutations
- Cache Strategy com staleTime de 5 minutos
- Invalidation Rules automáticas

### 3. State Strategy
| Tipo | Uso | Exemplo |
|---|---|---|
| Global | Apenas autenticação e persona | `useAuthStore` |
| Page | Filtros, paginação, ordenação | `useState` |
| Form | Estado de formulários | `useForm` |
| Transient | Modals, loading, errors | `useState` |

### 4. Component Strategy
- **Shared Components** — Reutilizáveis (StatusChip, KPICard, etc.)
- **Domain Components** — Específicos de feature (DoctorCard, etc.)
- **Page Components** — Tela completa (DoctorListScreen, etc.)
- **Layout Components** — Estrutura (AppLayout, etc.)

### 5. API Layer
- **API Client** — Abstração do Axios
- **Service Layer** — Endpoints por feature
- **Error Mapper** — Mensagens amigáveis
- **Interceptors** — Request/Response

### 6. Frontend Manifest
- JSON por feature documentando rotas, permissões, APIs
- Validador de estrutura (feature-validator.ts)
- Golden Frontend Module (Doctor) como referência

---

## Consequences

### Positivas
1. **Escalabilidade** — Novas features são módulos independentes
2. **Consistência** — Todas as features seguem mesma estrutura
3. **Performance** — Code splitting por feature
4. **Testabilidade** — Componentes independentes e testáveis
5. **Manutenibilidade** — Mudanças isoladas por feature

### Negativas
1. **Complexidade inicial** — Mais camadas para aprender
2. **Boilerplate** — Mais arquivos por feature
3. **Curva de aprendizado** — Equipe precisa entender a arquitetura

---

## Implementation

### Sprint 12 ETAPAs
| ETAPA | Status | Descrição |
|---|---|---|
| 1-2 | ✅ | Directory Structure |
| 3 | ✅ | API Layer |
| 4 | ✅ | Query Layer |
| 5 | ✅ | State Strategy (Types) |
| 6 | ✅ | Design System Foundation |
| 7 | ✅ | Domain Components |
| 8 | ✅ | Layout Engine |
| 9 | ✅ | Routing |
| 10 | ✅ | Error Experience |
| 11 | ✅ | Feature Manifests |
| 12 | ✅ | Frontend Validator |
| 13 | ✅ | Golden Frontend Module (Doctor) |
| 14 | ✅ | Storybook Readiness |
| 15 | ✅ | Documentation |
| 16 | ✅ | Test Infrastructure |
| 17 | ✅ | ADR-026 |

---

## References

- `docs/frontend/architecture/frontend-architecture.md`
- `docs/frontend/screen-inventory.md`
- `docs/frontend/frontend-contract-matrix.md`
- `docs/frontend/ux-rules.md`
- `frontend/manifests/doctor.json`
- `frontend/src/shared/utils/feature-validator.ts`
