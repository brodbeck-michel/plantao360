# Análise de Negócio — Cobertura Financeira

**Sprint:** 7 — Coverage Engine & Fundação do Domínio Financeiro
**Data:** 2026-06-26
**Status:** Versão 1.0

---

## Pergunta Fundamental

> "Quais fatos operacionais produzem direitos financeiros?"

**Resposta:** Apenas dois fatos operacionais produzem direitos financeiros:

1. **Assignment completado** — médico trabalhou efetivamente no plantão.
2. **Extra aprovado** — médico realizou horas extras devidamente autorizadas.

Nenhum outro fato operacional gera direito financeiro direto.

---

## O que caracteriza que um médico realmente trabalhou?

Um médico é considerado como tendo trabalhado quando sua atribuição (Assignment/ShiftPart) atinge o status `completed`. Este status indica que:

- O médico compareceu ao plantão;
- O plantão foi iniciado e finalizado;
- O intervalo de trabalho (start_time a end_time) foi efetivamente cumprido;
- Não houve cancelamento posterior à conclusão.

**Critério adicional:** O plantão pai (Shift) também deve estar `completed` ou `in_progress`. Um Assignment `completed` em um Shift `cancelled` é uma inconsistência que deve ser detectada pelo Coverage Engine.

---

## O que gera direito financeiro?

| Fato Operacional | Gera Direito? | Condição |
|---|---|---|
| Assignment `completed` | **Sim** | Shift não está `cancelled` |
| Extra `approved` | **Sim** | Extra não está `cancelled` |
| Assignment `confirmed` | **Não** | Apenas confirmação, não trabalho efetivo |
| Assignment `started` | **Não** | Trabalho em andamento, não concluído |
| Assignment `planned` | **Não** | Apenas planejamento |
| Extra `pending` | **Não** | Aguardando aprovação |
| Extra `rejected` | **Não** | Reprovado |
| Shift `scheduled` | **Não** | Apenas agendado |
| Shift `in_progress` | **Não** | Em andamento |

---

## O que não gera direito financeiro?

1. **Assignment cancelado** — revoga qualquer elegibilidade anterior.
2. **Extra rejeitado** — nunca gera direito.
3. **Extra cancelado** — direito revogado.
4. **Assignment planned/confirmed/started** — trabalho não concluído.
5. **Shift cancelled** — todos os Assignments associados perdem elegibilidade.
6. **Extra pending** — aguardando decisão.

---

## Como tratar substituições?

Uma substituição ocorre quando um médico substitui outro em um Assignment.

**Regras:**
- O Assignment original é cancelado (cancelado = sem direito).
- Um novo Assignment é criado para o substituto.
- Apenas o Assignment do substituto que for `completed` gera direito.
- O Coverage Engine deve registrar ambos os fatos: a revogação do original e a criação do novo.

**Invariantes:**
- Não podem existir dois Assignments ativos para o mesmo período sobreposto no mesmo Shift.
- A substituição é registrada como dois eventos distintos: cancelamento + criação.

---

## Como tratar plantões parcialmente cumpridos?

Um plantão parcialmente cumprido ocorre quando:
- O Assignment foi `started` mas não `completed`;
- O médico saiu antes do horário previsto;
- Houve interrupção durante o plantão.

**Tratamento:**
- Assignment `started` mas não `completed` → **não gera direito financeiro**.
- Apenas Assignments `completed` geram direito.
- O Coverage Engine deve detectar e registrar inconsistências de AssignmentsStarted mas nãoCompleted.

**Justificativa:** O sistema registra fatos, não interpreta meios. Se o médico não completou, não há como determinar o tempo efetivamente trabalhado a partir dos dados disponíveis.

---

## Como tratar cancelamentos?

### Cancelamento de Assignment
- Status → `cancelled`
- **Revoga imediatamente** qualquer direito financeiro associado.
- O Coverage Engine exclui o Assignment da consolidação.
- Se havia um Extra aprovado associado, este continua válido ( Extra é independente do Assignment).

### Cancelamento de Shift
- Status → `cancelled`
- **Revoga todos os direitos** dos Assignments associados.
- Extras aprovados associados continuam válidos (dependem do Shift, não do Assignment).
- O Coverage Engine marca todos os Assignments do Shift como inconsistentes.

### Cancelamento de Extra
- Status → `cancelled`
- **Revoga o direito** do Extra.
- Não afeta Assignments.

---

## Como tratar extras aprovados e rejeitados?

### Extra Aprovado (`approved`)
- Gera direito financeiro.
- O Coverage Engine inclui o Extra na consolidação.
- O direito é registrado como `extra` com duração em minutos.

### Extra Rejeitado (`rejected`)
- **Nunca** gera direito financeiro.
- O Coverage Engine exclui o Extra da consolidação.
- Não pode ser reavaliado posteriormente (estado terminal).

### Extra Pendente (`pending`)
- **Não gera direito** enquanto estiver pendente.
- O Coverage Engine deve registrar que existem Extras pendentes de decisão.
- Quando aprovado → gera direito retroativo à data de criação.

---

## Como tratar correções retroativas?

Correções retroativas ocorrem quando:
- Um Assignment `completed` é alterado para `cancelled` após o fechamento da competência;
- Um Extra `approved` é alterado para `rejected` após consolidação.

**Tratamento:**
- O sistema permite correções, mas o Coverage Engine deve ser **re-executado** para a competência.
- A re-execução gera um novo SnapshotFinanceiro substituindo o anterior.
- O evento `financial.fact.revoked` é disparado para cada direito revogado.
- A competência deve estar `draft` para permitir reconsolidação.

**Invariantes:**
- Competência `paid` não permite correções.
- Competência `closed` permite correções apenas com reabertura.
- Toda correção gera novo SnapshotFinanceiro.

---

## Como tratar reabertura de competência?

Reabertura occurs when a closed period is reopened.

**Tratamento:**
- O status do Period retorna para `draft`.
- Todos os SnapshotsFinanceiros anteriores são invalidados.
- O Coverage Engine deve ser re-executado para recalcular toda a cobertura.
- O evento `period.reopened.v1` é disparado.
- Após reconsolidação, o Period pode ser fechado novamente.

**Invariantes:**
- Competência `paid` não pode ser reaberta.
- Reabertura invalida todos os snapshots anteriores.
- Após reabertura, o fechamento anterior é desconsiderado.

---

## Fluxo de Consolidação

```
1. Operação                    →  Evento
2. Evento                      →  Coverage Engine
3. Coverage Engine              →  CoverageSnapshot
4. CoverageSnapshot             →  FinancialSnapshot
5. FinancialSnapshot            →  Payroll (Sprint 8)
```

O Coverage Engine é o **ponte** entre o domínio operacional e o domínio financeiro.

---

## Decisões Deliberadas

| Decisão | Justificativa |
|---|---|
| Apenas `completed` gera direito | Fato confirmado, não planejado |
| Extra `pending` não gera direito | Aguardando decisão formal |
| Cancelamento revoga retroativamente | Direito depende de status final |
| Competência `paid` é imutável | Proteção contra fraudes |
| Reabertura invalida snapshots | Recálculo completo necessário |
| Coverage Engine não calcula valores | Separação de responsabilidades |
