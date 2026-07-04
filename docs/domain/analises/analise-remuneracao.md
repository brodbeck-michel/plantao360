# Análise de Negócio — Remuneração

**Sprint:** 8 — Remuneration Engine & Payroll Foundation
**Data:** 2026-06-26
**Status:** Versão 1.0

---

## Pergunta Fundamental

> "Como o sistema consegue explicar, passo a passo, por que um determinado médico recebeu exatamente aquele valor?"

**Resposta:** O Remuneration Engine produz um `CalculationExplanation` para cada cálculo. Esta explicação contém: quais fatos foram utilizados, quais regras foram aplicadas, quais etapas foram executadas, quais valores foram obtidos em cada etapa, e qual o total final. A explicação é imutável e auditável.

---

## Como uma instituição remunera plantões?

A remuneração de plantões em hospitais segue um padrão geral:

1. **Valor base por hora** — definido por tabela ou contrato
2. **Tipo de plantão** — pode afetar o multiplicador (noturno, feriado, etc.)
3. **Duração efetiva** — tempo realmente trabalhado
4. **Adicionais** — horas extras, substituições, coberturas

Cada instituição possui suas próprias regras. O sistema deve suportar múltiplas tabelas sem assumir qual é a correta.

---

## Existem tabelas diferentes?

**Sim.** Uma mesma instituição pode possuir:
- Tabela para plantões regulares
- Tabela para horas extras
- Tabela para feriados
- Tabela para substituições

O sistema deve permitir múltiplas regras com períodos de vigência.

---

## O valor depende do tipo de plantão?

**Sim.** Tipos como T1, T2, T3, R1, R2 podem possuir multiplicadores diferentes.
Exemplo: Plantão noturno pode ter adicional de 20%.

---

## O valor depende do médico?

**Depende.** O `hour_rate` do médico é o valor base. Algumas instituições possuem tabelas diferentes por especialidade ou antiguidade. O sistema deve suportar ambos os cenários.

---

## O valor depende do período?

**Sim.** Feriados, finais de semana e períodos específicos podem possuir regras diferentes.
Exemplo: Plantão em 25/12 pode ter adicional de 100%.

---

## Como extras influenciam?

Extras aprovados geram fatos financeiros do tipo `extra_approved`. Cada fatos é multiplicado pelo `hour_rate` do médico. O Remuneration Engine aplica a regra correspondente ao tipo `extra_approved`.

---

## Como plantões parcialmente cumpridos influenciam?

Apenas Assignments `completed` geram fatos financeiros. Um plantão parcialmente cumprido (started mas não completed) não gera fato. O Coverage Engine já trata isso.

---

## Como feriados influenciam?

Feriados são tratados como uma regra com multiplicador diferenciado. O PricingPolicy identifica se o plantão cai em feriado e aplica a regra correspondente. O sistema de BusinessCalendar (já existente) fornece essa informação.

---

## Como mudanças futuras de tabela serão suportadas?

Cada `RemunerationRule` possui:
- `version` — identificador da versão
- `valid_from` — data de início de vigência
- `valid_until` — data fim de vigência (None = vigente)
- `status` — active/inactive/superseded

Regras antigas permanecem no histórico. O PricingPolicy sempre busca a regra vigente para a data do fato.

---

## Como explicar cada cálculo para auditoria?

O `CalculationExplanation` contém:
1. **Fatos de entrada** — quais FinancialFacts foram utilizados
2. **Regra aplicada** — qual RemunerationRule foi selecionada
3. **Política utilizada** — qual PricingPolicy escolheu a regra
4. **Etapas do cálculo** — cada passo documentado
5. **Totais** — valor final por médico
6. **Justificativas** — por que cada decisão foi tomada

A explicação é um objeto imutável, serializável, e pode ser consultada a qualquer momento.

---

## Fluxo Completo

```
1. Coverage Engine consolida fatos operacionais
   ↓
2. FinancialSnapshot contém FinancialFacts
   ↓
3. PricingPolicy seleciona regra vigente
   ↓
4. RemunerationCalculator aplica regra a cada fato
   ↓
5. RemuneraçãoResult consolida resultados
   ↓
6. CalculationExplanation documenta cada passo
   ↓
7. Payroll consome resultado (Sprint 9)
```

---

## Decisões Deliberadas

| Decisão | Justificativa |
|---|---|
| Engine não acessa banco | Separação de responsabilidades |
| Regras são versionadas | Suporte a mudanças históricas |
| Cada cálculo possui explicação | Auditoria obrigatória |
| Simulação não persiste | Segurança e teste |
| Payroll é consumidor puro | Regras ficam no Engine |
