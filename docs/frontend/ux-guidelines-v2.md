# UX Guidelines v2 — Plantão 360

## Quando usar cada componente

| Elemento | Quando Usar | Exemplo |
|----------|------------|---------|
| **OperationalHealthCard** | KPIs no Dashboard, métricas principais | Cobertura, Médicos, Plantões, Horas |
| **CoverageCard** | Exibir percentual de cobertura isoladamente | Detalhe de cobertura |
| **CompetencyCard** | Status da competência atual | Sidebar, Dashboard |
| **CriticalAlertCard** | Alertas que precisam de ação imediata | Plantões sem médico, cobertura baixa |
| **UpcomingActionCard** | Próximas ações com prioridade | Fechar competência, aprovar extras |
| **InstitutionStatusBar** | Status geral da operação no topo | Header de qualquer tela principal |
| **OperationalMetricsPanel** | Métricas detalhadas em múltiplas categorias | Dashboard, relatórios |
| **OperationalStatusBadge** | Badge de status em qualquer contexto | Status de plantão, médico, competência |
| **OperationalEmptyState** | Empty state contextual | Qualquer tela sem dados |

## Reglas de Layout

### Dashboard
1. **Header Operacional** sempre visível no topo
2. **Alertas Críticos** só aparecem se houver
3. **Health Cards** sempre 4 colunas em desktop
4. **Grid variado** — misturar painéis de tamanhos diferentes
5. **Métricas** na parte inferior (detalhes)

### Tabelas
- Listagens >5 itens
- Dados comparáveis
- Sempre com filtros visíveis quando >10 itens

### Cards
- KPIs, status, resumos
- Nunca para listas longas
- Máximo 6 no Dashboard

### Timelines
- Histórico, eventos, audit trail
- Últimos eventos: máximo 5 itens

### Empty States
- Sempre contextual (não genérico)
- Incluir ação recomendada
- Indicar pré-requisitos quando aplicável

## Loading Rules

| Cenário | Componente | Delay |
|---------|-----------|-------|
| Primeira carga | SkeletonCard/SkeletonKPI | 300ms |
| Refresh em background | AutoRefreshIndicator | Imediato |
| Operação longa | ProgressOverlay | Imediato |
| Transição de conteúdo | ContentTransition | Imediato |

## Feedback Rules

| Ação | Severidade | Duração |
|------|-----------|---------|
| Sucesso (criar, editar, excluir) | success | 5s automático |
| Erro de rede | error | Persistente |
| Erro de validação | error | 5s automático |
| Aviso (ação destrutiva) | warning | 5s automático |
| Informação | info | 4s automático |
| Confirmação | Dialog | Até resposta |

## Status Language

| Nível | Cor | Uso |
|-------|-----|-----|
| 🟢 Saudável | #00B87A | Cobertura OK, período fechado |
| 🟡 Atenção | #FFB020 | Extras pendentes, cobertura <90% |
| 🔴 Crítico | #FF4842 | Plantões sem médico, cobertura <70% |
| 🔵 Informativo | #1B6FE0 | Status neutro, dados contextuais |

## Validação Contínua

> "Esta tela parece um Centro de Operações Hospitalares ou apenas um CRUD administrativo?"

Se a resposta for "CRUD administrativo", revisar antes de prosseguir.
