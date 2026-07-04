# Matriz de Consultas — Query Domain

**Sprint:** 10 — Reporting Domain, Audit Analytics & Explainability Foundation
**Data:** 2026-06-27

---

## Visão Geral

A matriz de consultas documenta quem faz quais perguntas, com qual frequência, criticidade e necessidade de auditoria.

---

## Perfil: Diretor

| # | Pergunta | Frequência | Criticidade | Auditoria | Query Object |
|---|---|---|---|---|---|
| D01 | Custo total da folha | Mensal | Alta | Sim | `FinancialAnalyticsQuery` |
| D02 | Médicos ativos | Semanal | Média | Não | `DoctorAnalyticsQuery` |
| D03 | Cobertura média | Semanal | Alta | Sim | `CoverageAnalyticsQuery` |
| D04 | Competências pendentes | Diária | Alta | Sim | `PayrollAnalyticsQuery` |
| D05 | Valor médio por plantão | Mensal | Média | Sim | `FinancialAnalyticsQuery` |
| D06 | Extras aprovados | Mensal | Média | Não | `CoverageAnalyticsQuery` |
| D07 | Evolução do custo | Mensal | Alta | Sim | `FinancialAnalyticsQuery` |
| D08 | Médicos maior carga | Mensal | Média | Não | `DoctorAnalyticsQuery` |
| D09 | Mudanças desde última competência | Conforme necessário | Alta | Sim | `TimelineQuery` |
| D10 | Tempo médio cálculo→aprovação | Mensal | Média | Sim | `PayrollAnalyticsQuery` |

---

## Perfil: Financeiro

| # | Pergunta | Frequência | Criticidade | Auditoria | Query Object |
|---|---|---|---|---|---|
| F01 | Total remunerações por médico | Mensal | Alta | Sim | `FinancialAnalyticsQuery` |
| F02 | Regras aplicadas | Mensal | Alta | Sim | `FinancialAnalyticsQuery` |
| F03 | Fatos financeiros por remuneração | Mensal | Alta | Sim | `FinancialAnalyticsQuery` |
| F04 | Custo por tipo de plantão | Mensal | Média | Não | `FinancialAnalyticsQuery` |
| F05 | Remunerações recalculadas | Mensal | Média | Sim | `PayrollAnalyticsQuery` |
| F06 | Diferença entre versões | Conforme necessário | Alta | Sim | `PayrollAnalyticsQuery` |
| F07 | Inconsistências detectadas | Mensal | Alta | Sim | `CoverageAnalyticsQuery` |
| F08 | Total horas por médico | Mensal | Média | Não | `DoctorAnalyticsQuery` |
| F09 | Extras pendentes | Semanal | Alta | Não | `CoverageAnalyticsQuery` |
| F10 | Evolução custo por médico | Mensal | Média | Não | `FinancialAnalyticsQuery` |

---

## Perfil: Coordenação

| # | Pergunta | Frequência | Criticidade | Auditoria | Query Object |
|---|---|---|---|---|---|
| C01 | Plantões descobertos | Diária | Alta | Não | `CoverageAnalyticsQuery` |
| C02 | Médicos disponíveis | Diária | Alta | Não | `DoctorAnalyticsQuery` |
| C03 | Plantões por médico | Semanal | Média | Não | `CoverageAnalyticsQuery` |
| C04 | Conflitos de agenda | Diária | Alta | Não | `CoverageAnalyticsQuery` |
| C05 | Taxa de ocupação | Semanal | Média | Não | `CoverageAnalyticsQuery` |
| C06 | Extras rejeitados | Semanal | Média | Sim | `CoverageAnalyticsQuery` |
| C07 | Histórico de plantões | Conforme necessário | Média | Não | `TimelineQuery` |
| C08 | Períodos abertos | Diária | Média | Não | `PayrollAnalyticsQuery` |
| C09 | Previsão cobertura | Mensal | Alta | Não | `CoverageAnalyticsQuery` |
| C10 | Médicos no limite | Semanal | Média | Não | `DoctorAnalyticsQuery` |

---

## Perfil: Auditoria

| # | Pergunta | Frequência | Criticidade | Auditoria | Query Object |
|---|---|---|---|---|---|
| A01 | Competências reabertas | Conforme necessário | Alta | Sim | `PayrollAnalyticsQuery` |
| A02 | Quem aprovou cada competência | Conforme necessário | Alta | Sim | `PayrollAnalyticsQuery` |
| A03 | Tempo médio de fechamento | Mensal | Média | Sim | `PayrollAnalyticsQuery` |
| A04 | Alterações após bloqueio | Conforme necessário | Alta | Sim | `AuditAnalytics` |
| A05 | Segregação de funções | Conforme necessário | Alta | Sim | `AuditAnalytics` |
| A06 | Outliers de remuneração | Mensal | Alta | Sim | `FinancialAnalyticsQuery` |
| A07 | Trilha completa de competência | Conforme necessário | Alta | Sim | `TimelineQuery` |
| A08 | Dados alterados após aprovação | Conforme necessário | Alta | Sim | `AuditAnalytics` |
| A09 | Integridade do trail | Mensal | Alta | Sim | `AuditAnalytics` |
| A10 | Regras violadas | Conforme necessário | Alta | Sim | `AuditAnalytics` |

---

## Perfil: Médico

| # | Pergunta | Frequência | Criticidade | Auditoria | Query Object |
|---|---|---|---|---|---|
| M01 | Plantões agendados | Diária | Alta | Não | `TimelineQuery` |
| M02 | Total remunerações | Mensal | Alta | Não | `FinancialAnalyticsQuery` |
| M03 | Extras aprovados | Semanal | Média | Não | `CoverageAnalyticsQuery` |
| M04 | Histórico de plantões | Conforme necessário | Média | Não | `TimelineQuery` |
| M05 | Regras aplicadas | Mensal | Média | Sim | `FinancialAnalyticsQuery` |
| M06 | Explicação do pagamento | Mensal | Alta | Sim | `DomainExplanation` |
| M07 | Inconsistências que afetam | Conforme necessário | Alta | Sim | `DomainExplanation` |
| M08 | Total horas trabalhadas | Mensal | Média | Não | `DoctorAnalyticsQuery` |

---

## Resumo por Query Object

| Query Object | Perguntas | Perfis |
|---|---|---|
| `DoctorAnalyticsQuery` | D02, D08, F08, C02, C10, M08 | Diretor, Financeiro, Coordenação, Médico |
| `CoverageAnalyticsQuery` | D03, D06, F07, F09, C01, C03, C04, C05, C06, C09, M03 | Todos |
| `FinancialAnalyticsQuery` | D01, D05, D07, F01, F02, F03, F04, F10, A06, M02, M05 | Diretor, Financeiro, Auditoria, Médico |
| `PayrollAnalyticsQuery` | D04, D10, F05, F06, C08, A01, A02, A03 | Diretor, Financeiro, Coordenação, Auditoria |
| `TimelineQuery` | D09, C07, A07, M01, M04 | Diretor, Coordenação, Auditoria, Médico |
| `DomainExplanation` | E01-E08, M06, M07 | Todos |
| `AuditAnalytics` | A04, A05, A08, A09, A10 | Auditoria |

---

## Criticidade por Query Object

| Query Object | Alta | Média | Total |
|---|---|---|---|
| `DoctorAnalyticsQuery` | 2 | 4 | 6 |
| `CoverageAnalyticsQuery` | 5 | 6 | 11 |
| `FinancialAnalyticsQuery` | 6 | 5 | 11 |
| `PayrollAnalyticsQuery` | 4 | 4 | 8 |
| `TimelineQuery` | 3 | 2 | 5 |
| `DomainExplanation` | 3 | 0 | 3 |
| `AuditAnalytics` | 5 | 0 | 5 |
