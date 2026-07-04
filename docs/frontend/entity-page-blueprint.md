# Entity Page Blueprint — Plantão 360

**Sprint:** 13 — Golden Frontend Module
**Data:** 2026-06-27

---

## Visão Geral

Toda página de entidade no Plantão 360 segue este padrão.

---

## Estrutura Padrão

```
┌─────────────────────────────────────────────────────┐
│                    PAGE HEADER                      │
│  Breadcrumb > Título > Subtítulo > [Ações]          │
├─────────────────────────────────────────────────────┤
│                    TOOLBAR                          │
│  Contador > [Filtros] > [Exportar] > [Criar]        │
├─────────────────────────────────────────────────────┤
│                   FILTER BAR                        │
│  Pesquisa > Filtros > Limpar                        │
├─────────────────────────────────────────────────────┤
│                    DATA TABLE                       │
│  Colunas > Ordenação > Seleção > Ações              │
├─────────────────────────────────────────────────────┤
│                   PAGINATION                        │
│  Linhas por página > Navegação                      │
├─────────────────────────────────────────────────────┤
│               TABS (opcional)                       │
│  Detalhes | Histórico | Auditoria                   │
├─────────────────────────────────────────────────────┤
│                  FEEDBACK                           │
│  Snackbar (sucesso/erro)                            │
└─────────────────────────────────────────────────────┘
```

---

## Componentes por Seção

### 1. PageHeader
- Breadcrumb
- Título (h1)
- Subtítulo
- Status badge (opcional)
- Botões de ação

### 2. Toolbar
- Contador de registros
- Botão de exportar (opcional)
- Botão de criar
- Contador de selecionados (quando aplicável)

### 3. FilterBar
- Campo de pesquisa
- Filtros expansíveis
- Botão de limpar
- Contador de filtros ativos

### 4. DataTable
- Colunas ordenáveis
- Seleção múltipla (opcional)
- Menu de ações por linha
- Loading skeleton
- Empty state
- Retry on error

### 5. Pagination
- Linhas por página
- Navegação entre páginas
- Exibição "X-Y de Z"

### 6. Tabs (opcional)
- Detalhes
- Histórico
- Auditoria

### 7. Feedback
- Snackbar de sucesso
- Snackbar de erro
- Dialog de confirmação

---

## Dialogs Padrão

| Dialog | Uso | Severidade |
|---|---|---|
| Create | Criar nova entidade | - |
| Edit | Editar entidade existente | - |
| Delete | Excluir entidade | error |
| Deactivate | Desativar entidade | warning |
| Confirm | Confirmação genérica | warning |

---

## Hooks Padrão

| Hook | Tipo | Descrição |
|---|---|---|
| useEntityList | Query | Listar entidades |
| useEntityDetail | Query | Detalhar entidade |
| useEntitySummary | Query | Resumo da entidade |
| useCreateEntity | Mutation | Criar entidade |
| useUpdateEntity | Mutation | Atualizar entidade |
| useDeleteEntity | Mutation | Excluir entidade |
| useEntityFilters | State | Gerenciar filtros |
| useEntitySort | State | Gerenciar ordenação |
| useEntityPagination | State | Gerenciar paginação |
| useEntitySelection | State | Gerenciar seleção |

---

## Referências

- `features/doctor/` — Golden Frontend Module
- `shared/components/` — Componentes reutilizáveis
