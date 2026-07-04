# Metas de Performance — Plantão 360

**Sprint:** 11 — Product Design, User Experience Modeling & Frontend Functional Specification
**Data:** 2026-06-27

---

## Visão Geral

Metas de performance para todas as interações do Frontend.

---

## 1. Abertura de Dashboard

| Métrica | Meta | Prioridade |
|---|---|---|
| Tempo de carregamento inicial | ≤ 2 segundos | Crítica |
| Tempo de renderização dos KPIs | ≤ 1 segundo após dados | Alta |
| Tempo de carregamento de gráficos | ≤ 1.5 segundos | Alta |
| Percepção do usuário | Imediato (skeleton) | Crítica |

### Estratégia
- Skeleton screen durante carregamento
- Carregamento paralelo de KPIs
- Cache de dados por 5 minutos
- Lazy loading de gráficos secundários

---

## 2. Pesquisa e Busca

| Métrica | Meta | Prioridade |
|---|---|---|
| Tempo de resposta da busca | ≤ 300ms | Crítica |
| Debounce de digitação | 300ms | Alta |
| Mínimo de caracteres | 2 | Média |
| Máximo de resultados | 20 | Média |

### Estratégia
- Debounce no input de busca
- Busca no cliente para listas pequenas
- Busca no servidor para listas grandes
- Índice de busca otimizado

---

## 3. Filtros

| Métrica | Meta | Prioridade |
|---|---|---|
| Tempo de aplicação do filtro | ≤ 200ms | Alta |
| Tempo de limpeza do filtro | ≤ 100ms | Média |
| Atualização da tabela | Imediata | Alta |

### Estratégia
- Filtros aplicados no cliente quando possível
- Atualização otimizada da tabela
- Debounce para filtros de texto
- Filtros de status com resposta imediata

---

## 4. Paginação

| Métrica | Meta | Prioridade |
|---|---|---|
| Tempo de troca de página | ≤ 200ms | Alta |
| Tempo de carregamento de dados | ≤ 500ms | Alta |
| Itens por página padrão | 20 | Média |
| Opções de itens por página | 10, 20, 50, 100 | Baixa |

### Estratégia
- Paginação no servidor
- Cache de páginas visitadas
- Prefetch da próxima página
- Transição suave entre páginas

---

## 5. Carregamentos

| Métrica | Meta | Prioridade |
|---|---|---|
| Tempo para mostrar skeleton | ≤ 100ms | Crítica |
| Tempo para mostrar spinner | ≤ 500ms | Alta |
| Feedback de carregamento | Imediato | Crítica |
| Timeout de requisição | 30 segundos | Alta |

### Estratégia
- Skeleton screens para carregamentos longos
- Spinners para carregamentos curtos
- Progress bars para operações de longa duração
- Retry automático em caso de falha

---

## 6. Feedback Visual

| Métrica | Meta | Prioridade |
|---|---|---|
| Tempo de resposta a clique | ≤ 200ms | Crítica |
| Tempo de feedback de sucesso | ≤ 500ms | Alta |
| Tempo de feedback de erro | Imediato | Crítica |
| Duração de toast de sucesso | 5 segundos | Média |
| Duração de toast de erro | Persistente | Alta |

### Estratégia
- Feedback imediato em botões (hover, active)
- Toast notifications para ações
- Modais para confirmações
- Animações de transição suaves

---

## 7. Tabelas

| Métrica | Meta | Prioridade |
|---|---|---|
| Tempo de ordenação | ≤ 100ms | Alta |
| Tempo de paginação | ≤ 200ms | Alta |
| Tempo de renderização | ≤ 300ms | Alta |
| Linhas visíveis sem scroll | 10-15 | Média |

### Estratégia
- Virtualização para tabelas grandes
- Ordenação no cliente quando possível
- Cache de dados ordenados
- Lazy loading de colunas

---

## 8. Formulários

| Métrica | Meta | Prioridade |
|---|---|---|
| Tempo de validação | ≤ 100ms | Alta |
| Tempo de submissão | ≤ 1 segundo | Alta |
| Feedback de erro | Imediato | Crítica |
| Feedback de sucesso | ≤ 500ms | Alta |

### Estratégia
- Validação em tempo real
- Debounce em campos de texto
- Submissão otimizada
- Feedback imediato

---

## 9. Gráficos

| Métrica | Meta | Prioridade |
|---|---|---|
| Tempo de renderização | ≤ 1.5 segundos | Média |
| Tempo de interação | ≤ 200ms | Alta |
| Tempo de tooltip | ≤ 100ms | Média |
| Animação de transição | ≤ 300ms | Baixa |

### Estratégia
- Renderização lazy de gráficos
- Cache de dados de gráficos
- Animações otimizadas
- Tooltip com debounce

---

## 10. Navegação

| Métrica | Meta | Prioridade |
|---|---|---|
| Tempo de troca de tela | ≤ 300ms | Crítica |
| Tempo de carregamento de dados | ≤ 500ms | Alta |
| Animação de transição | ≤ 200ms | Média |
| Deep link resolution | ≤ 500ms | Alta |

### Estratégia
- Code splitting por módulo
- Prefetch de rotas frequentes
- Cache de dados de navegação
- Transições otimizadas

---

## Resumo das Metas

| Categoria | Meta Principal | Prioridade |
|---|---|---|
| Dashboard | ≤ 2s carregamento | Crítica |
| Pesquisa | ≤ 300ms resposta | Crítica |
| Filtros | ≤ 200ms aplicação | Alta |
| Paginação | ≤ 200ms troca | Alta |
| Carregamentos | Imediato (skeleton) | Crítica |
| Feedback | ≤ 200ms resposta | Crítica |
| Tabelas | ≤ 300ms renderização | Alta |
| Formulários | ≤ 1s submissão | Alta |
| Gráficos | ≤ 1.5s renderização | Média |
| Navegação | ≤ 300ms troca | Crítica |

---

## Validação

| Critério | Status |
|---|---|
| Todas as metas definidas | ✅ |
| Prioridades classificadas | ✅ |
| Estratégias documentadas | ✅ |
| Métricas mensuráveis | ✅ |
