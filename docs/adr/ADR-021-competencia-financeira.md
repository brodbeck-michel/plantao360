> ⚠️ **ADR HISTÓRICO — SUPERADO.** Registro mantido para rastreabilidade. A
> [Constituição](../../.specify/memory/constitution.md) (v1.1.0) supera os 31 ADRs onde houver
> conflito — em especial os de *freeze* e a arquitetura DDD/CQRS/event-sourcing, desmontada nas
> specs 003–006 (a `domain/` foi de 118 → ~13 arquivos; payroll/cobertura removidos). Índice e
> contexto em [docs/adr/README.md](README.md).

# ADR-021: Competência Financeira (Payroll)

**Data:** 2026-06-26
**Status:** Accepted
**Decisor:** Arquiteto de Domínio

## Contexto

O Plantão 360 possui toda a cadeia de domínio construída: Coverage Engine, Financial Facts, Remuneration Engine, Remuneration Result. A Sprint 9 precisa transformar resultados já consolidados em um documento financeiro oficial da competência.

**Problema:** Não existe uma entidade que represente oficialmente uma competência financeira, com versionamento, selo imutável e trilha de auditoria.

## Decisão

Criar o **PayrollCompetency** como Aggregate Root que representa oficialmente uma competência financeira.

### Princípio Fundamental

Payroll NÃO é um motor de cálculo. Payroll é um Aggregate responsável por representar oficialmente uma competência financeira. Toda inteligência permanece nos módulos anteriores.

### Componentes

1. **PayrollCompetency (Aggregate Root)** — Lifecycle, versões, snapshots, auditoria
2. **PayrollVersion** — Versão imutável do estado da competência
3. **PayrollStateMachine** — Controla transições: draft → calculated → reviewed → approved → exported → paid → archived
4. **PayrollSeal** — Selo imutável criado após aprovação
5. **PayrollExplanation** — Explicação passo a passo de cada cálculo
6. **PayrollAuditSnapshot** — Fotografia completa de auditoria

### Pergunta Fundamental

> "Como garantir que uma competência financeira possa ser reproduzida exatamente da mesma forma daqui a cinco anos, mesmo que todas as regras de remuneração tenham evoluído?"

**Resposta:** Selando uma fotografia imutável que contenha todos os dados necessários para reprodução, sem depender de dados vivos.

---

## PayrollCompetency (Aggregate Root)

Representa oficialmente uma competência. Responsável por:
- Ciclo de vida (7 estados)
- Versões (cada reabertura gera nova versão)
- Snapshots (FinancialSnapshot + RemunerationResult)
- Auditoria (quando, por quê, por quem)

---

## PayrollVersion

Versão imutável do estado de uma competência. Contém:
- FinancialSnapshotData (fatos de entrada)
- RemuneraçãoResult (resultados de cálculo)
- RemunerationRule aplicadas (snapshots das regras)
- Timestamp de criação
- Autor

Nunca editar. Sempre criar nova versão.

---

## PayrollLifecycle

Máquina de estados com 7 estados:

```
draft → calculated → reviewed → approved → exported → paid → archived
```

Transições especiais:
- Qualquer estado (exceto draft e archived) → draft (reabertura)
- Reabertura requer justificativa
- Reabertura gera nova versão

---

## PayrollSeal

Selo imutável criado ao aprovar. Contém:
- Snapshot completo dos dados
- Regras aplicadas no momento
- Resultados de remuneração
- Timestamp e autor

Após criação: nenhuma alteração permitida.

---

## PayrollExplanation

Explica, passo a passo, como cada remuneração foi calculada:
- Fato de entrada
- Regla aplicada
- Valores de entrada/saída
- Total

Imutável após criação.

---

## PayrollAuditSnapshot

Fotografia completa de auditoria. Append-only:
- Cada transição registra: timestamp, ação, autor, estados
- Registros existentes não podem ser alterados
- Disponível para consultas futuras

---

## Eventos de Domínio

- `payroll.created.v1` — Competência criada
- `payroll.calculated.v1` — Cálculo executado
- `payroll.reviewed.v1` — Revisão concluída
- `payroll.approved.v1` — Aprovação formal (selo criado)
- `payroll.exported.v1` — Exportação para ERP
- `payroll.paid.v1` — Pagamento confirmado
- `payroll.archived.v1` — Arquivamento automático
- `payroll.reopened.v1` — Reabertura (gera nova versão)

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

---

## Referências

- docs/domain/analises/analise-competencia-financeira.md
- docs/domain/glossario-payroll.md
- docs/domain/matriz-competencia.md
- docs/domain/invariantes-payroll.md
- docs/domain/casos-borda-payroll.md
