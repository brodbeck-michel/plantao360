# Dashboard Wireframe — Centro de Operações Hospitalares

## Layout Geral

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SIDEBAR (280px)          │  CONTEÚDO PRINCIPAL                        │
│                           │                                            │
│  ┌─────────────────────┐  │  ┌──────────────────────────────────────┐  │
│  │ 🏥 Plantão 360      │  │  │  HEADER OPERACIONAL                 │  │
│  │ PS Unimed Tubarão   │  │  │  Hospital · Competência · Cobertura  │  │
│  └─────────────────────┘  │  │  Última sync · Estado 🟢            │  │
│                           │  └──────────────────────────────────────┘  │
│  Status: 🟢 Operação      │                                            │
│  Competência: Jul/2026    │  ┌──────────────────────────────────────┐  │
│  Sync: 09:21 · 🟢        │  │  ALERTAS CRÍTICOS (se houver)        │  │
│                           │  │  🔴 3 plantões sem médico [Resolver] │  │
│  ─────────────────────    │  └──────────────────────────────────────┘  │
│                           │                                            │
│  📊 Dashboard        ●   │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐     │
│  ─────────────────────    │  │COBER.│ │MÉDIC.│ │PLANT.│ │ HORAS│     │
│  📋 Operacional          │  │92.5% │ │ 24   │ │ 180  │ │2.160 │     │
│    Períodos               │  │[ring]│ │[ring]│ │[ring]│ │[ring]│     │
│    Plantões               │  │🟢+2% │ │🟡-1  │ │🟢 ok │ │🟢 ok │     │
│    Atribuições            │  └──────┘ └──────┘ └──────┘ └──────┘     │
│    Cobertura              │  (cards clicáveis → navegam ao módulo)    │
│    Extras                 │                                            │
│  ─────────────────────    │  ┌─────────────────┐ ┌─────────────────┐  │
│  👨‍⚕️ Gestão de Pessoal   │  │ HEALTH CARDS    │ │ PRÓXIMAS AÇÕES  │  │
│    Médicos                │  │ (variação de    │ │ ▸ Fechar Jun/26 │  │
│  ─────────────────────    │  │  layout)        │ │ ▸ Aprovar 12    │  │
│  💰 Financeiro            │  │                 │ │ ▸ Revisar dom.  │  │
│    Payroll                │  └─────────────────┘ └─────────────────┘  │
│  ─────────────────────    │                                            │
│  📈 Analytics             │  ┌──────────────────────────────────────┐  │
│    Dashboard              │  │  ÚLTIMOS EVENTOS                     │  │
│    Timeline               │  │  ▸ Dr. Silva — check-in 08:00       │  │
│    Relatórios             │  │  ▸ Extra aprovado — UTI noturno     │  │
│                           │  │  ▸ Competência Jun/26 fechada       │  │
│                           │  └──────────────────────────────────────┘  │
│                           │                                            │
│                           │  ┌──────────────────────────────────────┐  │
│                           │  │  PAINEL DE MÉTRICAS                  │  │
│                           │  │  [Cobertura] [Médicos] [Plantões]   │  │
│                           │  │  [Competência] [Extras/Payroll]      │  │
│                           │  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Seções Detalhadas

### 1. Header Operacional (acima do Dashboard)

Barra de status com contexto global da operação.

```
┌──────────────────────────────────────────────────────────────────────┐
│ 🏥 PS Unimed Tubarão  │  Competência: Jul/2026  │  Cobertura: 92.5% │
│                        │  Status: 🟢 Operação    │  Sync: 09:21      │
└──────────────────────────────────────────────────────────────────────┘
```

- **Hospital:** Nome da instituição (fixo)
- **Competência:** Período atual (26/Jun → 25/Jul)
- **Cobertura:** Percentual geral com cor semântica
- **Status:** 🟢🟡🔴 com label
- **Sync:** Última atualização + indicador de sincronização

### 2. Alertas Críticos (se houver)

Apenas aparece se houver alertas de severidade crítica.

```
┌──────────────────────────────────────────────────────────────────────┐
│ ⚠️ ALERTAS CRÍTICOS (2)                                            │
│ ┌────────────────────────────────────────────────────────────────┐  │
│ │ 🔴 3 plantões sem médico — Hoje 19h–07h         [Resolver →] │  │
│ │ 🟡 Competência Jul/26 com 5 extras pendentes   [Revisar →]  │  │
│ └────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

- Borda vermelha pulsante para críticos
- Botão de ação rápida "Resolver" ou "Revisar"
- Se não houver alertas: seção oculta (não mostra "Nenhum alerta")

### 3. Operational Health Cards (4 cards clicáveis)

Layout de 4 colunas com progress rings.

```
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ COBER.   │ │ MÉDICOS  │ │ PLANTÕES │ │ HORAS    │
│  92.5%   │ │   24     │ │   180    │ │ 2.160h   │
│ [█████░] │ │ [████░░] │ │ [██████] │ │ [██████] │
│ 🟢 +2.3%│ │ 🟡 -1    │ │ 🟢 ok    │ │ 🟢 ok    │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
  ↳ clica      ↳ clica     ↳ clica      ↳ clica
  → Cobertura  → Médicos   → Plantões   → Payroll
```

- Cada card é clicável e navega ao módulo correspondente
- Progress ring visual (MUI CircularProgress customizado)
- Trend indicator (seta + variação vs. período anterior)
- Cor semântica na borda inferior do card

### 4. Grid Variado (Health Cards + Próximas Ações)

Layout 2/3 + 1/3 para quebrar monotonia de grids idênticos.

```
┌─────────────────────────────┐ ┌─────────────────────────┐
│ 📊 RESUMO OPERACIONAL      │ │ ⏰ PRÓXIMAS AÇÕES       │
│                             │ │                         │
│ Plantões Titulares: 120     │ │ ▸ Fechar competência    │
│ Plantões Reforço: 48        │ │   Jun/26                │
│ Divisões de turno: 8        │ │   [Fechar →]            │
│ Extras registrados: 12      │ │                         │
│                             │ │ ▸ Aprovar 12 extras     │
│ Total de médicos: 24        │ │   pendentes             │
│ Médicos ativos: 22          │ │   [Aprovar →]           │
│                             │ │                         │
│ 🟢 Cobertura estável        │ │ ▸ Revisar escala de     │
│    +2.3% vs. mês anterior   │ │   domingo               │
│                             │ │   [Revisar →]           │
└─────────────────────────────┘ └─────────────────────────┘
```

- Painel esquerdo: lista de dados com contexto
- Painel direito: ações com botões de prioridade
- Variação de layout: não são cards idênticos

### 5. Últimos Eventos

Timeline compacta de eventos recentes.

```
┌──────────────────────────────────────────────────────────────────────┐
│ 📋 ÚLTIMOS EVENTOS                                                  │
│                                                                      │
│  09:15  🟢  Dr. Silva — check-in Plantão T1                         │
│  08:45  🟡  Extra aprovado — UTI noturno (Dr. Costa)                │
│  08:30  🔵  Competência Jun/26 fechada pelo financeiro              │
│  08:00  🟢  Dr. Santos — check-in Plantão R1                       │
│  07:55  🔴  Plantão T3 noturno sem médico atribuído                 │
│                                                                      │
│  [Ver todos →]                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

- Ícone de status por severidade
- Timestamp + descrição + médico/envolvido
- Link "Ver todos" para timeline completa

### 6. Painel de Métricas Operacionais

Métricas detalhadas em 5 categorias com visual variado.

```
┌──────────────────────────────────────────────────────────────────────┐
│ 📈 PAINEL DE MÉTRICAS                                               │
│                                                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────────────┐    │
│  │ COBERTURA  │  │  MÉDICOS   │  │  COMPETÊNCIA               │    │
│  │   92.5%    │  │   24/25    │  │  Jul/26 — Aberta           │    │
│  │ [███████░] │  │  ativos    │  │  ━━━━━━━━━━━━━░░░ 62%      │    │
│  │ +2.3% ↑    │  │  1 inativo │  │  19 de 30 dias             │    │
│  └────────────┘  └────────────┘  └────────────────────────────┘    │
│                                                                      │
│  ┌─────────────────────────┐  ┌─────────────────────────────────┐  │
│  │  PLANTÕES               │  │  EXTRAS / PAYROLL                │  │
│  │  T1: 22  T2: 20  T3: 18│  │  Extras pendentes: 5            │  │
│  │  R1: 15  R2: 13        │  │  Extras aprovados: 7            │  │
│  │  Total: 180             │  │  Payroll: Pendente              │  │
│  │  Sem médico: 3 🔴       │  │  Próximo fechamento: 25/Jul     │  │
│  └─────────────────────────┘  └─────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────┘
```

- Layout variado: não são todos cards idênticos
- Métricas de cobertura: progress bar
- Métricas de competência: timeline de progresso
- Métricas de plantões: distribuição por turno
- Métricas de payroll: status com pending highlight

---

## Regras de Layout

1. **Header Operacional** sempre visível no topo
2. **Alertas Críticos** só aparecem se houver (ocultos caso contrário)
3. **Health Cards** sempre 4 colunas em desktop, 2 em tablet, 1 em mobile
4. **Grid variado** — misturar painéis de tamanhos diferentes
5. **Timeline** sempre por último (dados históricos)
6. **Métricas** sempre na parte inferior (detalhes)

## Responsividade

| Breakpoint | Layout |
|------------|--------|
| Desktop (>1280px) | Sidebar + conteúdo com grid 4 colunas |
| Tablet (≤1024px) | Sidebar colapsada + grid 2 colunas |
| Mobile (≤768px) | Bottom nav + grid 1 coluna |

## Validação

> "Esta tela parece um Centro de Operações Hospitalares ou apenas um CRUD administrativo?"

**Critério de aceite:** Ao abrir o Dashboard, o coordenador deve conseguir em <30 segundos:
1. Ver o estado geral da operação (header)
2. Identificar se há alertas críticos (seção de alertas)
3. Ver as 4 métricas principais (health cards)
4. Saber quais ações precisa tomar (próximas ações)
5. Ver o que aconteceu recentemente (últimos eventos)
