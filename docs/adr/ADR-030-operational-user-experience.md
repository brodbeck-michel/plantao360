> ⚠️ **ADR HISTÓRICO — SUPERADO.** Registro mantido para rastreabilidade. A
> [Constituição](../../.specify/memory/constitution.md) (v1.1.0) supera os 31 ADRs onde houver
> conflito — em especial os de *freeze* e a arquitetura DDD/CQRS/event-sourcing, desmontada nas
> specs 003–006 (a `domain/` foi de 118 → ~13 arquivos; payroll/cobertura removidos). Índice e
> contexto em [docs/adr/README.md](README.md).

# ADR-030: Operational User Experience

## Status

Accepted

## Context

O Plantão 360 evoluiu de um MVP funcional para uma ferramenta operacional de coordenação médica. O Dashboard atual (cards MUI genéricos, layout de ERP) não responde à pergunta central: "Um coordenador médico consegue entender a situação operacional do hospital em menos de 30 segundos?"

O backend está congelado (ADR-017, ADR-024). O domínio está congelado (ADR-024). Esta decisão afeta apenas UX/UI/Design System/Componentes React/Navegação/Microinterações.

## Decision

Implementar uma fundação de UX operacional completa, transformando o Plantão 360 de "CRUD administrativo" para "Centro de Operações Hospitalares".

### 7 Princípios de Design

1. **P1 — Informação antes de Navegação**: O dado mais importante aparece primeiro, sem cliques
2. **P2 — Operação antes de Administração**: Priorizar o que o coordenador precisa agir agora
3. **P3 — Poucos Cliques**: Máximo 3 cliques para qualquer ação crítica
4. **P4 — Alto Contraste**: Hierarquia visual clara — urgente vs. informativo
5. **P5 — Tempo Real**: Auto-refresh, dados vivos, sem refresh manual
6. **P6 — Explicabilidade**: Todo número é rastreável (DomainExplanation)
7. **P7 — Feedback Imediato**: Toda ação gera resposta visual em <200ms

### Identidade Visual

- **Primária**: Verde Unimed #00995D (identidade + estados positivos)
- **Fundo**: #F7F8FA (neutro)
- **Superfícies**: #FFFFFF (cards)
- **Texto**: #1A1A2E (primário), #6B7280 (secundário)

### Sistema de Status de 4 Níveis

| Nível | Cor | Uso |
|-------|-----|-----|
| 🟢 Saudável | #00B87A | Cobertura OK, período fechado |
| 🟡 Atenção | #FFB020 | Extras pendentes, cobertura <90% |
| 🔴 Crítico | #FF4842 | Plantões sem médico, cobertura <70% |
| 🔵 Informativo | #1B6FE0 | Status neutro, dados contextuais |

### Componentes Novos (22)

- 10 Operational Cards (InstitutionStatusBar, OperationalHealthCard, CoverageCard, CompetencyCard, CriticalAlertCard, UpcomingActionCard, OperationalMetricsPanel, OperationalStatusBadge, OperationalEmptyState + barrel)
- 7 Loading Components (SkeletonCard, SkeletonKPI, SkeletonTable, ProgressOverlay, AutoRefreshIndicator, ContentTransition + barrel)
- 4 Feedback Components (AppToast, AppDialog, AppConfirmation + barrel)
- 1 Provider (FeedbackProvider com useFeedback hook)

### Ajustes de UX

1. Dashboard responde primeiro a perguntas operacionais, depois KPIs
2. Todos os Operational Health Cards são clicáveis e navegam ao módulo correspondente
3. Sidebar mostra contexto operacional permanente (competência, hospital, sync, status)
4. Header Operacional acima do Dashboard com contexto global
5. Interface transmite sensação de sistema vivo (auto-refresh, indicadores, eventos)
6. Hierarquia visual única: Crítico > Atenção > Informativo
7. Verde = identidade + positivo, não dominante
8. Layout variado — não apenas grids de cards idênticos
9. Sem bibliotecas de gráficos nesta sprint

## Consequences

### Positivas
- Dashboard responde à pergunta central em <30 segundos
- Identidade visual hospitalar reconhecível
- Sistema de status unificado em toda a aplicação
- Componentes reutilizáveis para telas futuras
- Fundação preparada para dark mode

### Negativas
- 22 novos componentes para manter
- Tokens e paleta divergem do MUI padrão
- Necessário treinamento da equipe sobre novos componentes

### Neutras
- Backend não afetado (congelado)
- APIs existentes consumidas sem alteração
- Dark mode preparado mas não implementado

## References

- ADR-017: Engineering Freeze
- ADR-024: Domain Freeze Integration Architecture
- ADR-025: Product Design & Frontend Functional Specification
- ADR-026: Frontend Enterprise Architecture
- ADR-027: Golden Frontend Module
- ADR-028: Frontend Platform Governance
- ADR-029: Production Readiness
