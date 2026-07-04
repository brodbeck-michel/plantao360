# Glossário — Payroll & Competência Financeira

**Sprint:** 9
**Data:** 2026-06-26

---

| Termo | Definição |
|---|---|
| **Competência** | Período financeiro de referência (mês/ano) que será consolidado em folha de pagamento. Identificada por year_month (ex: 202606). |
| **Folha** | Documento financeiro oficial que consolida todas as remunerações de uma competência. Equivale ao conceito de "payroll" em sistemas financeiros. |
| **Versão** | Cópia imutável do estado de uma competência em um momento dado. Toda reabertura gera nova versão. Nunca se sobrescreve — sempre se cria nova versão. |
| **Aprovação** | Ato formal que confirma a correção dos dados de uma competência. Após aprovação, a competência fica imutável. Requer pessoa autorizada. |
| **Fechamento** | Transição de estado que impede alterações na competência. Diferente de "fechar período" — fecha a competência, não os dados operacionais. |
| **Conferência** | Revisão manual dos totais e detalhes antes de aprovar. Responsável valida: totais por médico, regras aplicadas, explicações. |
| **Reabertura** | Operação restrita que retorna uma competência ao estado de cálculo. Gera nova versão. Requer justificativa. |
| **Auditoria** | Rastreabilidade completa de todas as ações: quem, quando, por quê. Cada transição gera registro de auditoria. |
| **Consolidação** | Processo de agregar dados operacionais em resultados financeiros. Executado por Coverage Engine e Remuneration Engine. |
| **Snapshot** | Fotografia imutável de dados em um momento dado. Existem dois tipos: FinancialSnapshot (dados de entrada) e PayrollSnapshot (resultado consolidado). |
| **Selagem** | Ato de criar o PayrollSeal após aprovação. Congela todos os dados necessários para reprodução futura. Irreversível. |
| **Histórico** | Conjunto de todas as versões e selos de uma competência. Preservado indefinidamente. Nunca é alterado. |
| **PayrollSeal** | Documento imutável que contém snapshot completo da competência: fatos, resultados, regras, explicações. Base para auditoria e reprodução. |
| **PayrollVersion** | Versão imutável do estado de uma competência. Contém todos os dados necessários para reprodução. |
| **PayrollLifecycle** | Máquina de estados que controla as transições de uma competência: draft → calculated → reviewed → approved → exported → paid → archived. |
| **PayrollExplanation** | Documento que explica, passo a passo, como cada remuneração foi calculada. Contém: regra aplicada, valores de entrada, valores de saída, justificativas. |
| **PayrollAuditSnapshot** | Fotografia de auditoria contendo: todos os estados anteriores, timestamps, responsáveis, ações executadas. |
