# Análise das Consultas de Negócio — Query Domain

**Sprint:** 10 — Reporting Domain, Audit Analytics & Explainability Foundation
**Data:** 2026-06-27
**Pergunta Fundamental:**

> "Como garantir que qualquer pergunta de negócio feita por um diretor, auditor, coordenador ou médico seja respondida utilizando exatamente as mesmas regras do domínio operacional e financeiro, sem duplicação de lógica?"

---

## Resposta

A resposta é: **através de Read Models imutáveis que consomem os Aggregates existentes sem modificá-los, Query Objects que representam perguntas de negócio, Projeções que transformam dados em formatos de consulta, e KPIs que encapsulam fórmulas e evidências.**

O Query Domain não duplica regras. Ele **consome** os mesmos Aggregates que os Commands utilizam, mas apresenta os dados em formatos otimizados para consulta.

---

## Perguntas de Negócio por Perfil

### 1. Quais perguntas um Diretor faria?

| # | Pergunta | Frequência | Criticidade |
|---|---|---|---|
| D01 | Qual o custo total da folha deste mês? | Mensal | Alta |
| D02 | Quantos médicos ativos temos? | Semanal | Média |
| D03 | Qual a cobertura média dos plantões? | Semanal | Alta |
| D04 | Quantas competências estão pendentes de aprovação? | Diária | Alta |
| D05 | Qual o valor médio por plantão? | Mensal | Média |
| D06 | Quantos extras foram aprovados este mês? | Mensal | Média |
| D07 | Qual a evolução do custo nos últimos 6 meses? | Mensal | Alta |
| D08 | Quais médicos tiveram maior carga de plantões? | Mensal | Média |
| D09 | O que mudou desde a última competência aprovada? | Conforme necessário | Alta |
| D10 | Qual o tempo médio entre cálculo e aprovação? | Mensal | Média |

### 2. Quais perguntas o Financeiro faria?

| # | Pergunta | Frequência | Criticidade |
|---|---|---|---|
| F01 | Qual o total de remunerações por médico? | Mensal | Alta |
| F02 | Quais regras de remuneração foram aplicadas? | Mensal | Alta |
| F03 | Quais fatos financeiros geraram cada remuneração? | Mensal | Alta |
| F04 | Qual o custo por tipo de plantão? | Mensal | Média |
| F05 | Quantas remunerações foram recalculadas? | Mensal | Média |
| F06 | Qual a diferença entre versões de uma competência? | Conforme necessário | Alta |
| F07 | Quais inconsistencies foram detectadas no cálculo? | Mensal | Alta |
| F08 | Qual o total de horas trabalhadas por médico? | Mensal | Média |
| F09 | Quais extras estão pendentes de processamento? | Semanal | Alta |
| F10 | Qual a evolução do custo por médico? | Mensal | Média |

### 3. Quais perguntas a Coordenação faria?

| # | Pergunta | Frequência | Criticidade |
|---|---|---|---|
| C01 | Quais plantões estão descobertos? | Diária | Alta |
| C02 | Quais médicos estão disponíveis para um período? | Diária | Alta |
| C03 | Quantos plantões cada médico cobriu este mês? | Semanal | Média |
| C04 | Quais conflitos de agenda existem? | Diária | Alta |
| C05 | Qual a taxa de ocupação por tipo de plantão? | Semanal | Média |
| C06 | Quais extras foram rejeitados e por quê? | Semanal | Média |
| C07 | Qual o histórico de plantões de um médico? | Conforme necessário | Média |
| C08 | Quais períodos estão abertos para edição? | Diária | Média |
| C09 | Qual a previsão de cobertura para o próximo mês? | Mensal | Alta |
| C10 | Quais médicos atingiram o limite de plantões? | Semanal | Média |

### 4. Quais perguntas a Auditoria faria?

| # | Pergunta | Frequência | Criticidade |
|---|---|---|---|
| A01 | Quais competências foram reabertas e por quê? | Conforme necessário | Alta |
| A02 | Quem aprovou cada competência? | Conforme necessário | Alta |
| A03 | Qual o tempo médio de fechamento? | Mensal | Média |
| A04 | Quais alterações ocorreram após bloqueio? | Conforme necessário | Alta |
| A05 | Existe segregação de funções na aprovação? | Conforme necessário | Alta |
| A06 | Quais outliers de remuneração existem? | Mensal | Alta |
| A07 | Qual a trilha completa de uma competência? | Conforme necessário | Alta |
| A08 | Quais dados foram alterados após aprovação? | Conforme necessário | Alta |
| A09 | Qual a integridade do trail de auditoria? | Mensal | Alta |
| A10 | Quais regras de negócio foram violadas? | Conforme necessário | Alta |

### 5. Quais perguntas um Médico faria?

| # | Pergunta | Frequência | Criticidade |
|---|---|---|---|
| M01 | Quais plantões tenho agendados? | Diária | Alta |
| M02 | Qual o valor total das minhas remunerações? | Mensal | Alta |
| M03 | Quais extras foram aprovados para mim? | Semanal | Média |
| M04 | Qual o histórico dos meus plantões? | Conforme necessário | Média |
| M05 | Quais regras foram aplicadas ao meu cálculo? | Mensal | Média |
| M06 | Qual a explicação detalhada do meu pagamento? | Mensal | Alta |
| M07 | Quais inconsistências afetaram meus dados? | Conforme necessário | Alta |
| M08 | Qual o total de horas trabalhadas no período? | Mensal | Média |

---

## Perguntas que Explicam Decisões

| # | Pergunta | Tipo | Componente |
|---|---|---|---|
| E01 | Por que esse médico recebeu esse valor? | Explainability | DomainExplanation |
| E02 | Por que um extra foi rejeitado? | Explainability | DomainExplanation |
| E03 | Por que uma competência foi reaberta? | Explainability | DomainExplanation |
| E04 | Por que um plantão ficou descoberto? | Explainability | DomainExplanation |
| E05 | Por que uma regra não foi aplicada? | Explainability | DomainExplanation |
| E06 | Por que o custo aumentou? | Analytics | FinancialAnalytics |
| E07 | Por que a cobertura diminuiu? | Analytics | CoverageAnalytics |
| E08 | Por que uma remuneração foi recalculada? | Explainability | DomainExplanation |

---

## Indicadores Estratégicos

| # | Indicador | Fórmula | Fonte |
|---|---|---|---|
| K01 | Cobertura Média | total_plantoes_cobertos / total_plantoes * 100 | CoverageKPI |
| K02 | Custo Médio por Plantão | total_remuneracoes / total_plantoes | FinancialKPI |
| K03 | Tempo Médio de Fechamento | media(data_aprovacao - data_calculo) | PayrollKPI |
| K04 | Taxa de Extras Aprovados | extras_aprovados / extrasolicitados * 100 | OperationalKPI |
| K05 | Médicos por Plantão | total_medicos / total_plantoes | OperationalKPI |
| K06 | Custo por Médico | total_remuneracoes / total_medicos | FinancialKPI |
| K07 | Taxa de Reabertura | competencias_reabertas / total_competencias * 100 | PayrollKPI |
| K08 | Horas Médias por Médico | total_horas / total_medicos | OperationalKPI |

---

## Consultas que Exigem Rastreabilidade

| # | Consulta | Componente | Rastreabilidade |
|---|---|---|---|
| R01 | Timeline completa de uma competência | InstitutionTimeline | Eventos + timestamps + responsáveis |
| R02 | Explicação de um cálculo de remuneração | DomainExplanation | Regras + fatos + resultados |
| R03 | Trail de auditoria de uma competência | PayrollAuditSnapshot | Entries + timestamps + status |
| R04 | Histórico de versões | PayrollVersion | Snapshot + rules + results |
| R05 | Cadeia de aprovação | AdministrativeApproval | Checklist + approval + lock |

---

## Pergunta Fundamental — Resposta Completa

**"Como garantir que qualquer pergunta de negócio feita por um diretor, auditor, coordenador ou médico seja respondida utilizando exatamente as mesmas regras do domínio operacional e financeiro, sem duplicação de lógica?"**

### Solução: Query Domain com Read Models Imutáveis

1. **Read Models** consomem os mesmos Aggregates que os Commands utilizam
2. **Query Objects** representam perguntas de negócio (nunca filtros HTTP)
3. **Projeções** transformam dados dos Aggregates em formatos de consulta
4. **KPIs** encapsulam fórmulas e evidências
5. **Explainability** responde "por quê" usando as mesmas regras do domínio
6. **Timeline** reconstrói a cadeia completa de eventos
7. **Report Definitions** definem contratos de consulta sem gerar output

**Nenhuma regra de negócio é duplicada.** O Query Domain é uma **janela de leitura** sobre os mesmos Aggregates que os Commands modificam.

---

## Decisões Deliberadamente Adiadas

1. Power BI
2. PDF
3. Excel
4. Dashboard React
5. Cubos OLAP
6. Jasper Reports
7. Impressão
8. Analytics em tempo real

---

## Referências

- docs/domain/glossario-consultas.md
- docs/domain/matriz-consultas.md
- ADR-023-query-domain-explainability.md
