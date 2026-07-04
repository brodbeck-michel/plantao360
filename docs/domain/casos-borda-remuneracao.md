# Casos de Borda — Remuneração

**Sprint:** 8
**Data:** 2026-06-26

---

## CB-01: Mudança de Tabela

**Cenário:** Uma nova tabela de valores entra em vigor no meio do mês.

**Exemplo:** De 01/01 a 15/01 valor = R$ 150/h. De 16/01 a 31/01 valor = R$ 170/h.

**Decisão:** Cada FinancialFact é avaliado pela regra vigente na data do fato. O PricingPolicy busca a regra com `valid_from <= fact_date` e `valid_until > fact_date`.

**Resultado:** Fatos do dia 1-15 usam regra antiga; fats do dia 16-31 usam regra nova.

---

## CB-02: Tabela Retroativa

**Cenário:** Uma nova tabela é definida com vigência retroativa (ex: aprovada em fevereiro com vigência de janeiro).

**Decisão:** O PricingPolicy utiliza a data do fato (`source_event` data), não a data de cálculo. Regras retroativas são aplicadas normalmente.

**Resultado:** Fatos anteriores são recalculados com a nova regra quando a competência é reaberta.

---

## CB-03: Extra Cancelado Após Cálculo

**Cenário:** Um Extra foi aprovado, calculado, e depois cancelado.

**Decisão:** O FinancialFact do Extra é revogado (`status=revoked`). O RemuneraçãoEngine deve ser re-executado para a competência. O resultado anterior é invalidado.

**Resultado:** Novo RemuneraçãoResult é gerado sem o fato revogado.

---

## CB-04: Reabertura de Competência

**Cenário:** Uma competência fechada e paga precisa ser reaberta para correção.

**Decisão:** Apenas competências com status `closed` podem ser reabertas. Competências `paid` requerem processo manual. Ao reabrir, todos os RemunerationResults são invalidados.

**Resultado:** O Coverage Engine e o Remuneration Engine são re-executados.

---

## CB-05: Médico Desligado

**Cenário:** Um médico foi desativado após ter plantões no mês.

**Decisão:** O FinancialFact já foi criado com o doctor_id válido. O RemuneraçãoEngine processa normalmente. O Payroll pode precisar de tratamento especial para pagamento.

**Resultado:** O cálculo é executado. O pagamento pode exigir processo manual.

---

## CB-06: Plantão Parcial

**Cenário:** Um médico trabalhou 6 horas em um plantão de 12 horas.

**Decisão:** O Coverage Engine já trata isso: apenas Assignments `completed` com `duration_minutes > 0` geram fatos. O RemuneraçãoEngine recebe o fato com a duração real.

**Resultado:** O cálculo utiliza `duration_minutes` do fato, não a duração esperada do plantão.

---

## CB-07: Múltiplos Extras

**Cenário:** Um médico possui 3 extras aprovados no mesmo mês.

**Decisão:** Cada Extra gera um FinancialFact independente. O RemuneraçãoEngine processa cada fato separadamente. O RemuneraçãoResult consolida todos.

**Resultado:** 3 cálculos independentes, somados no resultado final.

---

## CB-08: Múltiplas Tabelas

**Cenário:** A instituição possui tabela para plantões regulares e tabela para extras.

**Decisão:** Cada tipo de fato (`assignment_completion`, `extra_approved`) possui suas próprias regras. O PricingPolicy seleciona a regra correta para cada tipo.

**Resultado:** Regras independentes por tipo de fato.

---

## CB-09: Simulação

**Cenário:** O gestor quer verificar quanto seria o pagamento se a tabela mudasse.

**Decisão:** O RemuneraçãoEngine possui modo simulação. Calcula resultado sem persistir. Nenhum banco é alterado.

**Resultado:** Objeto RemuneraçãoResult em memória, descartado após consulta.

---

## CB-10: Estorno

**Cenário:** Um pagamento precisa ser estornado após faturamento.

**Decisão:** O estorno é um evento financeiro (`financial.fact.revoked.v1`). O RemuneraçãoEngine invalida o resultado anterior e gera novo resultado.

**Resultado:** Novo RemuneraçãoResult com fatos revogados excluídos.

---

## Resumo

| ID | Caso | Tratamento |
|---|---|---|
| CB-01 | Mudança de tabela | Regra vigente por data do fato |
| CB-02 | Tabela retroativa | Aplicada na reabertura |
| CB-03 | Extra cancelado após cálculo | Re-execução do Engine |
| CB-04 | Reabertura de competência | Invalidação + re-execução |
| CB-05 | Médico desligado | Cálculo normal, pagamento manual |
| CB-06 | Plantão parcial | Duração real do fato |
| CB-07 | Múltiplos extras | Fatos independentes |
| CB-08 | Múltiplas tabelas | Regras por tipo de fato |
| CB-09 | Simulação | Modo sem persistência |
| CB-10 | Estorno | Invalidação + novo resultado |
