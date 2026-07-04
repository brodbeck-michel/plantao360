# Glossário — Consultas, Query Domain & Explainability

**Sprint:** 10 — Reporting Domain, Audit Analytics & Explainability Foundation
**Data:** 2026-06-27

---

| Termo | Definição |
|---|---|
| **Consulta** | Pergunta de negócio feita pelo usuário. Representa uma necessidade de informação. Nunca modifica estado. |
| **Projeção** | Transformação de dados de um Aggregate em formato otimizado para consulta. Consome sem modificar. |
| **Read Model** | Modelo imutável de leitura. Desacoplado dos Models SQLAlchemy. Representa o estado do domínio para consulta. |
| **KPI** | Key Performance Indicator. Indicador estratégico com definição, fórmula, evidências e explicação. |
| **Analytics** | Análise de dados do domínio para identificar padrões, tendências e anomalias. Não gera gráficos. |
| **Explainability** | Capacidade de explicar por que algo aconteceu. Responde perguntas como "por que esse valor?" usando regras do domínio. |
| **Timeline** | Linha do tempo completa de uma entidade. Reconstrói a cadeia de eventos com timestamps e responsáveis. |
| **Resumo** | Visão consolidada de uma entidade. Contém apenas campos essenciais para consulta rápida. |
| **Evidência** | Dado que comprova uma afirmação. Utilizada por KPIs e Explainability para fundamentar respostas. |
| **Métrica** | Valor quantificável que mede aspecto do negócio. Base para KPIs. |
| **Indicador** | Métrica com contexto estratégico. Inclui meta, tendência e interpretação. |
| **Snapshot de Consulta** | Fotografia imutável do estado de uma entidade no momento da consulta. Preservada para auditoria. |
| **Query Object** | Objeto que representa uma pergunta de negócio. Nunca é um filtro HTTP. Contém parâmetros da consulta. |
| **Read Domain** | Camada de leitura especializada. Consome Aggregates sem modificá-los. Base para consultas. |
| **Domain Explanation** | Explicação gerada pelo domínio. Usa as mesmas regras de cálculo para justificar resultados. |
| **Audit Analytics** | Análises de auditoria. Responde perguntas sobre integridade, conformidade e riscos. |
| **Report Definition** | Contrato de consulta. Define nome, objetivo, campos, filtros, ordenação e permissões. Sem gerar output. |
| **CQRS** | Command Query Responsibility Segregation. Padrão que separa leitura e escrita. Nesta sprint, apenas a camada de leitura. |
| **Consistency** | Propriedade que garante que o Read Model reflete fielmente o estado do Aggregate. Eventual consistency é aceitável. |
| **Desacoplamento** | Separação entre camada de escrita (Commands) e leitura (Queries). Read Models são independentes dos Models. |
