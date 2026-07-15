> ⚠️ **ADR HISTÓRICO — SUPERADO.** Registro mantido para rastreabilidade. A
> [Constituição](../../.specify/memory/constitution.md) (v1.1.0) supera os 31 ADRs onde houver
> conflito — em especial os de *freeze* e a arquitetura DDD/CQRS/event-sourcing, desmontada nas
> specs 003–006 (a `domain/` foi de 118 → ~13 arquivos; payroll/cobertura removidos). Índice e
> contexto em [docs/adr/README.md](README.md).

# ADR-020: Motor de Remuneração

**Data:** 2026-06-26
**Status:** Accepted
**Decisor:** Arquiteto de Domínio

## Contexto

O Plantão 360 possui o Coverage Engine (Sprint 7) que consolida fatos operacionais em fatos financeiros. O Payroll (Sprint 9) precisa calcular remuneração. O Payroll não deve interpretar regras financeiras — apenas consolidar resultados.

## Decisão

Criar o **Remuneration Engine** como camada intermediária entre fatos financeiros e folha de pagamento.

### Separação de Responsabilidades

```
Operacional → Coverage Engine → Financeiro → Remuneration Engine → Payroll
(Dados)       (Consolidação)    (Fatos)       (Regras + Cálculo)    (Folha)
```

### Componentes

1. **RemuneraçãoRule** — Define como um tipo de fato é convertido em valor. Imutável, versionada.
2. **PricingPolicy** — Seleciona qual regra aplicar. Não calcula.
3. **RemuneraçãoCalculator** — Executa o cálculo. Produz resultado + explicação.
4. **RemuneraçãoResult** — Consolidação do resultado. Consumido pelo Payroll.
5. **CalculationExplanation** — Trilha de auditoria completa. Imutável.

### Princípios

- Engine não acessa banco de dados
- Cada cálculo é reproduzível e determinístico
- Toda remuneração possui explicação completa
- Simulação não persiste dados
- Regras são imutáveis e versionadas

## PricingPolicy

Seleciona regra vigente para um tipo de fato e data. Suporta:
- Múltiplas regras por tipo
- Períodos de vigência
- Regras sobrepostas (usa a mais recente)

## CalculationExplanation

Contém:
- Fatos de entrada
- Regra aplicada
- Etapas do cálculo (com valores de entrada/saída)
- Total final
- Justificativas

É imutável e serializável. Pode ser consultada a qualquer momento para auditoria.

## Versionamento

Cada RemuneraçãoRule possui:
- `version` — identificador (ex: "1.0")
- `valid_from` — início de vigência
- `valid_until` — fim de vigência (None = vigente)
- `status` — active/inactive/superseded

Regras antigas permanecem no histórico. O PricingPolicy busca a regra vigente.

## Simulation Mode

O RemuneraçãoCalculator possui modo simulação:
- Calcula resultado sem persistir
- Nenhum banco é alterado
- Resultado é descartado após consulta
- Permite testar cenários e validar regras

## Impacto sobre Payroll

- Payroll consome `RemuneraçãoResult` como entrada
- Cada `DoctorRemuneração` contém lista de `CalculationExplanation`
- Payroll aplica regras de pagamento (impostos, descontos) sobre os valores
- Separação permite alterar regras financeiras sem afetar Payroll

## Decisões Deliberadamente Adiadas

1. **Geração de folha** — Sprint 9
2. **Impostos e retenções** — Sprint 9
3. **Descontos** — Sprint 9
4. **Integração contábil** — Sprint 10
5. **Exportação para ERP** — Sprint 10
6. **Pagamentos** — Sprint 10
7. **Integração bancária** — Sprint 10

## Eventos de Domínio

- `remuneration.calculated.v1` — Cálculo executado
- `remuneration.simulated.v1` — Simulação executada
- `remuneration.recalculated.v1` — Recálculo após reabertura
- `remuneration.invalidated.v1` — Resultado invalidado

## Referências

- docs/domain/analises/analise-remuneracao.md
- docs/domain/glossario-remuneracao.md
- docs/domain/matriz-remuneracao.md
- docs/domain/invariantes-remuneracao.md
- docs/domain/casos-borda-remuneracao.md
