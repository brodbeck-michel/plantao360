# Matriz de Aprovação — Governança Administrativa

**Sprint:** 9.5 — Competência Administrativa & Governança Financeira
**Data:** 2026-06-27

---

## Visão Geral

A matriz de aprovação define quem pode executar cada ação administrativa, quais pré-requisitos são exigidos e quais evidências devem ser preservadas.

---

## Ações Administrativas

### 1. Validar Competência (PayrollReadiness)

| Campo | Descrição |
|---|---|
| **Ação** | Validar se a competência está apta para fechamento |
| **Papel Responsible** | Qualquer usuário com acesso ao sistema |
| **Permissões** | Leitura |
| **Pré-requisitos** | Competência em estado `calculated` ou `reviewed` |
| **Pós-condições** | Resultado da validação registrado (ready/not ready) |
| **Evidências Obrigatórias** | Lista de pendências (se houver) |
| **Evento** | `payroll.ready.v1` |

### 2. Preencher Checklist (ApprovalChecklist)

| Campo | Descrição |
|---|---|
| **Ação** | Preencher o checklist de fechamento |
| **Papel Responsible** | Gestor de Escala, Administrador Financeiro, Diretor |
| **Permissões** | Escrita |
| **Pré-requisitos** | Competência em estado `calculated` ou `reviewed` |
| **Pós-condições** | Checklist registrado com status de cada item |
| **Evidências Obrigatórias** | Checklist completo com justificativas |
| **Evento** | `payroll.checklist.completed.v1` |

### 3. Solicitar Aprovação (Approval Request)

| Campo | Descrição |
|---|---|
| **Ação** | Solicitar aprovação formal da competência |
| **Papel Responsible** | Gestor de Escala, Administrador Financeiro |
| **Permissões** | Escrita |
| **Pré-requisitos** | PayrollReadiness = ready, Checklist completo |
| **Pós-condições** | Solicitação de aprovação registrada |
| **Evidências Obrigatórias** | Readiness + Checklist |
| **Evento** | `payroll.approval.requested.v1` |

### 4. Aprovar Competência (AdministrativeApproval)

| Campo | Descrição |
|---|---|
| **Ação** | Aprovar formalmente a competência |
| **Papel Responsible** | Administrador Financeiro, Diretor |
| **Permissões** | Aprovação |
| **Pré-requisitos** | Solicitação de aprovação registrada, Checklist completo, Segregação de funções (aprovador ≠ calculador) |
| **Pós-condições** | Competência aprovada, Selo criado, ApprovalSnapshot registrado |
| **Evidências Obrigatórias** | ApprovalSnapshot, PayrollSeal, AuditTrail |
| **Evento** | `payroll.approved.v1` |

### 5. Bloquear Competência (AdministrativeLock)

| Campo | Descrição |
|---|---|
| **Ação** | Bloquear administrativamente a competência |
| **Papel Responsible** | Administrador Financeiro, Diretor |
| **Permissões** | Bloqueio |
| **Pré-requisitos** | Competência aprovada |
| **Pós-condições** | Competência bloqueada, nenhuma alteração administrativa permitida |
| **Evidências Obrigatórias** | AdministrativeLock com responsável e justificativa |
| **Evento** | `payroll.locked.v1` |

### 6. Desbloquear Competência (AdministrativeUnlock)

| Campo | Descrição |
|---|---|
| **Ação** | Remover bloqueio administrativo |
| **Papel Responsible** | Diretor (apenas) |
| **Permissões** | Desbloqueio superior |
| **Pré-requisitos** | Competência bloqueada, Justificativa documentada |
| **Pós-condições** | Competência desbloqueada |
| **Evidências Obrigatórias** | Justificativa + Registro de desbloqueio |
| **Evento** | `payroll.unlocked.v1` |

### 7. Reabrir Competência (Reopen)

| Campo | Descrição |
|---|---|
| **Ação** | Reabrir competência aprovada |
| **Papel Responsible** | Administrador Financeiro, Diretor, Auditor |
| **Permissões** | Reabertura |
| **Pré-requisitos** | Competência em estado `calculated`, `reviewed`, `approved`, `exported` ou `paid`, Justificativa obrigatória |
| **Pós-condições** | Competência em `draft`, nova versão, selo anterior invalidado |
| **Evidências Obrigatórias** | Justificativa + Registro de reabertura |
| **Evento** | `payroll.reopened.v1` |

---

## Matriz de Permissões por Papel

| Papel | Validar | Checklist | Solicitar | Aprovar | Bloquear | Desbloquear | Reabrir |
|---|---|---|---|---|---|---|---|
| Gestor de Escala | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Administrador Financeiro | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ |
| Diretor | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Auditor | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## Segregação de Funções

| Regra | Descrição |
|---|---|
| **SR-01** | O usuário que executou o cálculo não pode ser o mesmo que aprova |
| **SR-02** | O usuário que preencheu o checklist não pode ser o único aprovador |
| **SR-03** | Desbloqueio requer autorização superior ao bloqueador |

---

## Pré-requisitos Detalhados

### Para Aprovação:
1. PayrollReadiness = ready (todos os itens atendidos)
2. ApprovalChecklist = completo (todos os itens marcados)
3. Segregação de funções verificada
4. Responsável pela aprovação identificado
5. Justificativa registrada (se aplicável)

### Para Bloqueio:
1. Competência aprovada
2. Responsável pelo bloqueio identificado
3. Justificativa registrada

### Para Reabertura:
1. Competência em estado reabrível
2. Justificativa obrigatória (mínimo 10 caracteres)
3. Responsável pela reabertura identificado

---

## Pós-condições

### Após Aprovação:
- PayrollSeal criado e imutável
- ApprovalSnapshot registrado
- AuditTrail atualizado
- Evento `payroll.approved.v1` emitido

### Após Bloqueio:
- Nenhuma alteração administrativa permitida
- AdministrativeLock registrado
- Evento `payroll.locked.v1` emitido

### Após Reabertura:
- Competência em estado `draft`
- Nova versão criada
- Selo anterior invalidado
- Evento `payroll.reopened.v1` emitido

---

## Evidências Obrigatórias por Ação

| Ação | Evidências |
|---|---|
| Validação | Lista de pendências |
| Checklist | Checklist completo com justificativas |
| Solicitação | Readiness + Checklist |
| Aprovação | ApprovalSnapshot + PayrollSeal + AuditTrail |
| Bloqueio | AdministrativeLock + responsável + justificativa |
| Desbloqueio | Justificativa + registro de desbloqueio |
| Reabertura | Justificativa + registro de reabertura |
