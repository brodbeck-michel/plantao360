> ⚠️ **ADR HISTÓRICO — SUPERADO.** Registro mantido para rastreabilidade. A
> [Constituição](../../.specify/memory/constitution.md) (v1.1.0) supera os 31 ADRs onde houver
> conflito — em especial os de *freeze* e a arquitetura DDD/CQRS/event-sourcing, desmontada nas
> specs 003–006 (a `domain/` foi de 118 → ~13 arquivos; payroll/cobertura removidos). Índice e
> contexto em [docs/adr/README.md](README.md).

# ADR-024: Domain Freeze, Application Baseline & Integration Architecture

**Date:** 2026-06-27
**Status:** Accepted
**Sprint:** 10.5

---

## Context

O Plantão 360 atingiu maturidade suficiente no domínio para transição da fase de modelagem para a fase de aplicação. O domínio possui 92 componentes congelados, 35 eventos de domínio, 5 state machines, 7 read models, 4 KPIs e sistema completo de explicabilidade.

A instituição precisa garantir que:
1. O domínio seja completamente independente de sistemas externos
2. Futuras integrações (Tasy, MV Soul, TOTVS, SAP, Senior) não afetem o domínio
3. A arquitetura de aplicação seja bem definida
4. Contratos de integração sejam estabelecidos antes de implementações concretas

---

## Decision

Declaramos **Domain Freeze** para todos os componentes existentes do domínio e estabelecemos a **Integration Architecture** com os seguintes elementos:

### 1. Domain Freeze
- Todos os 92 componentes do domínio estão congelados
- Qualquer alteração requer ADR e aprovação formal
- Domínio é puramente Python, zero dependências externas

### 2. Application Baseline
- Arquitetura de 4 camadas: API → Application → Domain → Infrastructure
- CQRS-lite: Commands modificam estado; Queries explicam estado
- Repository Pattern para abstração de persistência

### 3. Integration Architecture
- **Integration Contracts:** 6 contratos (Hospital, Payroll, Doctor, Schedule, Financial, Notification)
- **Anti-Corruption Layer:** 6 ACLs que traduzem dados externos para formato do domínio
- **External Adapters:** 6 adaptadores base + 5 placeholders (Tasy, MV Soul, TOTVS, SAP, Senior)
- **Data Mappers:** Estrutura para tradução de dados
- **Integration Providers:** Estrutura para injecção de dependência

### 4. Context Map
- 8 Bounded Contexts mapeados
- Relacionamentos documentados
- Bordas do contexto definidas

### 5. Dependency Matrix
- Domain é independente (zero dependências externas)
- Dependências apontam para baixo
- Dependências circulares proibidas

---

## Consequences

### Positivas

1. **Domínio protegido** — Nenhuma mudança externa afeta o domínio
2. **Integrações seguras** — Contratos e ACLs garantem tradução segura
3. **Substituibilidade** — Sistemas externos podem ser trocados sem afetar o domínio
4. **Testabilidade** — Contratos permitem testes com mocks
5. **Documentação** — Toda arquitetura está documentada

### Negativas

1. **Complexidade inicial** — Mais camadas para manter
2. **Overhead** — Tradução de dados adiciona processamento
3. **Aprendizado** — Equipe precisa entender novos padrões

### Neutras

1. **Placeholders** — Adaptadores futuros são apenas estruturas
2. **Flexibilidade** — Contratos podem ser estendidos conforme necessário

---

## Pergunta Fundamental

> **"Se daqui a cinco anos a instituição trocar o Tasy por outro ERP hospitalar, quantas linhas do domínio precisarão ser alteradas?"**

**Resposta:** Nenhuma.

O domínio é completamente independente de sistemas externos. Todas as integrações ocorrem através de contratos e adaptadores na camada de infraestrutura. O domínio jamais conhece sistemas externos.

---

## Alternatives Considered

### 1. Integração direta com Tasy
- **Rejeitada:** Acoplaria domínio ao Tasy
- **Risco:** Troca de sistema requer refactoring massivo

### 2. Integração via API Gateway
- **Rejeitada:** Adiciona complexidade sem benefício claro
- **Risco:** Overhead desnecessário

### 3. Integração via mensageria
- **Rejeitada:** Complexidade demais para necessidades atuais
- **Risco:** Síncronia difícil de garantir

---

## References

- `docs/architecture/domain-freeze.md`
- `docs/architecture/application-baseline.md`
- `docs/architecture/integration-architecture.md`
- `docs/architecture/context-map.md`
- `docs/architecture/dependency-matrix.md`
- `docs/reviews/domain-freeze-review.md`
- `docs/reviews/backend-readiness.md`
