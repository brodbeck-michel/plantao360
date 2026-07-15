> ⚠️ **ADR HISTÓRICO — SUPERADO.** Registro mantido para rastreabilidade. A
> [Constituição](../../.specify/memory/constitution.md) (v1.1.0) supera os 31 ADRs onde houver
> conflito — em especial os de *freeze* e a arquitetura DDD/CQRS/event-sourcing, desmontada nas
> specs 003–006 (a `domain/` foi de 118 → ~13 arquivos; payroll/cobertura removidos). Índice e
> contexto em [docs/adr/README.md](README.md).

# ADR-023: Query Domain & Explainability

**Data:** 2026-06-27
**Status:** Accepted
**Decisor:** Arquiteto de Domínio
**Sprint:** 10

## Contexto

O Plantão 360 possui todo o domínio operacional e financeiro consolidado: Doctor, Assignment, Shift, Coverage Engine, Financial Facts, Remuneration Engine, Payroll Competency e Administrative Governance.

**Problema:** Não existe uma camada responsável por responder perguntas do negócio. Diretores, auditores, coordenadores e médicos precisam de informações que o sistema atual não consegue fornecer de forma estruturada.

## Decisão

Criar o **Query Domain** como camada de leitura especializada, separada dos Commands.

### Pergunta Fundamental

> "Como garantir que qualquer pergunta de negócio feita por um diretor, auditor, coordenador ou médico seja respondida utilizando exatamente as mesmas regras do domínio operacional e financeiro, sem duplicação de lógica?"

### Resposta

Através de componentes que consomem os mesmos Aggregates que os Commands utilizam, mas apresentam os dados em formatos otimizados para consulta.

---

## Princípio Fundamental

**Commands modificam estado. Queries explicam o estado.**

Nenhuma Query poderá alterar qualquer Aggregate.

---

## Componentes

### 1. Read Models (7 modelos)

Modelos imutáveis de leitura, desacoplados dos Models SQLAlchemy:

| Read Model | Propósito |
|---|---|
| `DoctorSummary` | Resumo de médico para consultas |
| `PeriodSummary` | Resumo de período |
| `ShiftSummary` | Resumo de plantão |
| `AssignmentSummary` | Resumo de atribuição |
| `CoverageSummary` | Resumo de cobertura |
| `FinancialSummary` | Resumo financeiro |
| `PayrollSummary` | Resumo de competência |

### 2. Query Objects (5 objetos)

Representam perguntas de negócio, nunca filtros HTTP:

| Query Object | Pergunta |
|---|---|
| `DoctorAnalyticsQuery` | Perguntas sobre médicos |
| `CoverageAnalyticsQuery` | Perguntas sobre cobertura |
| `FinancialAnalyticsQuery` | Perguntas sobre finanças |
| `PayrollAnalyticsQuery` | Perguntas sobre folha |
| `TimelineQuery` | Perguntas sobre linha do tempo |

### 3. Projeções (4 projeções)

Transformam dados dos Aggregates em formatos de consulta:

| Projeção | Propósito |
|---|---|
| `CoverageProjection` | Projeção de cobertura |
| `FinancialProjection` | Projeção financeira |
| `PayrollProjection` | Projeção de folha |
| `InstitutionProjection` | Projeção institucional |

### 4. Domain Explainability

Responde perguntas como "por quê":

| Componente | Propósito |
|---|---|
| `DomainExplanation` | Explicação completa |
| `ExplanationStep` | Passo da explicação |
| `ExplanationContext` | Contexto da explicação |

### 5. Audit Analytics

Consultas de auditoria:

| Componente | Propósito |
|---|---|
| `AuditAnalytics` | Analytics de auditoria |
| `CompetencyAudit` | Auditoria de competência |
| `ApprovalAudit` | Auditoria de aprovação |
| `ChangeAudit` | Auditoria de mudanças |

### 6. KPI Domain (4 KPIs)

Indicadores estratégicos com definição, fórmula e evidências:

| KPI | Indicador |
|---|---|
| `CoverageKPI` | Cobertura |
| `FinancialKPI` | Financeiro |
| `PayrollKPI` | Folha |
| `OperationalKPI` | Operacional |

### 7. InstitutionTimeline

Linha do tempo global reconstruindo a cadeia completa:

```
Shift → Assignment → Extra → Coverage → Financial Facts →
Remuneration → Payroll → Approval → Administrative Lock
```

### 8. Report Definitions

Contratos de consulta sem gerar output:

| Componente | Propósito |
|---|---|
| `ReportDefinition` | Contrato do relatório |
| `ReportField` | Campo do relatório |
| `ReportFilter` | Filtro do relatório |

---

## Query Service

Serviço read-only que orquestra todas as consultas:

- `execute_doctor_query`
- `execute_coverage_query`
- `execute_financial_query`
- `execute_payroll_query`
- `execute_timeline_query`
- `explain_remuneration`
- `explain_extra_rejection`
- `explain_competency_reopen`
- `get_audit_analytics`
- `get_coverage_kpi`
- `get_financial_kpi`
- `get_payroll_kpi`
- `get_operational_kpi`

---

## API Endpoints

Todos os endpoints são read-only:

| Endpoint | Método | Descrição |
|---|---|---|
| `/query/doctors` | GET | Consulta de médicos |
| `/query/coverage` | GET | Consulta de cobertura |
| `/query/financial` | GET | Consulta financeira |
| `/query/payroll` | GET | Consulta de folha |
| `/query/timeline` | GET | Linha do tempo |
| `/query/explain/remuneration` | GET | Explicação de remuneração |
| `/query/explain/extra-rejection` | GET | Explicação de rejeição |
| `/query/explain/competency-reopen` | GET | Explicação de reabertura |
| `/query/audit` | GET | Analytics de auditoria |
| `/query/kpi/coverage` | GET | KPI de cobertura |
| `/query/kpi/financial` | GET | KPI financeiro |
| `/query/kpi/payroll` | GET | KPI de folha |
| `/query/kpi/operational` | GET | KPI operacional |

---

## Consumidores Futuros

O Query Domain servirá como fonte única de consulta para:

1. Frontend React
2. Power BI
3. APIs públicas
4. Integrações externas
5. Dashboards
6. Relatórios PDF/Excel

**Todos consumirão os mesmos Read Models e Query Objects**, sem duplicação de regras.

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

- docs/domain/analises/analise-consultas-negocio.md
- docs/domain/glossario-consultas.md
- docs/domain/matriz-consultas.md
- ADR-022-governanca-administrativa.md
