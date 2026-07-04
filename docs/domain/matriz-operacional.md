# Matriz Operacional

**Sprint:** 7
**Data:** 2026-06-26

---

## Definição

Relaciona as responsabilidades de cada setor/ator no ciclo de vida dos fatos operacionais e financeiros.

---

## Setores e Responsabilidades

### Coordenação de Plantão

| Atividade | Responsabilidade | Ocorrência |
|---|---|---|
| Criar plantão | Criar Shift | Antes do período |
| Atribuir médico | Criar Assignment | Antes do período |
| Confirmar atribuição | Confirmar Assignment | Quando médico aceita |
| Iniciar plantão | Atualizar status Shift/Assignment | No momento do plantão |
| Finalizar plantão | Completar Shift/Assignment | Ao término do plantão |
| Cancelar atribuição | Cancelar Assignment | Quando necessário |
| Registrar extra | Criar Extra | Quando médico trabalha além |
| Aprovar/rejeitar extra | Atualizar Extra status | Quando necessário |
| Detectar inconsistências | Reportar ao Coverage Engine | Durante consolidação |

### Financeiro

| Atividade | Responsabilidade | Ocorrência |
|---|---|---|
| Consolidar cobertura | Executar Coverage Engine | Ao fechar competência |
| Gerar snapshots | Criar CoverageSnapshot/FinancialSnapshot | Ao fechar competência |
| Revisar direitos | Validar FinancialSnapshot | Antes de fechar |
| Fechar competência | Alterar Period status | Mensalmente |
| Reabrir competência | Alterar Period status | Quando necessário |
| Preparar folha | Consumir FinancialSnapshot | Sprint 8 |

### Auditoria

| Atividade | Responsabilidade | Ocorrência |
|---|---|---|
| Rastrear eventos | Registrar logs de auditoria | Sempre |
| Verificar consistência | Validar invariantes | Durante consolidação |
| Detectar fraudes | Analisar padrões | Periodicamente |
| validar regras | Verificar compliance | Durante consolidação |

### RH

| Atividade | Responsabilidade | Ocorrência |
|---|---|---|
| Cadastrar médico | Criar/atualizar Doctor | Quando necessário |
| Gerenciar ativos | Ativar/desativar Doctor | Quando necessário |
| Validar CRM | Verificar registro médico | No cadastro |

### Administração

| Atividade | Responsabilidade | Ocorrência |
|---|---|---|
| Definir política | Configurar regras | Antes do período |
| Aprovar exceções | Decidir sobre casos especiais | Quando necessário |
| Revisar relatórios | Analisar consolidados | Mensalmente |

---

## Fluxo de Responsabilidade

```
1. Coordenação cria plantão e atribui médicos
         │
2. Médicos trabalham (Assignment started → completed)
         │
3. Coordenação registra extras quando necessário
         │
4. Ao fim do mês, Coordenação fecha competência
         │
5. Financeiro executa Coverage Engine
         │
6. Coverage Engine gera CoverageSnapshot
         │
7. Coverage Engine gera FinancialSnapshot
         │
8. Auditoria valida consistência
         │
9. Financeiro fecha competência
         │
10. Payroll consome FinancialSnapshot (Sprint 8)
```

---

## Matriz de Acesso

| Entidade | Coordenação | Financeiro | Auditoria | RH | Admin |
|---|---|---|---|---|---|
| Doctor | CRUD | Leitura | Leitura | CRUD | Leitura |
| Period | Leitura | CRUD | Leitura | Leitura | Leitura |
| Shift | CRUD | Leitura | Leitura | Leitura | Leitura |
| Assignment | CRUD | Leitura | Leitura | Leitura | Leitura |
| Extra | CRUD + Aprovação | Leitura | Leitura | Leitura | Leitura |
| CoverageSnapshot | Leitura | CRUD | Leitura | Leitura | Leitura |
| FinancialSnapshot | Leitura | CRUD | Leitura | Leitura | Leitura |
