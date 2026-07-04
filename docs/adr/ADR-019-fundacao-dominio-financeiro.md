# ADR-019: Fundação do Domínio Financeiro

**Data:** 2026-06-26
**Status:** Accepted
**Decisor:** Arquiteto de Domínio

## Contexto

O sistema Plantão 360 possui módulos operacionais implementados (Doctor, Period, Shift, Assignment, Extras). O Payroll (Sprint 8) precisa consumir dados consolidados para calcular remuneração.

**Problema:** Não existe uma camada intermediária que transforme fatos operacionais em fatos financeiros. O Payroll não deve interpretar regras operacionais.

## Decisão

Criar a **Fundação do Domínio Financeiro** com três componentes:

### 1. Coverage Engine
- Consolida fatos operacionais (Assignment completado, Extra aprovado)
- Não calcula valores — apenas identifica e valida fatos elegíveis
- Detecta e registra inconsistências
- Gera CoverageSnapshot (fotografia operacional)

### 2. CoverageSnapshot
- Representação definitiva do estado operacional de uma competência
- Contém: médicos participantes, intervalos trabalhados, extras válidos, inconsistências
- Imutável após criação (pode ser invalidado por reabertura)

### 3. FinancialSnapshot
- Consolidação de todos os direitos financeiros de uma competência
- Contém lista de FinancialFact (fatos individuais)
- Consumido pelo Payroll (Sprint 8)
- Não contém valores monetários — apenas direitos

## Separação de Responsabilidades

```
Operacional          →  Coverage Engine  →  Financial  →  Payroll
(Dados brutos)          (Consolidação)       (Direitos)     (Valores)
```

O Payroll nunca interpreta regras operacionais. Apenas consome fatos financeiros consolidados.

## Fatos que Geram Direito

| Fato Operacional | Gera Direito? | Condição |
|---|---|---|
| Assignment `completed` | Sim | Shift não cancelled |
| Extra `approved` | Sim | Extra não cancelled |
| Assignment `cancelled` | Revoga | Retroativo |
| Extra `rejected` | Nunca | Estado terminal |

## Impacto sobre Payroll

- Payroll consome `FinancialSnapshot` como entrada
- Cada `FinancialFact` contém: tipo, médico, competência, duração
- Payroll aplica tabela de valores sobre os fatos
- Separação permite alterar regras operacionais sem afetar Payroll

## Decisões Deliberadamente Adiadas

1. **Cálculo de valores** — Sprint 8 (Payroll)
2. **Tabela de remuneração** — Sprint 8
3. **Integração contábil** — Sprint 9
4. **Relatórios financeiros** — Sprint 9
5. **Notificações** — Sprint 10
6. **Multi-setor** — Sprint 10

## Eventos de Domínio

- `coverage.consolidated.v1` — Consolidação executada
- `financial.snapshot.created.v1` — Snapshot financeiro criado
- `financial.fact.generated.v1` — Fato financeiro individual gerado
- `financial.fact.revoked.v1` — Fato financeiro revogado

## Consequências

### Positivas
- Payroll é consumidor puro — não precisa entender operações
- Consolidação é idempotente e reversível
- Inconsistências são detectadas e documentadas
- Reabertura de competência suportada

### Negativas
- Mais uma camada de abstração
- Consolidação requer execução explícita
- Complexidade inicial maior

## Referências

- docs/domain/analises/analise-cobertura-financeira.md
- docs/domain/glossario-financeiro.md
- docs/domain/matriz-fatos-financeiros.md
- docs/domain/invariantes-financeiras.md
- docs/domain/matriz-consistencia.md
