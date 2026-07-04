# UX Operational Audit — Sprint 15

## Referência Operacional

**Sistema de referência:** `plantoes_ps_unimed.html` — Planilha HTML local usada atualmente pela equipe de coordenação do PS Unimed Tubarão.

**Sistema alvo:** Plantão 360 — Frontend React/MUI em desenvolvimento.

**Pergunta central:** "Um coordenador médico consegue entender a situação operacional do hospital em menos de 30 segundos ao abrir o sistema?"

---

## Comparativo: Referência vs Plantão 360

### ✅ O que preservar (da referência HTML)

| Elemento | Por quê | Como implementar |
|----------|---------|------------------|
| **Barra de período** — competência visível no topo, com navegação ← → | O coordenador sempre precisa saber "em que mês estamos" | `InstitutionStatusBar` com competência atual |
| **Métricas resumidas** — grid de KPIs numéricos grandes (26px+) | Vista rápida de totais: plantões, horas, médicos | `OperationalHealthCard` com progress rings |
| **Legenda de turnos** — T1/T2/T3/R1/R2 com cores e horários | Linguagem operacional padronizada | `StatusChip` com códigos de turno |
| **Tabela de escala** — grade diária com dropdowns por turno | Forma mais eficiente de visualizar/atribuir escalas | `DataTable` existente, manter |
| **Tags coloridas** — Titular(azul), Reforço(verde), Dividido(roxo), Extra(âmbar) | Hierarquia visual clara por tipo | Estender `StatusChip` com variantes |
| **Toast de confirmação** — feedback discreto no rodapé | Confirmação de ações sem blocking | `AppToast` padronizado |
| **Modais contextuais** — formulários de atribuição inline | Ações rápidas sem navegação | `AppDialog` + `AppConfirmation` |
| **Métricas de remuneração** — cards de resumo financeiro | Visão financeira por competência | `OperationalMetricsPanel` |
| **Relatório por período** — filtragem por data com totais | Análise temporal | Manter `FilterBar` existente |

### ❌ O que eliminar (do Plantão 360 atual)

| Elemento | Problema | Solução |
|----------|----------|---------|
| **Cards MUI genéricos** — todos idênticos, sem hierarquia visual | Parece ERP, não centro de operações | `OperationalHealthCard` com layouts variados |
| **KPIs como lista key-value** — "Total de Plantões: 180" em texto simples | Sem impacto visual, sem urgência | Progress rings + big numbers + trends |
| **Alertas MUI `<Alert>` empilhados** — todos com o mesmo peso | Crítico e informativo misturados | `CriticalAlertCard` com severidade visual |
| **Layout 2x2 simétrico** — grids de cards idênticos | Monotonia visual, sem variação | Layout assimétrico com painéis diferentes |
| **Empty states genéricos** — "Nenhum registro encontrado" | Sem contexto operacional | `OperationalEmptyState` com SVG contextual |
| **Loading mix** — CircularProgress em uns, Skeleton em outros | Inconsistência perceptível | Sistema unificado com anti-flickering |
| **Sidebar sem contexto** — apenas navegação | Coordenador precisa ver status na sidebar | Sidebar com indicadores operacionais permanentes |
| **AppBar genérica** — search placeholder + avatar | Sem indicador de estado do sistema | Header operacional com status全局 |
| **Breadcrumbs triviais** — "Dashboard" | Sem contexto operacional | Breadcrumbs com competência + status |

### 🚀 O que superar (além da referência)

| Capacidade | Na referência HTML | No Plantão 360 |
|------------|-------------------|----------------|
| **Velocidade de compreensão** | Aba "Resumo" mostra métricas | Dashboard responde em <30s com header + cards + alertas |
| **Alertas proativos** | Nenhum — dados estáticos | `CriticalAlertCard` com ação rápida + pulsação |
| **Operação em tempo real** | Dados fixos no HTML | Auto-refresh 30s + `AutoRefreshIndicator` |
| **Navegação por módulo** | Abas (Planilha, Resumo, Médicos) | Sidebar com badges + cards clicáveis |
| **Feedback de ação** | Toast genérico no rodapé | `useFeedback()` padronizado com 4 severidades |
| **Empty states inteligentes** | "Nenhum plantão registrado" | Contexto operacional + ação recomendada |
| **Acessibilidade** | Nenhuma | ARIA + keyboard nav + screen reader |
| **Responsividade** | Print CSS apenas | Mobile + Tablet + Desktop breakpoints |
| **Identidade visual** | CSS customizado, cores fixas | Design system Unimed + tokens |

---

## Diagnóstico por Seção

### Dashboard Atual (Plantão 360)

| Critério | Nota | Observação |
|----------|------|------------|
| Responde em 30s? | ❌ Não | Lista de dados sem hierarquia |
| Hierarquia de urgência? | ❌ Não | Tudo tem o mesmo peso visual |
| Linguagem de status? | ⚠️ Parcial | `StatusChip` existe mas não é operacional |
| Loading consistente? | ❌ Não | Mix de spinner/skeleton |
| Empty states? | ❌ Genérico | "Nenhum registro encontrado" |
| Feedback visual? | ⚠️ Parcial | `ToastProvider` existe mas subutilizado |
| Identidade? | ❌ Não | Parece MUI boilerplate |

### Sidebar Atual

| Critério | Nota | Observação |
|----------|------|------------|
| Navegação funcional? | ✅ Sim | Seções colapsáveis funcionam |
| Contexto operacional? | ❌ Não | Apenas links, sem status |
| Indicadores? | ❌ Não | Sem badges de alertas |
| Competência visível? | ⚠️ Parcial | `OperationalContext` existe mas é discreto |

### Referência HTML

| Critério | Nota | Observação |
|----------|------|------------|
| Responde em 30s? | ⚠️ Parcial | Métricas no topo, mas precisa de abas |
| Hierarquia de urgência? | ⚠️ Parcial | Cores por tipo de turno |
| Layout operacional? | ✅ Sim | Parece ferramenta de operação |
| Identidade? | ✅ Sim | Visual Unimed Tubarão reconhecível |

---

## Decisões de Design Derivadas

1. **Dashboard = Centro de Operações** — Não é uma lista de dados, é um painel de monitoramento
2. **Alertas primeiro** — A seção mais importante do Dashboard é "O que precisa de ação agora"
3. **Cards clicáveis** — Todo card de métrica navega para o módulo correspondente
4. **Header operacional** — Barra de status acima do Dashboard com contexto global
5. **Sidebar viva** — Indicadores permanentes de competência, alertas e sincronização
6. **Variedade de layout** — Não apenas grids de cards idênticos; misturar painéis, timelines, listas
7. **Verde com moderação** — Identidade Unimed nos elementos de marca, não em toda a interface
8. **Sistema vivo** — Auto-refresh, indicadores de sincronização, eventos recentes visíveis

---

## Aprovação

| Item | Status |
|------|--------|
| Auditoria completa | ✅ |
| Decisões de design documentadas | ✅ |
| Pronto para ETAPA 1 (Design Principles) | ✅ |
