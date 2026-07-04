# Design Principles — Plantão 360

## Pergunta Central

"Um coordenador médico consegue entender a situação operacional do hospital em menos de 30 segundos ao abrir o sistema?"

Estes 7 princípios governam todas as decisões de UX/UI do Plantão 360.

---

## P1 — Informação antes de Navegação

**O dado mais importante aparece primeiro, sem cliques.**

- O Dashboard é a primeira tela e deve responder à pergunta central imediatamente
- Dados críticos (plantões sem médico, cobertura baixa) aparecem acima da dobra
- Nenhum dado operacional importante deve estar escondido atrás de menus ou abas
- KPIs usam big numbers (2.5rem) com progress rings, não listas key-value

**Exemplo:**
```
❌ "Cobertura" como item de lista com valor "92.5%"
✅ Card com progress ring grande mostrando 92.5% + trend verde + label "Cobertura"
```

---

## P2 — Operação antes de Administração

**Priorizar o que o coordenador precisa agir agora.**

- Alertas críticos aparecem antes de métricas históricas
- "Próximas Ações" com botão de ação aparecem antes de "Atividade Recente"
- Ações urgentes (plantão sem médico) têm botão vermelho visível
- Dados financeiros ficam abaixo da dobra operacional

**Exemplo:**
```
❌ Grid: [KPIs] [Alertas] [Atividade] [Ações]
✅ Grid: [Alertas Críticos com Ação] [Próximas Ações] [KPIs Visuais] [Atividade]
```

---

## P3 — Poucos Cliques

**Máximo 3 cliques para qualquer ação crítica (UX-001).**

- Dashboard → Card de cobertura → Lista de plantões com cobertura baixa
- Dashboard → Alerta crítico → Ação de resolução
- Sidebar → Módulo → Ação desejada
- Cards do Dashboard são clicáveis e navegam para o módulo correspondente

---

## P4 — Alto Contraste

**Hierarquia visual clara — urgente vs. informativo.**

Sistema de 4 níveis visuais:

| Nível | Cor | Uso | Peso Visual |
|-------|-----|-----|-------------|
| 🔴 Crítico | `#FF4842` | Plantão sem médico, cobertura <70% | Máximo — pulsação, borda vermelha |
| 🟡 Atenção | `#FFB020` | Extras pendentes, cobertura <90% | Médio — ícone de warning |
| 🔵 Informativo | `#1B6FE0` | Status neutro, dados contextuais | Baixo — neutro |
| 🟢 Saudável | `#00B87A` | Cobertura OK, período fechado | Mínimo — cor de confiança |

**Regra:** Verde é cor de confiança/identidade, NÃO de destaque. Elementos verdes são os que NÃO precisam de ação.

---

## P5 — Tempo Real

**Auto-refresh, dados vivos, sem refresh manual.**

- Dashboard atualiza a cada 30s automaticamente
- `AutoRefreshIndicator` mostra discreto "Atualizado há 12s" no header
- Indicador visual de sincronização (ícone girando) durante refresh
- Skeleton loading apenas na primeira carga; depois, transição suave
- Sidebar mostra "Última sincronização: 09:21" com status 🟢

---

## P6 — Explicabilidade

**Todo número é rastreável (DomainExplanation).**

- KPIs mostram de onde vem o número (ex: "92.5% = 166/180 plantões cobertos")
- Trend indicators mostram variação vs. período anterior
- Cards clicáveis levam ao detalhamento dos dados
- Tooltips explicam fórmulas de cálculo quando relevante

---

## P7 — Feedback Imediato

**Toda ação gera resposta visual em <200ms.**

- `useFeedback()` hook padronizado para todas as telas
- Toast success (auto-dismiss 5s), error (persistente), warning, info
- Confirmações com explicação de impacto ("Esta ação não pode ser desfeita")
- Hover effects em cards interativos (scale 1.02, shadow elevation)
- Active states em botões (scale 0.98)
- Loading states inline para ações assíncronas

---

## Identidade Visual

### Cores Unimed Tubarão

| Uso | Cor | Hex |
|-----|-----|-----|
| **Primária** — botões, links, ações | Verde Unimed | `#00995D` |
| **Primária escura** — headers, textos | Verde Escuro | `#007A47` |
| **Primária clara** — backgrounds suaves | Verde Claro | `#E6F7EF` |
| **Fundo da aplicação** | Cinza Claro | `#F7F8FA` |
| **Superfícies (cards)** | Branco | `#FFFFFF` |
| **Texto primário** | Cinza Escuro | `#1A1A2E` |
| **Texto secundário** | Cinza Médio | `#6B7280` |

### Hierarquia de Cores

- **Verde** = Identidade da marca + estados positivos (confiança)
- **Âmbar** = Atenção (precisa de ação, mas não urgente)
- **Vermelho** = Crítico (precisa de ação imediata)
- **Azul** = Informativo (dados neutros, contexto)

### Tipografia

| Elemento | Fonte | Tamanho | Peso |
|----------|-------|---------|------|
| Título de Dashboard | Inter | 1.75rem | 700 |
| Big Number (KPI) | Inter | 2.5rem | 700 |
| Subtítulo | Inter | 1rem | 600 |
| Body | Inter | 0.875rem | 400 |
| Caption | Inter | 0.75rem | 400 |
| Label de status | Inter | 0.75rem | 600 |

---

## Validação Contínua

Durante toda a implementação, validar:

> "Esta tela parece um Centro de Operações Hospitalares ou apenas um CRUD administrativo?"

Se a resposta for "CRUD administrativo", revisar antes de prosseguir.
