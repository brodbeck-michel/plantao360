# User Journeys — Plantão 360

**Sprint:** 10.5 — Domain Freeze, Application Baseline & Integration Architecture
**Data:** 2026-06-27

---

## Visão Geral

Os User Journeys documentam os fluxos principais de uso do Plantão 360.

---

## 1. Journey: Gerenciar Médicos

### Fluxo Principal

```
1. Usuário acessa lista de médicos
2. Usuário clica em "Novo Médico"
3. Usuário preenche dados (nome, especialidade, CRM, email)
4. Sistema valida dados
5. Sistema cria médico
6. Sistema confirma criação
7. Usuário vê médico na lista
```

### Fluxos Alternativos

| Fluxo | Condição | Ação |
|---|---|---|
| Dados inválidos | Validação falha | Exibir erros |
| CRM duplicado | CRM já existe | Exibir aviso |
| Médico inativo | Médico desativado | Exibir status |

### Telas

| Tela | Descrição |
|---|---|
| `DoctorList` | Lista de médicos com filtros |
| `DoctorDetail` | Detalhes do médico |
| `DoctorForm` | Formulário de criação/edição |

---

## 2. Journey: Gerenciar Períodos

### Fluxo Principal

```
1. Usuário acessa lista de períodos
2. Usuário clica em "Novo Período"
3. Usuário preenche dados (nome, data início, data fim, tipo)
4. Sistema valida dados
5. Sistema cria período
6. Sistema confirma criação
7. Usuário vê período na lista
```

### Fluxos Alternativos

| Fluxo | Condição | Ação |
|---|---|---|
| Período sobreposto | Conflito de datas | Exibir aviso |
| Data inválida | Início > Fim | Exibir erro |
| Período fechado | Não pode editar | Exibir status |

### Telas

| Tela | Descrição |
|---|---|
| `PeriodList` | Lista de períodos |
| `PeriodDetail` | Detalhes do período |
| `PeriodForm` | Formulário de criação/edição |

---

## 3. Journey: Gerenciar Plantões

### Fluxo Principal

```
1. Usuário acessa lista de plantões
2. Usuário clica em "Novo Plantão"
3. Usuário seleciona período e médico
4. Usuário preenche dados (data, tipo, horário)
5. Sistema valida dados
6. Sistema cria plantão
7. Sistema confirma criação
8. Usuário vê plantão na lista
```

### Fluxos Alternativos

| Fluxo | Condição | Ação |
|---|---|---|
| Plantão duplicado | Médico já atribuído | Exibir aviso |
| Horário conflitante | Conflito de horário | Exibir erro |
| Plantão cancelado | Pode reatribuir | Exibir status |

### Telas

| Tela | Descrição |
|---|---|
| `ShiftList` | Lista de plantões |
| `ShiftDetail` | Detalhes do plantão |
| `ShiftForm` | Formulário de criação/edição |

---

## 4. Journey: Gerenciar Atribuições

### Fluxo Principal

```
1. Usuário acessa lista de atribuições
2. Usuário clica em "Nova Atribuição"
3. Usuário seleciona plantão e médico
4. Usuário seleciona tipo de atribuição
5. Sistema valida dados
6. Sistema cria atribuição
7. Sistema confirma criação
8. Usuário vê atribuição na lista
```

### Fluxos Alternativos

| Fluxo | Condição | Ação |
|---|---|---|
| Atribuição duplicada | Médico já atribuído | Exibir aviso |
| Plantão lotado | Sem vagas | Exibir erro |
| Atribuição cancelada | Pode reatribuir | Exibir status |

### Telas

| Tela | Descrição |
|---|---|
| `AssignmentList` | Lista de atribuições |
| `AssignmentDetail` | Detalhes da atribuição |
| `AssignmentForm` | Formulário de criação/edição |

---

## 5. Journey: Gerenciar Coberturas

### Fluxo Principal

```
1. Usuário acessa lista de coberturas
2. Usuário clica em "Nova Cobertura"
3. Usuário seleciona plantão
4. Usuário preenche dados (tipo, motivo)
5. Sistema valida dados
6. Sistema cria cobertura
7. Sistema confirma criação
8. Usuário vê cobertura na lista
```

### Fluxos Alternativos

| Fluxo | Condição | Ação |
|---|---|---|
| Cobertura aprovada | Status atualizado | Exibir confirmação |
| Cobertura rejeitada | Motivo registrado | Exibir motivo |
| Cobertura pendente | Aguardando aprovação | Exibir status |

### Telas

| Tela | Descrição |
|---|---|
| `CoverageList` | Lista de coberturas |
| `CoverageDetail` | Detalhes da cobertura |
| `CoverageForm` | Formulário de criação/edição |

---

## 6. Journey: Gerenciar Payroll

### Fluxo Principal

```
1. Usuário acessa lista de competências
2. Usuário clica em "Nova Competência"
3. Usuário seleciona período
4. Usuário preenche dados (competência)
5. Sistema valida dados
6. Sistema cria competência
7. Sistema confirma criação
8. Usuário vê competência na lista
```

### Fluxos Alternativos

| Fluxo | Condição | Ação |
|---|---|---|
| Competência aprovada | Checklist preenchido | Exibir confirmação |
| Competência rejeitada | Motivo registrado | Exibir motivo |
| Competência processando | Em andamento | Exibir progresso |
| Competência bloqueada | Trava administrativa | Exibir status |

### Telas

| Tela | Descrição |
|---|---|
| `PayrollList` | Lista de competências |
| `PayrollDetail` | Detalhes da competência |
| `PayrollForm` | Formulário de criação/edição |
| `PayrollApproval` | Formulário de aprovação |

---

## 7. Journey: Visualizar Analytics

### Fluxo Principal

```
1. Usuário acessa dashboard de analytics
2. Usuário seleciona período
3. Sistema carrega dados
4. Usuário visualiza KPIs
5. Usuário visualiza gráficos
6. Usuário exporta relatório
```

### Fluxos Alternativos

| Fluxo | Condição | Ação |
|---|---|---|
| Sem dados | Período vazio | Exibir mensagem |
| Dados parciais | Dados incompletos | Exibir aviso |
| Erro de carregamento | Falha na consulta | Exibir erro |

### Telas

| Tela | Descrição |
|---|---|
| `AnalyticsDashboard` | Dashboard principal |
| `KPIs` | Indicadores chave |
| `Reports` | Relatórios disponíveis |
| `Timeline` | Timeline da instituição |

---

## Validação

| Critério | Status |
|---|---|
| Todas as journeys documentadas | ✅ |
| Fluxos principais definidos | ✅ |
| Fluxos alternativos definidos | ✅ |
| Telas documentadas | ✅ |
