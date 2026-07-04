# Mapa de Navegação — Plantão 360

**Sprint:** 11 — Product Design, User Experience Modeling & Frontend Functional Specification
**Data:** 2026-06-27

---

## 1. Menu Lateral

### Estrutura

```
├── Dashboard
├── Operacional
│   ├── Períodos
│   ├── Plantões
│   ├── Atribuições
│   ├── Cobertura
│   └── Extras
├── Gestão de Pessoal
│   └── Médicos
├── Financeiro
│   ├── Payroll
│   └── Readiness
├── Analytics
│   ├── Dashboard
│   ├── Timeline
│   └── Relatórios
└── Configurações
    └── (futuro)
```

### Regras de Exibição

| Itens | Coordenador | Médico | Financeiro | RH | Auditor | Admin | Diretor |
|---|---|---|---|---|---|---|---|
| Dashboard | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Períodos | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Plantões | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Atribuições | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Cobertura | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Extras | ✅ | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Médicos | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| Payroll | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Readiness | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ | ❌ |
| Analytics | ✅ | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ |
| Timeline | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Relatórios | ❌ | ❌ | ✅ | ❌ | ✅ | ✅ | ✅ |

---

## 2. Breadcrumbs

### Padrão

```
Dashboard > Módulo > Tela Atual
```

### Exemplos

| Tela | Breadcrumb |
|---|---|
| Dashboard | `Dashboard` |
| Lista de Médicos | `Dashboard > Médicos` |
| Detalhe do Médico | `Dashboard > Médicos > Dr. Carlos` |
| Formulário do Médico | `Dashboard > Médicos > Novo Médico` |
| Lista de Períodos | `Dashboard > Períodos` |
| Detalhe do Período | `Dashboard > Períodos > Junho 2026` |
| Lista de Plantões | `Dashboard > Plantões` |
| Calendário de Plantões | `Dashboard > Plantões > Calendário` |
| Lista de Payroll | `Dashboard > Payroll` |
| Detalhe do Payroll | `Dashboard > Payroll > Competência 06/2026` |
| Aprovação do Payroll | `Dashboard > Payroll > Competência 06/2026 > Aprovar` |
| Dashboard Analytics | `Dashboard > Analytics` |
| Timeline | `Dashboard > Analytics > Timeline` |
| Relatórios | `Dashboard > Analytics > Relatórios` |

---

## 3. Atalhos

### Atalhos Globais

| Atalho | Ação | Disponível para |
|---|---|---|
| `Ctrl + K` | Busca global | Todas |
| `Ctrl + N` | Nova notificação | Todas |
| `Ctrl + D` | Dashboard | Todas |
| `Esc` | Fechar modal/dialog | Todas |

### Atalhos por Módulo

| Módulo | Atalho | Ação |
|---|---|---|
| Plantões | `Ctrl + Shift + N` | Novo plantão |
| Médicos | `Ctrl + Shift + M` | Novo médico |
| Payroll | `Ctrl + Shift + P` | Nova competência |
| Cobertura | `Ctrl + Shift + C` | Nova cobertura |

---

## 4. Deep Links

### Padrão

```
/app/{modulo}/{recurso}/{id}
```

### Exemplos

| Tela | Deep Link |
|---|---|
| Dashboard | `/app/dashboard` |
| Lista de Médicos | `/app/doctors` |
| Detalhe do Médico | `/app/doctors/{id}` |
| Formulário do Médico | `/app/doctors/new` |
| Lista de Períodos | `/app/periods` |
| Detalhe do Período | `/app/periods/{id}` |
| Lista de Plantões | `/app/shifts` |
| Calendário | `/app/shifts/calendar` |
| Detalhe do Plantão | `/app/shifts/{id}` |
| Lista de Atribuições | `/app/assignments` |
| Detalhe da Atribuição | `/app/assignments/{id}` |
| Lista de Cobertura | `/app/coverage` |
| Detalhe da Cobertura | `/app/coverage/{id}` |
| Lista de Extras | `/app/extras` |
| Detalhe do Extra | `/app/extras/{id}` |
| Lista de Payroll | `/app/payroll` |
| Detalhe do Payroll | `/app/payroll/{id}` |
| Aprovação do Payroll | `/app/payroll/{id}/approve` |
| Readiness | `/app/readiness` |
| Analytics | `/app/analytics` |
| Timeline | `/app/analytics/timeline` |
| Relatórios | `/app/analytics/reports` |

---

## 5. Navegação Contextual

### Ações Contextuais por Tela

| Tela | Ações Contextuais |
|---|---|
| DoctorList | Novo Médico, Exportar |
| DoctorDetail | Editar, Desativar, Histórico |
| DoctorForm | Salvar, Cancelar |
| PeriodList | Novo Período, Exportar |
| PeriodDetail | Editar, Fechar, Reabrir, Histórico |
| PeriodForm | Salvar, Cancelar |
| ShiftList | Novo Plantão, Calendário, Exportar |
| ShiftDetail | Editar, Cancelar, Histórico |
| ShiftForm | Salvar, Cancelar |
| ShiftCalendar | Novo Plantão, Filtros |
| AssignmentList | Nova Atribuição, Exportar |
| AssignmentDetail | Editar, Cancelar, Histórico |
| AssignmentForm | Salvar, Cancelar |
| CoverageList | Nova Cobertura, Exportar |
| CoverageDetail | Aprovar, Rejeitar, Histórico |
| CoverageForm | Salvar, Cancelar |
| ExtraList | Novo Extra, Exportar |
| ExtraDetail | Editar, Cancelar, Histórico |
| ExtraForm | Salvar, Cancelar |
| PayrollList | Nova Competência, Exportar |
| PayrollDetail | Editar, Aprovar, Rejeitar, Processar, Bloquear |
| PayrollForm | Salvar, Cancelar |
| PayrollApproval | Aprovar, Rejeitar, Cancelar |
| AnalyticsDashboard | Filtros, Exportar |
| Timeline | Filtros, Exportar |
| Reports | Gerar, Exportar |
| Readiness | Verificar, Atualizar |

---

## 6. Navegação entre Módulos

### Fluxos de Navegação

```
Dashboard → Qualquer módulo
Qualquer módulo → Dashboard
Módulo → Detalhe → Formulário
Módulo → Detalhe → Ação contextual
Payroll → Readiness
Payroll → Analytics
Analytics → Timeline
Analytics → Relatórios
```

### Regras de Volta

| Contexto | Ação de Volta |
|---|---|
| Lista → Detalhe | Voltar para Lista |
| Detalhe → Formulário | Voltar para Detalhe |
| Formulário → Salvar | Voltar para Lista |
| Formulário → Cancelar | Voltar para Formulário anterior |
| Ação contextual | Voltar para Tela anterior |

---

## Validação

| Critério | Status |
|---|---|
| Menu lateral estruturado | ✅ |
| Breadcrumbs definidos | ✅ |
| Atalhos documentados | ✅ |
| Deep links definidos | ✅ |
| Navegação contextual mapeada | ✅ |
| Regras de volta definidas | ✅ |
