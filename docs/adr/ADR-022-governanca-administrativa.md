# ADR-022: Governança Administrativa da Competência

**Data:** 2026-06-27
**Status:** Accepted
**Decisor:** Arquiteto de Domínio
**Sprint:** 9.5

## Contexto

A Sprint 9 implementou o PayrollCompetency como Aggregate Root que representa oficialmente uma competência financeira, com lifecycle de 7 estados, versionamento, selo imutável e trilha de auditoria.

**Problema:** Não existe um processo administrativo que valide, aprove e encerre oficialmente uma competência financeira. Uma competência calculada não significa uma competência aprovada.

## Decisão

Criar uma **cadeia de validação obrigatória e progressiva** para o encerramento administrativo da competência.

### Pergunta Fundamental

> "Como garantir que uma competência financeira só possa ser encerrada quando todos os requisitos administrativos, operacionais e de auditoria estiverem satisfeitos, preservando rastreabilidade completa para futuras inspeções?"

### Resposta

Através de cinco componentes que formam a cadeia de governança:

1. **PayrollReadiness** — Validação automatizada de pré-requisitos
2. **ApprovalChecklist** — Checklist completo e verificável
3. **AdministrativeApproval** — Registro formal do ato de aprovação
4. **AdministrativeLock** — Congelamento administrativo
5. **ApprovalSnapshot** — Fotografia do estado completo na aprovação

---

## Fluxo Administrativo

```
Competência Calculada
        ↓
PayrollReadiness (validação automatizada)
        ↓
ApprovalChecklist (checklist completo)
        ↓
AdministrativeApproval (ato formal)
        ↓
AdministrativeLock (congelamento)
        ↓
ApprovalSnapshot (fotografia final)
        ↓
Competência Oficialmente Encerrada
```

---

## PayrollReadiness

Componente de validação que não altera estado. Verifica:

- Competência calculada (estado `calculated` ou `reviewed`)
- Versão válida (ao menos uma versão)
- Snapshot financeiro presente
- Resultado de remuneração presente
- Sem inconsistências críticas
- Trail de auditoria presente
- Explicação presente

Retorna resultado binário: `ready` ou `not_ready` com lista de pendências.

---

## ApprovalChecklist

Lista completa de critérios obrigatórios. Cada item possui:

- **ID** único (ex: CLC-01, SNF-01, REM-01)
- **Descrição** do critério
- **Categoria** (cálculo, snapshot, remuneração, consistência, auditoria, explicação)
- **Status** (pending, satisfied, not_satisfied, waived)
- **Justificativa** (obrigatória para dispensa)
- **Responsável** e timestamp

Checklist completo é pré-requisito para aprovação.

---

## AdministrativeApproval

Registro formal do ato de aprovação. Contém:

- **competency_id** — Identificador da competência
- **year_month** — Período de referência
- **version** — Versão aprovada
- **approved_by** — Responsável pela aprovação
- **approved_at** — Data/hora da aprovação
- **justification** — Justificativa da aprovação
- **observations** — Observações adicionais
- **checklist_version** — Versão do checklist utilizado

Irreversível sem reabertura.

---

## AdministrativeLock

Congelamento administrativo. Após criado:

- Nenhuma alteração administrativa pode ocorrer
- Competência bloqueada não pode ser exportada (exceto via desbloqueio)
- Desbloqueio requer autorização superior (Diretor)

Contém:

- **locked_by** — Responsável pelo bloqueio
- **locked_at** — Data/hora do bloqueio
- **justification** — Justificativa do bloqueio

---

## ApprovalSnapshot

Fotografia do estado completo no momento da aprovação. Congela:

- Versão aprovada
- Usuário responsável
- Timestamp
- Justificativa
- Approval completo
- Lock (se aplicável)
- Checklist utilizado

Imutável após criação.

---

## Lifecycle Expandido

```
draft → calculated → reviewed → approved → locked → exported → paid → archived
```

Novas transições:

- `approved → locked` (lock)
- `locked → approved` (unlock)
- `locked → exported` (export direto)
- Qualquer estado reabrível → `draft` (reopen)

---

## Eventos de Domínio

| Evento | Descrição |
|---|---|
| `payroll.ready.v1` | Readiness validado |
| `payroll.checklist.completed.v1` | Checklist completo |
| `payroll.approval.requested.v1` | Aprovação solicitada |
| `payroll.approved.v1` | Aprovação registrada |
| `payroll.locked.v1` | Competência bloqueada |
| `payroll.unlocked.v1` | Competência desbloqueada |
| `payroll.reopened.v1` | Competência reaberta |

---

## Segregação de Funções

- O usuário que executou o cálculo **não pode** ser o mesmo que aprova
- Desbloqueio requer papel superior ao bloqueador
- Reabertura requer justificativa obrigatória

---

## Decisões Deliberadamente Adiadas

1. Assinatura digital ICP-Brasil
2. Workflow configurável por tipo de competência
3. Aprovação paralela (múltiplos aprovadores)
4. Integração com Active Directory
5. Aprovação por certificado digital
6. Integração com ERP
7. Integração bancária

---

## Referências

- docs/domain/analises/analise-fechamento-administrativo.md
- docs/domain/glossario-governanca.md
- docs/domain/matriz-aprovacao.md
- docs/domain/checklist-fechamento.md
- docs/domain/invariantes-governanca.md
- docs/domain/casos-borda-governanca.md
- ADR-021-competencia-financeira.md
