# Baseline Operacional — v1.0

## Operational Core

| Campo | Valor |
|-------|-------|
| **Status** | FROZEN |
| **Data** | 2026-07-06 |
| **Baseline** | v1.0 |
| **Tag** | v1-operational-core |

---

## Escopo Congelado

A partir desta baseline, os módulos listados abaixo encontram-se congelados (Frozen). Qualquer alteração futura deverá ocorrer exclusivamente para correção de bugs encontrados durante homologação.

### Competências (Periods)

- Criar competência
- Editar competência (status)
- Excluir competência
- Duplicar competência
- Copiar competência
- Fechar/Reabrir competência

### Workspace

- Visualização em grade (Planilha)
- Adicionar médico a turno
- Trocar médico em turno
- Mover médico entre turnos
- Excluir assignment
- Drag and drop
- Controle por teclado
- Undo/Redo

### Turnos (Shifts)

- Criar turno
- Editar turno
- Cancelar turno
- Alterar status (draft → scheduled → in_progress → completed)
- Sincronização com planilha (Workspace)
- 5 tipos por dia: T1, T2, T3, R1, R2

### Médicos (Doctors)

- Criar médico
- Editar médico
- Inativar médico
- Reativar médico

### Financeiro

- Cálculo de remuneração
- Payroll

### Relatórios

- Relatórios operacionais
- Relatórios financeiros

### Dashboard

- KPIs de cobertura
- KPIs financeiros
- KPIs operacionais

---

## O Que Não Pode Mais Sofrer Alteração

| Módulo | Status | Alterações Permitidas |
|--------|--------|----------------------|
| Workspace | Frozen | Bug fix apenas |
| Competências | Frozen | Bug fix apenas |
| Turnos | Frozen | Bug fix apenas |
| Assignments | Frozen | Bug fix apenas |
| Médicos | Frozen | Bug fix apenas |
| Financeiro | Frozen | Bug fix apenas |
| Relatórios | Frozen | Bug fix apenas |
| Dashboard | Frozen | Bug fix apenas |
| Sidebar/Menu | Frozen | Bug fix apenas |
| React Query | Frozen | Bug fix apenas |
| APIs | Frozen | Bug fix apenas |
| Banco de Dados | Frozen | Bug fix apenas |
| Migrations | Frozen | Bug fix apenas |
| Docker | Frozen | Bug fix apenas |
| Seeds | Frozen | Bug fix apenas |
| Runtime | Frozen | Bug fix apenas |

---

## Como Tratar Bugs

Após o congelamento, qualquer correção deverá seguir:

1. **Bug fix apenas** — corrigir o defeito sem alterar comportamento
2. **Sem refatorações** — não reestruturar código existente
3. **Sem mudanças arquiteturais** — não alterar a arquitetura do sistema
4. **Commit com prefixo** — `fix: descrição do bug`
5. **Teste de regressão** — confirmar que a correção não quebrou outras funcionalidades
6. **Nova tag** — `v1-operational-core-fix-N`

---

## Módulos Fora do Escopo (não congelados)

- Autenticação/Authorization (futuro)
- Integração Tasy (futuro)
- Exportação PDF (futuro)
- Importação Legacy (futuro)
