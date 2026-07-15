# Dependency Matrix — Plantão 360

**Sprint:** 10.5 — Domain Freeze, Application Baseline & Integration Architecture
**Data:** 2026-06-27

---

## Visão Geral

A Dependency Matrix define quais dependências são permitidas e proibidas entre camadas do sistema.

---

## Regras Gerais

1. **Domain é independente** — não depende de nenhuma outra camada
2. **Dependências apontam para baixo** — camadas superiores dependem de camadas inferiores
3. **Dependências circulares são proibidas** — não há dependências circulares
4. **Dependências são explícitas** — todas as dependências devem ser documentadas

---

## Matriz de Dependências

### 1. Domain Layer

| Dependência | Permitida? | Justificativa |
|---|---|---|
| Domain → Python stdlib | ✅ | Permitido |
| Domain → SQLAlchemy | ❌ | Proibido |
| Domain → FastAPI | ❌ | Proibido |
| Domain → Pydantic | ❌ | Proibido |
| Domain → requests | ❌ | Proibido |
| Domain → httpx | ❌ | Proibido |
| Domain → External libs | ❌ | Proibido |
| Domain → Infrastructure | ❌ | Proibido |
| Domain → Application | ❌ | Proibido |
| Domain → API | ❌ | Proibido |

---

### 2. Application Layer

| Dependência | Permitida? | Justificativa |
|---|---|---|
| Application → Python stdlib | ✅ | Permitido |
| Application → Domain | ✅ | Permitido |
| Application → Pydantic | ✅ | Permitido (DTOs) |
| Application → SQLAlchemy | ❌ | Proibido |
| Application → FastAPI | ❌ | Proibido |
| Application → Infrastructure | ❌ | Proibido (usa interfaces) |
| Application → API | ❌ | Proibido |

---

### 3. Infrastructure Layer

| Dependência | Permitida? | Justificativa |
|---|---|---|
| Infrastructure → Python stdlib | ✅ | Permitido |
| Infrastructure → Domain | ✅ | Permitido (interfaces) |
| Infrastructure → Application | ✅ | Permitido |
| Infrastructure → SQLAlchemy | ✅ | Permitido |
| Infrastructure → FastAPI | ✅ | Permitido |
| Infrastructure → Pydantic | ✅ | Permitido |
| Infrastructure → External libs | ✅ | Permitido |
| Infrastructure → API | ❌ | Proibido |

---

### 4. API Layer

| Dependência | Permitida? | Justificativa |
|---|---|---|
| API → Python stdlib | ✅ | Permitido |
| API → Application | ✅ | Permitido |
| API → Domain | ❌ | Proibido (usa Application) |
| API → SQLAlchemy | ❌ | Proibido |
| API → FastAPI | ✅ | Permitido |
| API → Pydantic | ✅ | Permitido |
| API → Infrastructure | ❌ | Proibido |
| API → External libs | ❌ | Proibido |

---

## Diagrama de Dependências

```
┌─────────────────────────────────────────────────────────┐
│                      API Layer                          │
│  Depende de: Application, FastAPI, Pydantic             │
├─────────────────────────────────────────────────────────┤
│                  Application Layer                      │
│  Depende de: Domain, Pydantic                           │
├─────────────────────────────────────────────────────────┤
│                    Domain Layer                         │
│  Depende de: Python stdlib apenas                       │
├─────────────────────────────────────────────────────────┤
│                 Infrastructure Layer                    │
│  Depende de: Domain, Application, SQLAlchemy, FastAPI   │
└─────────────────────────────────────────────────────────┘
```

---

## Violações Detectadas

| Violação | Severidade | Ação |
|---|---|---|
| Nenhuma | — | Nenhuma |

**Status:** ✅ Nenhuma violação detectada

---

## Validação

| Critério | Status |
|---|---|
| Domain é independente | ✅ |
| Dependências apontam para baixo | ✅ |
| Dependências circulares ausentes | ✅ |
| Dependências são explícitas | ✅ |
| Violações documentadas | ✅ |
