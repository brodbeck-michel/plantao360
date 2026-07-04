# Glossário de Remuneração

**Sprint:** 8
**Data:** 2026-06-26

---

## Termos

### Remuneração
Valor monetário devido a um médico por seus direitos financeiros. Resultado da aplicação de regras sobre fatos financeiros consolidados. Não confundir com pagamento (que é a transferência efetiva de valores).

### Regra (RemunerationRule)
Definição formal de como um tipo de fato financeiro é convertido em valor monetário. Contém: tipo de fato, valor base, multiplicadores, período de vigência. Regras são versionadas e imutáveis.

### Política (PricingPolicy)
Componente que seleciona qual regra aplicar para um determinado fato financeiro. Considera: tipo do fato, data do fato, médico, período. Não calcula valores — apenas escolhe a regra.

### Tabela
Conjunto de regras vigentes para um período específico. Uma tabela pode conter múltiplas regras para diferentes tipos de fatos. O termo "tabela" é used colloquially; formalmente, é um grupo de RemunerationRules.

### Valor Hora (hour_rate)
Valor monetário por hora trabalhado, definido no cadastro do médico. É o valor base para cálculos. Pode ser sobrescrito por regras específicas.

### Adicional
Percentual ou valor fixo adicionado ao valor base. Exemplos: adicional noturno (+20%), adicional feriado (+100%). Cada regra pode definir seus próprios adicionais.

### Multiplicador
Fator numérico que amplifica ou reduz o valor base. Exemplo: multiplicador 1.5 para plantões noturnos. Diferente de adicional (que é adicionado) — multiplicador é aplicado sobre o valor.

### Resultado (RemunerationResult)
Representação consolidada do resultado do cálculo de remuneração para um período. Contém: total por médico, total geral, lista de cálculos individuais. Não grava folha.

### Simulação (Simulation)
Modo de cálculo que produz resultado sem persistir alterações. Permite testar cenários, verificar impacto de mudanças, validar regras. Nenhum dado é gravado em banco.

### Competência
Período mensal (ano-mês) ao qual os cálculos são vinculados. Definido pelo Period. Cada competência pode ser calculada independentemente.

### Cálculo (Calculation)
Ato de aplicar uma regra sobre um fato financeiro para obter um valor. Cada cálculo é documentado com explicação completa.

### Explicação (CalculationExplanation)
Registro completo e imutável de como um cálculo foi executado. Contém: fatos de entrada, regra aplicada, etapas, totais, justificativas. Elemento central para auditoria.

---

## Diagrama de Relacionamento

```
FinancialFact
    │
    ▼
PricingPolicy ──seleciona──▶ RemunerationRule
    │
    ▼
RemuneraçãoCalculator
    │
    ├──▶ RemunerationResult (consolidação)
    │
    └──▶ CalculationExplanation (documentação)
              │
              └──▶ Payroll (Sprint 9)
```
