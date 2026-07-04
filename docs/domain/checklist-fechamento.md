# Checklist de Fechamento — Governança Administrativa

**Sprint:** 9.5 — Competência Administrativa & Governança Financeira
**Data:** 2026-06-27

---

## Visão Geral

O checklist de fechamento é uma lista completa de critérios obrigatórios que devem ser atendidos antes da aprovação formal de uma competência. Cada item possui identificador, descrição, categoria, status e justificativa.

---

## Itens do Checklist

### Categoria: Cálculo

| ID | Item | Descrição | Obrigatório | Justificativa |
|---|---|---|---|---|
| CLC-01 | Competência calculada | A competência deve estar no estado `calculated` ou `reviewed` | Sim | Estado obrigatório para início do processo administrativo |
| CLC-02 | Versão válida | A competência deve possuir ao menos uma versão | Sim | Toda competência calculada possui versão |
| CLC-03 | Snapshot financeiro presente | O FinancialSnapshot deve estar associado à versão ativa | Sim | Dados de entrada são necessários para validação |
| CLC-04 | Resultado de remuneração presente | O RemunerationResult deve estar associado à versão ativa | Sim | Resultados de cálculo são necessários para validação |

### Categoria: Snapshot Financeiro

| ID | Item | Descrição | Obrigatório | Justificativa |
|---|---|---|---|---|
| SNF-01 | Snapshot íntegro | O FinancialSnapshot não deve estar corrompido | Sim | Dados corrompidos impedem validação |
| SNF-02 | Fatos consistentes | Todos os fatos devem ter tipo, duração e médico válidos | Sim | Fatos inválidos geram remunerações incorretas |
| SNF-03 | Sem fatos órfãos | Todo fato deve estar vinculado a um plantão ou extra válido | Sim | Fatos órfãos indicam inconsistência nos dados |
| SNF-04 | Duração positiva | Todos os fatos devem ter duração > 0 minutos | Sim | Duração zero ou negativa indica erro |

### Categoria: Remuneração

| ID | Item | Descrição | Obrigatório | Justificativa |
|---|---|---|---|---|
| REM-01 | Remunerações válidas | Todos os DoctorRemuneration devem ter cálculos válidos | Sim | Cálculos inválidos geram valores incorretos |
| REM-02 | Sem remunerações órfãs | Toda remuneração deve estar vinculada a um fato financeiro válido | Sim | Remunerações órfãs indicam inconsistência |
| REM-03 | Regras aplicadas válidas | Todas as RemunerationRule aplicadas devem estar válidas no momento | Sim | Regras expiradas geram cálculos incorretos |
| REM-04 | Total consistente | O total da competência deve ser igual à soma dos totais por médico | Sim | Inconsistência total indica erro de cálculo |
| REM-05 | valores positivos | Todos os valores de remuneração devem ser >= 0 | Sim | Valores negativos indicam erro |

### Categoria: Consistência

| ID | Item | Descrição | Obrigatório | Justificativa |
|---|---|---|---|---|
| CON-01 | Sem inconsistências críticas | Nenhuma inconsistência do tipo `critical` pode estar pendente | Sim | Inconsistências críticas impedem fechamento |
| CON-02 | Sem extras pendentes | Todos os extras devem ter sido processados | Sim | Extras pendentes indicam dados incompletos |
| CON-03 | Período consistente | O período da competência deve ser consistente com os dados | Sim | Período inconsistente indica erro de dados |

### Categoria: Auditoria

| ID | Item | Descrição | Obrigatório | Justificativa |
|---|---|---|---|---|
| AUD-01 | Trail completo | O AuditTrail deve conter todas as transições de estado | Sim | Trail incompleto impede rastreabilidade |
| AUD-02 | Timestamps válidos | Todos os timestamps devem ser chronologicamente consistentes | Sim | Timestamps inconsistentes indicam erro |
| AUD-03 | Responsáveis identificados | Todas as ações devem ter responsável identificado | Sim | Ações sem responsável impedem auditoria |

### Categoria: Explicação

| ID | Item | Descrição | Obrigatório | Justificativa |
|---|---|---|---|---|
| EXP-01 | Explicação presente | A PayrollExplanation deve estar associada à versão ativa | Sim | Explicação é necessária para transparência |
| EXP-02 | Steps completos | A explicação deve conter todos os passos de cálculo | Sim | Steps incompletos indicam cálculo parcial |

---

## Itens Opcionais

| ID | Item | Descrição | Obrigatório | Justificativa |
|---|---|---|---|---|
| OPT-01 | Observações gerais | Campo para observações adicionais | Não | Permite registrar informações adicionais |
| OPT-02 | Referências externas | Links para documentos de suporte | Não | Facilita consulta a documentos de suporte |

---

## Status dos Itens

| Status | Descrição |
|---|---|
| `pending` | Item ainda não verificado |
| `satisfied` | Item atendido e verificado |
| `not_satisfied` | Item não atendido (impede fechamento) |
| `waived` | Item dispensado com justificativa |

---

## Regras de Validação

1. **Todos os itens obrigatórios** devem estar com status `satisfied` ou `waived`
2. **Itens dispensados** (`waived`) devem possuir justificativa
3. **Itens não atendidos** (`not_satisfied`) impedem o fechamento
4. **Itens pendentes** (`pending`) impedem o fechamento
5. **Checklist completo** é pré-requisito para aprovação

---

## Processo de Preenchimento

1. **Validação automática:** PayrollReadiness valida itens técnicos automaticamente
2. **Revisão manual:** Responsável revisa e confirma itens manuais
3. **Justificativa:** Itens dispensados devem possuir justificativa
4. **Confirmação:** Responsável confirma conclusão do checklist
5. **Registro:** Checklist é registrado como evidência

---

## Exemplo de Checklist Preenchido

```json
{
  "checklist_id": "chk_202606_001",
  "competency_id": 1,
  "version": 1,
  "created_at": "2026-06-27T10:00:00Z",
  "created_by": "admin@unimed.com",
  "items": [
    {"id": "CLC-01", "status": "satisfied", "justificativa": "Competência em estado calculated"},
    {"id": "CLC-02", "status": "satisfied", "justificativa": "Versão 1 criada"},
    {"id": "SNF-01", "status": "satisfied", "justificativa": "Snapshot íntegro"},
    {"id": "REM-01", "status": "satisfied", "justificativa": "Remunerações válidas"},
    {"id": "CON-01", "status": "satisfied", "justificativa": "Sem inconsistências"},
    {"id": "AUD-01", "status": "satisfied", "justificativa": "Trail completo"},
    {"id": "EXP-01", "status": "satisfied", "justificativa": "Explicação presente"}
  ],
  "total_items": 7,
  "satisfied_items": 7,
  "status": "complete"
}
```
