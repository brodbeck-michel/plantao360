# Release Notes — v1-operational-core

## Resumo Executivo

O Plantão360 atinge a versão v1-operational-core, marcando o congelamento do core operacional. Todos os módulos fundamentais estão prontos para homologação.

---

## Funcionalidades Prontas

### Competências
- Criar competência com geração automática de turnos (5 tipos/dia)
- Editar status (draft → closed → paid)
- Excluir competência sem assignments
- Duplicar competência existente
- Copiar competência para novo período
- Fechar/Reabrir competência

### Workspace (Planilha)
- Visualização em grade: dias × tipos de turno
- Adicionar médico a turno vago
- Trocar médico em turno ocupado
- Mover médico entre turnos
- Excluir assignment
- Drag and drop entre células
- Controle por teclado (setas, Enter, Escape)
- Undo/Redo (Ctrl+Z, Ctrl+Y)
- Indicadores visuais de status

### Turnos
- 5 tipos: T1 (07:00-19:00), T2 (19:00-07:00), T3 (07:00-07:00), R1 (09:00-15:00), R2 (15:00-21:00)
- Sincronização com Workspace
- Status: draft → scheduled → in_progress → completed → cancelled
- Validação de data dentro da competência
- Edição de campos
- Cancelamento

### Médicos
- Criar médico com dados completos (nome, CRM, especialidade, telefone, email)
- Editar informações
- Inativar/Reativar
- Taxa horária configurável

### Financeiro
- Cálculo de remuneração por médico
- Payroll por competência

### Relatórios
- Relatórios operacionais
- Relatórios financeiros

### Dashboard
- KPIs de cobertura
- KPIs financeiros
- KPIs operacionais

---

## Funcionalidades Escondidas (MVP Mode)

- Sidebar reduzida (VITE_MVP_MODE=true)
- Autenticação desativada (ENABLE_JWT=false)
- Audit log desativado (ENABLE_AUDIT_LOG=false)
- Integração Tasy desativada (ENABLE_TASY_INTEGRATION=false)
- Exportação PDF desativada (ENABLE_EXPORT_PDF=false)
- Importação Legacy desativada (ENABLE_IMPORT_LEGACY=false)

---

## Escopo MVP

| Módulo | Status | Notas |
|--------|--------|-------|
| Competências | Pronto | CRUD completo |
| Workspace | Pronto | Grade interativa |
| Turnos | Pronto | 5 tipos, sincronizado |
| Médicos | Pronto | CRUD completo |
| Financeiro | Pronto | Cálculo básico |
| Relatórios | Pronto | Básicos |
| Dashboard | Pronto | KPIs essenciais |

---

## Limitações Conhecidas

1. **Banco SQLite** — não suporta concorrência simultânea
2. **Seed gera 1-2 tipos/dia** — não todos os 5 tipos
3. **Períodos 7+** — precisam de normalização manual ou script
4. **Sem autenticação** —任何人 pode acessar
5. **Sem auditoria** — ações não são registradas
6. **Sem testes automatizados** — validação manual
7. **Docker dev** — volume de dados mapeado para `/app/data`

---

## Bugs Corrigidos nesta Release

### Sprint 18.1
- Seed gerava turnos com datas de calendário (01-30) em vez de competência (26→25)

### Sprint 18.2
- `Shift` model faltava `aggregate_id`, `before_transition`, `after_transition`
- Período 6 tinha apenas 41 shifts (faltavam R1/R2)
- Workspace mostrava "Turno não encontrado" para células sem shift

### Sprint 18.3
- Períodos 1-5 tinham apenas T1/T2/T3 (sem R1/R2)

### Infraestrutura
- DB SQLite não persistia entre rebuilds do Docker
- `seed_data(clear=True)` limpava DB a cada restart
- WatchFiles reiniciava backend ao detectar scripts em `/app/scripts/`
