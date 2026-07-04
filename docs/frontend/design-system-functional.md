# Design System Funcional — Plantão 360

**Sprint:** 11 — Product Design, User Experience Modeling & Frontend Functional Specification
**Data:** 2026-06-27

---

## Visão Geral

Definição funcional dos componentes de interface. NÃO desenha componentes. Define comportamento.

---

## 1. Tipos de Tabela

### 1.1 Tabela de Dados (DataTable)
- **Uso:** Listagem de registros (médicos, plantões, etc.)
- **Colunas:** Ordenáveis, redimensionáveis
- **Linhas:** Selecionáveis, com ações em linha
- **Paginação:** Inferior, com seletor de itens por página
- **Filtros:** Barra superior com filtros globais
- **Exportação:** Botão de exportar (CSV, PDF)

### 1.2 Tabela de Resumo (SummaryTable)
- **Uso:** KPIs, indicadores consolidados
- **Colunas:** Métricas, valores, variações
- **Linhas:** Apenas dados agregados
- **Sem paginação:** Todos os dados visíveis
- **Sem seleção:** Apenas visualização

### 1.3 Tabela de Histórico (HistoryTable)
- **Uso:** Timeline de eventos, audit trail
- **Colunas:** Timestamp, evento, usuário, detalhes
- **Linhas:** Cronológicas (mais recente primeiro)
- **Paginação:** Inferior
- **Filtros:** Por data, tipo de evento, usuário

---

## 2. Tipos de Formulário

### 2.1 Formulário de Criação (CreateForm)
- **Uso:** Criar novo registro
- **Campos:** Todos os obrigatórios
- **Ações:** Salvar, Cancelar
- **Validação:** Em tempo real
- **Feedback:** Toast de sucesso, redirect para lista

### 2.2 Formulário de Edição (EditForm)
- **Uso:** Editar registro existente
- **Campos:** Preenchidos com dados atuais
- **Ações:** Salvar, Cancelar
- **Validação:** Em tempo real
- **Feedback:** Toast de sucesso, manter na tela

### 2.3 Formulário de Filtro (FilterForm)
- **Uso:** Filtrar dados
- **Campos:** Opcionais, com valores padrão
- **Ações:** Aplicar, Limpar
- **Validação:** Opcional
- **Feedback:** Atualização da lista/tabela

### 2.4 Formulário de Busca (SearchForm)
- **Uso:** Busca global
- **Campo:** Único, com autocomplete
- **Ações:** Buscar
- **Validação:** Mínimo de 2 caracteres
- **Feedback:** Resultados em dropdown

---

## 3. Tipos de Filtro

### 3.1 Filtro por Data (DateFilter)
- **Componente:** Seletor de período ou range de datas
- **Opções:** Hoje, Última semana, Último mês, Personalizado
- **Formato:** DD/MM/AAAA

### 3.2 Filtro por Status (StatusFilter)
- **Componente:** Multi-select com badges
- **Opções:** Todas as possíveis para a entidade
- **Visual:** Cores diferentes por status

### 3.3 Filtro por Texto (TextFilter)
- **Componente:** Input com debounce
- **Comportamento:** Busca parcial
- **Delay:** 300ms

### 3.4 Filtro por Select (SelectFilter)
- **Componente:** Dropdown com busca
- **Opções:** Lista de valores possíveis
- **Comportamento:** Seleção múltipla opcional

---

## 4. Tipos de Timeline

### 4.1 Timeline Cronológica (ChronologicalTimeline)
- **Uso:** Eventos da instituição
- **Formato:** Vertical, com timestamps
- **Itens:** Ícone + título + descrição + timestamp
- **Filtros:** Por tipo de evento, período

### 4.2 Timeline de Processo (ProcessTimeline)
- **Uso:** Status de competência, fluxo de aprovação
- **Formato:** Horizontal, com etapas
- **Itens:** Etapa + status + responsável + timestamp
- **Estados:** Concluído, em andamento, pendente

### 4.3 Timeline de Mudanças (ChangeTimeline)
- **Uso:** Histórico de edições
- **Formato:** Vertical, com diffs
- **Itens:** Campo + valor anterior + valor novo + usuário + timestamp

---

## 5. Tipos de Card

### 5.1 Card de KPI (KPICard)
- **Uso:** Indicadores no dashboard
- **Conteúdo:** Título, valor, variação, ícone
- **Ação:** Click para drill-down
- **Estado:** Normal, alerta, sucesso

### 5.2 Card de Resumo (SummaryCard)
- **Uso:** Resumo de entidade
- **Conteúdo:** Título, dados principais, ações rápidas
- **Ação:** Click para detalhes
- **Estado:** Normal, selecionado

### 5.3 Card de Ação (ActionCard)
- **Uso:** Ações frequentes no dashboard
- **Conteúdo:** Ícone, título, descrição
- **Ação:** Click para iniciar ação
- **Estado:** Normal, hover

### 5.4 Card de Alerta (AlertCard)
- **Uso:** Notificações, alertas
- **Conteúdo:** Ícone, título, mensagem, ação
- **Ação:** Resolver, dispensar
- **Estado:** Info, warning, error, success

---

## 6. Tipos de Alerta

### 6.1 Alerta de Informação (InfoAlert)
- **Uso:** Informações contextuais
- **Cor:** Azul
- **Ícone:** Informação
- **Ação:** Apenas fechar

### 6.2 Alerta de Aviso (WarningAlert)
- **Uso:** Atenção necessária
- **Cor:** Amarelo
- **Ícone:** Aviso
- **Ação:** Revisar, dispenser

### 6.3 Alerta de Erro (ErrorAlert)
- **Uso:** Erros, falhas
- **Cor:** Vermelho
- **Ícone:** Erro
- **Ação:** Retry, contato suporte

### 6.4 Alerta de Sucesso (SuccessAlert)
- **Uso:** Confirmações
- **Cor:** Verde
- **Ícone:** Sucesso
- **Ação:** Apenas fechar

---

## 7. Tipos de Indicador

### 7.1 Indicador Numérico (NumericIndicator)
- **Uso:** KPIs principais
- **Conteúdo:** Valor numérico + unidade
- **Variação:** Setas indicando tendência
- **Meta:** Barra de progresso

### 7.2 Indicador Percentual (PercentageIndicator)
- **Uso:** Taxas, cobertura
- **Conteúdo:** Percentual + meta
- **Visual:** Circular ou barra
- **Cores:** Verde (>=90%), Amarelo (>=70%), Vermelho (<70%)

### 7.3 Indicador de Moeda (CurrencyIndicator)
- **Uso:** Valores financeiros
- **Conteúdo:** Valor + moeda
- **Formato:** R$ X.XXX,XX
- **Variação:** Comparativo com período anterior

### 7.4 Indicador de Contagem (CountIndicator)
- **Uso:** Quantidades
- **Conteúdo:** Número + label
- **Visual:** Badge ou número grande

---

## 8. Tipos de Diálogo

### 8.1 Diálogo de Confirmação (ConfirmDialog)
- **Uso:** Ações destrutivas
- **Conteúdo:** Título, descrição, botões confirmar/cancelar
- **Estilo:** Modal centralizado
- **Acesso:** Teclado (Enter/ESC)

### 8.2 Diálogo de Formulário (FormDialog)
- **Uso:** Formulário rápido
- **Conteúdo:** Formulário em modal
- **Estilo:** Modal com scroll
- **Acesso:** Teclado (Tab, Enter)

### 8.3 Diálogo de Detalhes (DetailDialog)
- **Uso:** Visualização rápida
- **Conteúdo:** Dados formatados
- **Estilo:** Modal largo
- **Acesso:** Teclado (ESC para fechar)

### 8.4 Diálogo de Processamento (ProcessingDialog)
- **Uso:** Operações longas
- **Conteúdo:** Progresso, etapa atual
- **Estilo:** Modal sem botão de fechar
- **Acesso:** Nenhum (aguardar conclusão)

---

## Resumo dos Componentes

| Categoria | Tipos | Total |
|---|---|---|
| Tabelas | 3 | 3 |
| Formulários | 4 | 4 |
| Filtros | 4 | 4 |
| Timelines | 3 | 3 |
| Cards | 4 | 4 |
| Alertas | 4 | 4 |
| Indicadores | 4 | 4 |
| Diálogos | 4 | 4 |
| **Total** | — | **30** |

---

## Validação

| Critério | Status |
|---|---|
| Todos os tipos definidos | ✅ |
| Comportamentos documentados | ✅ |
| Estados listados | ✅ |
| Sem referência a CSS/HTML | ✅ |
| Foco no funcional | ✅ |
