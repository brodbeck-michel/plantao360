# Análise da Competência Financeira — Payroll

**Sprint:** 9 — Payroll Aggregate & Competência Financeira
**Data:** 2026-06-26
**Pergunta Fundamental:**

> "Como garantir que uma competência financeira possa ser reproduzida exatamente da mesma forma daqui a cinco anos, mesmo que todas as regras de remuneração tenham evoluído?"

---

## Resposta

A resposta é: **selando uma fotografia imutável que contenha todos os dados necessários para reprodução, sem depender de dados vivos.**

Uma competência financeira, ao ser aprovada, gera um **PayrollSeal** que contém:
- Snapshot financeiro completo (dados brutos)
- Resultado de remuneração completo (cálculos executados)
- Regras aplicadas no momento (snapshots das regras)
- Explicações passo a passo de cada cálculo
- Identificadores de todas as entidades envolvidas

Após o selo, **nenhum dado pode ser alterado**. O histórico permanece exatamente como era naquele momento.

---

## Perguntas de Negócio — Respostas

### 1. O que caracteriza uma competência?

Uma competência financeira é o **período de referência** (mês/ano) em que ocorreram plantões e extras, e que será consolidado em uma folha de pagamento oficial.

Uma competência é caracterizada por:
- **Período de referência** (ex: 2026-06)
- **Estado** (draft → calculated → reviewed → approved → exported → paid → archived)
- **Versão** (cada reabertura gera nova versão)
- **Selo** (após aprovação, dados são congelados)
- **Snapshot** (fotografia dos dados no momento do cálculo)

### 2. Quando ela nasce?

Uma competência nasce quando um **usuário autorizado** inicia o cálculo da folha para um período. O nascimento pode ocorrer de duas formas:

- **Manual:** Operador seleciona um período e solicita cálculo
- **Automática:** Sistema detecta período fechado sem cálculo e sugere criação

### 3. Quando pode ser recalculada?

Uma competência pode ser recalculada **apenas nos estados `draft` ou `calculated`**, antes da revisão.

Após revisão (`reviewed`), qualquer alteração requer **reabertura**, que gera nova versão.

### 4. Quem pode aprová-la?

Aprovação requer papel autorizado:
- **Gestor de Escala** (pode revisar)
- **Administrador Financeiro** (pode aprovar)
- **Diretor** (pode aprovar e exportar)

Aprovação é um ato de responsabilidade — quem aprova assume que os dados estão corretos.

### 5. Quem pode reabri-la?

Reabertura é uma operação restrita:
- Apenas **Administrador Financeiro** ou **Diretor**
- Gera **nova versão** (nunca sobrescreve)
- Requer **justificativa** obrigatória
- Invalida aprovações anteriores

### 6. O que significa fechar uma competência?

Fechar (close) significa:
- Nenhum novo plantão ou extra pode ser adicionado ao período
- A cobertura operacional é consolidada
- O estado muda de `draft` para `closed`

**Nota:** Fechar período ≠ fechar competência. São operações distintas.

### 7. Quais impactos jurídicos existem?

- **Imutabilidade após aprovação:** Uma competência aprovada não pode ser silenciosamente alterada
- **Auditoria:** Toda alteração deve ser rastreável (quando, por quê, por quem)
- **Prescrição:** Competências arquivadas devem ser preservadas por prazo legal (5 anos mínimo)
- **Prova documental:** O PayrollSeal serve como prova em caso de disputa

### 8. Quais impactos operacionais existem?

- **Consolidação:** Uma vez aprovada, a competência não pode ter dados operacionais modificados
- **Retificação:** Se erro for detectado, requer reabertura com nova versão
- **Conferência:** Antes de aprovar, revisor deve validar todos os totais
- **Exportação:** Após aprovação, dados podem ser exportados para sistemas externos

### 9. O que acontece quando uma remuneração muda após fechamento?

Se uma regra de remuneração é alterada após o fechamento:
- A competência **não é afetada** automaticamente
- A regra antiga permanece registrada no PayrollSeal
- Se a alteração deve ser aplicada, requer **reabertura** e **nova versão**
- A versão anterior permanece no histórico como registro

### 10. Como preservar histórico?

O histórico é preservado através de:
- **PayrollSeal:** Fotografia imutável com todos os dados
- **PayrollVersion:** Cada versão é uma cópia completa do estado
- **PayrollExplanation:** Explicação detalhada de cada cálculo
- **PayrollAuditSnapshot:** Registro de auditoria com timestamps e responsáveis

---

## Pergunta Fundamental — Resposta Completa

**"Como garantir que uma competência financeira possa ser reproduzida exatamente da mesma forma daqui a cinco anos, mesmo que todas as regras de remuneração tenham evoluído?"**

### Solução: Imutabilidade por Snapshot Completo

1. **Ao calcular:** O sistema cria um `FinancialSnapshot` e um `RemunerationResult` como objetos imutáveis
2. **Ao revisar:** Valida-se que os cálculos estão corretos
3. **Ao aprovar:** O sistema cria um `PayrollSeal` que contém cópias completas de:
   - Todos os `FinancialFactData` (fatos de entrada)
   - Todos os `DoctorRemuneration` (resultados por médico)
   - Todas as `CalculationExplanation` (explicações passo a passo)
   - Todas as `RemunerationRule` aplicadas (snapshots das regras)
4. **Ao arquivar:** O selo permanece imutável para sempre
5. **Para reproduzir:** Basta ler o selo e reconstruir exatamente o que aconteceu

**Nunca se referencia dados vivos após aprovação.** Sempre se copia.

---

## Fluxo Completo

```
Operação                → Coverage Engine → FinancialSnapshot
                                              ↓
                        → RemunerationEngine → RemuneraçãoResult
                                              ↓
                        → PayrollCompetency → PayrollSeal (após aprovação)
                                              ↓
                        → Arquivo Imutável (5+ anos)
```

---

## Decisões Deliberadamente Adiadas

1. Integração bancária
2. CNAB
3. PIX
4. ERP
5. XML
6. Contabilidade
7. Assinatura digital
8. Pagamentos automáticos

Essas funcionalidades serão implementadas nas Sprints 10+.
