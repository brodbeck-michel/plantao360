# Regras de UX — Plantão 360

**Sprint:** 11 — Product Design, User Experience Modeling & Frontend Functional Specification
**Data:** 2026-06-27

---

## 1. Regras Gerais

### UX-001: Limite de Cliques
- Nenhuma ação crítica deve exigir mais de 3 cliques
- Exceção: operações de governance (aprovção) podem ter até 5 passos

### UX-002: Confirmação de Ações Destrutivas
- Toda operação destrutiva (cancelar, desativar, excluir) deve solicitar confirmação
- Confirmação deve incluir: ação, impacto, opção de cancelar
- Exceção: desativar médico requer justificativa adicional

### UX-003: Feedback Imediato
- Toda ação deve gerar feedback visual em até 200ms
- Feedback deve ser claro: sucesso, erro, ou carregamento
- Operações longas devem mostrar progresso

### UX-004: Mensagens Derivadas do Domínio
- Mensagens de erro devem vir do DomainExplanation
- Mensagens de sucesso devem descrever o resultado
- Nunca mostrar mensagens técnicas ao usuário

### UX-005: Indicadores Explicáveis
- Todo indicador (KPI) deve ser clicável para mostrar como foi calculado
- Drill-down deve mostrar passo a passo do cálculo
- Fonte de dados deve ser identificável

### UX-006: Consistência Visual
- Ações similares devem ter posicionamento consistente
- Botões de ação principal sempre no canto superior direito
- Botões de cancelamento sempre à esquerda do principal

### UX-007: Acessibilidade
- Todas as imagens devem ter alt text
- Contraste mínimo de 4.5:1
- Navegação por teclado completa
- Focus ring visível

### UX-008: Empty States
- Tela vazia deve explicar o que é e como preencher
- Incluir botão de ação primária para criar primeiro registro
- Nunca mostrar apenas "Nenhum registro encontrado"

### UX-009: Loading States
- Dados carregando devem mostrar skeleton
- Skeleton deve refletir a estrutura da tela
- Nunca mostrar apenas spinner genérico

### UX-010: Error States
- Erros de rede devem sugerir retry
- Erros de validação devem indicar campo específico
- Erros de servidor devem sugerir contato com suporte

---

## 2. Regras de Tabelas

### UX-011: Ordenação
- Colunas ordenáveis devem ter ícone indicativo
- Ordenação padrão deve ser a mais relevante para o contexto
- Permitir ordenação por múltiplas colunas

### UX-012: Filtragem
- Filtros devem ser aplicáveis individualmente
- Filtros ativos devem ser visíveis
- Permitir limpar todos os filtros com uma ação

### UX-013: Paginação
- Padrão: 20 itens por página
- Permitir alterar quantidade (10, 20, 50, 100)
- Mostrar total de itens e página atual

### UX-014: Ações em Linha
- Ações de visualizar, editar, excluir na mesma linha
- Máximo 3 ações visíveis
- Ações extras em menu dropdown

---

## 3. Regras de Formulários

### UX-015: Validação em Tempo Real
- Validar campo ao perder foco
- Mostrar erro imediatamente
- Permitir submissão apenas com todos os campos válidos

### UX-016: Campos Obrigatórios
- Indicar com asterisco (*)
- Mensagem de erro deve explicar o que é esperado
- Nunca deixar campo vazio sem aviso

### UX-017: Autocomplete
- Busca deve ser debounced (300ms)
- Mínimo de 2 caracteres para buscar
- Mostrar "Nenhum resultado" quando aplicável

### UX-018: Dates e Times
- Formato: DD/MM/AAAA para datas
- Formato: HH:MM para horários
- Calendário deve destacar dias com eventos

### UX-019: Selects
- Ordenar opções por relevância
- Permitir busca dentro do select
- Mostrar selected value claramente

---

## 4. Regras de Dialogs e Modals

### UX-020: Confirmação
- Título claro da ação
- Descrição do impacto
- Botão de confirmação com cor de perigo (vermelho) para ações destrutivas
- Botão de cancelar sempre visível

### UX-021: Formulário em Modal
- Modal deve ter tamanho adequado ao conteúdo
- Fechar com ESC ou clique fora
- Confirmação ao fechar com dados preenchidos

### UX-022: Alertas
- Alertas devem ser não-bloqueantes quando possível
- Timeout para alertas de sucesso (5 segundos)
- Alertas de erro persistem até ação do usuário

---

## 5. Regras de Notificações

### UX-023: Toast Notifications
- Posição: canto superior direito
- Duração: 5 segundos para sucesso, persistente para erro
- Permitir fechar manualmente

### UX-024: Notificações In-App
- Badge no ícone de notificação
- Lista de notificações com timestamp
- Marcar como lida ao visualizar

---

## 6. Regras de Keyboard

### UX-025: Atalhos de Tecla
- `Enter` para confirmar ações
- `ESC` para cancelar/fechar
- `Tab` para navegar entre campos
- `Shift+Tab` para navegar backwards

---

## Resumo das Regras

| Categoria | Quantidade |
|---|---|
| Gerais | 10 |
| Tabelas | 4 |
| Formulários | 5 |
| Dialogs/Modals | 3 |
| Notificações | 2 |
| Keyboard | 1 |
| **Total** | **25** |

---

## Validação

| Critério | Status |
|---|---|
| Regras gerais definidas | ✅ |
| Regras de tabelas definidas | ✅ |
| Regras de formulários definidas | ✅ |
| Regras de dialogs definidas | ✅ |
| Regras de notificações definidas | ✅ |
| Regras de keyboard definidas | ✅ |
| Total: 25 regras | ✅ |
