# Application Baseline — Plantão 360

**Sprint:** 10.5 — Domain Freeze, Application Baseline & Integration Architecture
**Data:** 2026-06-27
**Status:** BASELINE

---

## Declaração

O Application Baseline do Plantão 360 define a arquitetura definitiva para a camada de aplicação. Todos os novos componentes devem seguir este baseline.

---

## Arquitetura de Camadas

```
┌─────────────────────────────────────────────────────────┐
│                      API Layer                          │
│  (FastAPI Routes, Schemas, Validators)                  │
├─────────────────────────────────────────────────────────┤
│                  Application Layer                      │
│  (Services, Commands, Queries, DTOs)                    │
├─────────────────────────────────────────────────────────┤
│                    Domain Layer                         │
│  (Aggregates, Value Objects, Events, Rules, Policies)  │
├─────────────────────────────────────────────────────────┤
│                 Infrastructure Layer                    │
│  (Database, External Systems, Integrations, Adapters)   │
└─────────────────────────────────────────────────────────┘
```

---

## 1. API Layer

### Responsabilidade
Receber requisições HTTP, validar entrada, retornar respostas.

### Componentes

| Componente | Responsabilidade | Padrão |
|---|---|---|
| `routes/` | Endpoints HTTP | FastAPI Router |
| `schemas/` | Request/Response DTOs | Pydantic V2 |
| `validators/` | Validação de entrada | Pydantic V2 |

### Regras
- Routes não contêm lógica de negócio
- Routes delegam para Services
- Schemas são imutáveis após criação
- Validators validam regras de negócio simples

---

## 2. Application Layer

### Responsabilidade
Orquestrar operações de negócio, coordenar Domain Objects.

### Componentes

| Componente | Responsabilidade | Padrão |
|---|---|---|
| `services/` | Orquestração de negócio | Service Pattern |
| `commands/` | Operações de escrita (CQRS) | Command Pattern |
| `queries/` | Operações de leitura (CQRS) | Query Pattern |
| `dto/` | Data Transfer Objects | Pydantic V2 |

### Regras
- Services orquestram Domain Objects
- Services não contêm lógica de negócio (domain regras)
- Services não acessam Infrastructure diretamente
- Commands modificam estado; Queries explicam estado

---

## 3. Domain Layer

### Responsabilidade
Conter toda a lógica de negócio pura.

### Componentes

| Componente | Responsabilidade | Padrão |
|---|---|---|
| `aggregates/` | Estados e comportamentos | Aggregate Pattern |
| `value_objects/` | Objetos imutáveis | Value Object Pattern |
| `events/` | Eventos de domínio | Domain Event Pattern |
| `rules/` | Regras de negócio | Business Rule Pattern |
| `policies/` | Políticas de domínio | Policy Pattern |
| `state_machines/` | Máquinas de estados | State Machine Pattern |

### Regras
- Domain é puramente Python
- Domain não importa infraestrutura
- Domain não importa SQLAlchemy
- Domain não importa FastAPI
- Domain não importa Pydantic
- Domain não possui external dependencies

---

## 4. Infrastructure Layer

### Responsabilidade
Implementar interfaces definidas pelo Domain.

### Componentes

| Componente | Responsabilidade | Padrão |
|---|---|---|
| `database/` | Persistência | SQLAlchemy 2.0 |
| `integrations/` | Integrações externas | Adapter Pattern |
| `repositories/` | Repositórios | Repository Pattern |
| `external/` | Sistemas externos | Anti-Corruption Layer |

### Regras
- Infrastructure implementa interfaces do Domain
- Infrastructure não contém lógica de negócio
- Infrastructure é substituível
- Integrações ocorrem via Adapter Pattern

---

## Padrões Aplicados

### 1. CQRS-Lite
- Commands: operações de escrita
- Queries: operações de leitura
- Read Models: modelos de consulta

### 2. Domain Events
- Eventos são publicados após operações
- Eventos são consumidos por projections
- Eventos são auditados

### 3. State Machines
- Estados são definidos por state machines
- Transições são validadas
- Estados são auditados

### 4. Repository Pattern
- Repositories abstraem persistência
- Repositories são injetados via Dependency Injection
- Repositories são substituíveis

### 5. Adapter Pattern
- Adapters abstraem sistemas externos
- Adapters implementam interfaces do Domain
- Adapters são substituíveis

---

## Tecnologias

| Camada | Tecnologia | Versão |
|---|---|---|
| API | FastAPI | Latest |
| Application | Python | 3.12 |
| Domain | Python | 3.12 |
| Infrastructure | SQLAlchemy | 2.0 |
| Database (Dev) | SQLite | Latest |
| Database (Prod) | PostgreSQL | Latest |
| Validation | Pydantic | V2 |
| Testing | pytest | Latest |

---

## Validação

### Critérios de Aceite

| Critério | Status |
|---|---|
| Domain é puramente Python | ✅ |
| Domain não importa infraestrutura | ✅ |
| Domain não importa SQLAlchemy | ✅ |
| Domain não importa FastAPI | ✅ |
| Domain não importa Pydantic | ✅ |
| Domain não possui external dependencies | ✅ |
| Infrastructure implementa interfaces do Domain | ✅ |
| Services não contêm lógica de negócio | ✅ |
| Routes não contêm lógica de negócio | ✅ |

---

## Referências

- `architecture-baseline-v1.md` — Baseline original
- `engineering-freeze.md` — Engenheiria congelada
- `domain-freeze.md` — Domínio congelado
