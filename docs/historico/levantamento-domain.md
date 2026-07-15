# Levantamento da camada `domain/` (Fase 2 — passo 2)

Análise de acoplamento de cada módulo de `backend/app/domain/` medida em 2026-07-13.
Métrica por módulo: **arqs** (arquivos .py, sem `__init__`), **prod** (nº de referências de
código de PRODUTO), **locais** (nº de arquivos de produto distintos que o consomem), **test**
(referências em testes), **dom** (referências por outros módulos de domain).

> Regra de ouro (Princípio I): módulo com **prod=0** não é usado pelo produto; módulo com
> **locais=1** é consumidor único → candidato a *inline*.

## Tabela (ordenada: menos usado em produto primeiro)

| módulo | arqs | prod | locais | test | dom | Classificação |
|---|---:|---:|---:|---:|---:|---|
| entities | 0 | 0 | 0 | 0 | 0 | **DELETAR** (vazio) |
| services | 0 | 0 | 0 | 0 | 0 | **DELETAR** (vazio; confunde com `app/services`) |
| reports | 0 | 0 | 0 | 1 | 0 | **DELETAR** (vazio) |
| calendar | 1 | 0 | 0 | 1 | 1 | **DELETAR** (morto em produto) |
| metrics | 1 | 0 | 0 | 1 | 0 | **DELETAR** |
| snapshots | 1 | 0 | 0 | 1 | 0 | **DELETAR** |
| transitions | 1 | 0 | 0 | 1 | 0 | **DELETAR** |
| contracts | 2 | 0 | 0 | 2 | 0 | **DELETAR** |
| overlap | 3 | 0 | 0 | 3 | 0 | **DELETAR** ⚠️ (ver alerta) |
| value_objects | 6 | 0 | 0 | 5 | 1 | **DELETAR** |
| remuneration | 6 | 0 | 0 | 14 | 2 | **DELETAR** ⚠️ (ver alerta) |
| base | 1 | 0 | 0 | 3 | 4 | **DELETAR** com os que o usam |
| exceptions | 1 | 1 | 1 | 0 | 0 | INLINE/manter (camada api) |
| timeline | 0 | 1 | 1 | 1 | 0 | **INLINE** → query_service |
| policies | 2 | 1 | 1 | 2 | 0 | **INLINE** → use_cases/periods |
| coverage | 1 | 1 | 1 | 2 | 1 | **INLINE** → coverage_service |
| financial | 1 | 1 | 1 | 4 | 2 | **INLINE** → coverage_service |
| projections | 5 | 1 | 1 | 4 | 0 | **INLINE** → dashboard_service |
| analytics | 4 | 1 | 1 | 4 | 0 | **INLINE** → query_service |
| explainability | 3 | 3 | 1 | 3 | 0 | **INLINE** → query_service |
| kpi | 4 | 4 | 1 | 4 | 0 | **INLINE** → query_service |
| payroll | 2 | 3 | 2 | 4 | 0 | INLINE → payroll_service (+validator) |
| read_models | 8 | 5 | 2 | 7 | 0 | **CONSOLIDAR** nos services (dashboard/query) |
| query | 6 | 12 | 4 | 5 | 0 | CONSOLIDAR (query objects) |
| rules | 3 | 7 | 7 | 4 | 1 | **AVALIAR** (regra real; manter, simplificar) |
| state_machines | 5 | 8 | 8 | 5 | 2 | **AVALIAR** (transições; esforço maior) |
| errors | 7 | 19 | 19 | 8 | 1 | **MANTER** (catálogo de erros) |
| events | 2 | 20 | 20 | 7 | 3 | **MANTER** (event_names + collector) |
| constants | 12 | 46 | 31 | 39 | 18 | **MANTER** (enums: ShiftStatus etc.) |

## Grupos e estratégia

### Grupo A — DELETAR (zero uso em produto) — ~23 arquivos, RISCO BAIXO
`entities, services, reports, calendar, metrics, snapshots, transitions, contracts, overlap,
value_objects, remuneration, base`. Nada de produto os importa; só há testes (que saem junto).
É a **maior redução com menor risco** — bom ponto de partida.

### Grupo B — INLINE (consumidor único) — ~20 arquivos
Mover a lógica para o único service que a usa e deletar o módulo:
`timeline, policies, coverage, financial, projections, analytics, explainability, kpi` (e
`payroll` com 2 consumidores). Mecânico; a suíte verde garante a paridade a cada passo.

### Grupo C — MANTER (fundação compartilhada)
`constants, errors, events`. Usados em dezenas de lugares; são a base legítima.

### Grupo D — AVALIAR (usado, mas é cerimônia) — esforço maior, por último
`read_models, query, rules, state_machines`. Além disso, a camada **`use_cases/`**
(assignments, periods) é outra camada intermediária que consome muito `domain` — forte
candidata a colapsar nos services.

## ⚠️ Alertas — VERIFICADOS em 2026-07-13

1. **remuneration (prod=0) → 🔴 GAP REAL CONFIRMADO.** A folha **não calcula valor** em lugar
   nenhum do produto:
   - `Payroll` (model) não tem campo de valor — só status/versão/timestamps; `create` só grava
     period/year_month.
   - `financial_fact`/`financial_snapshot` guardam **duração** (minutos), sem R$; o
     `financial_snapshot_builder` diz no docstring: *"Does NOT calculate values. Only consolidates
     rights."*
   - O único `hour_rate × duração = R$` está em `domain/remuneration/remuneration_calculator.py`,
     que tem **prod=0** (nunca chamado).
   - **Consequência**: deletar o motor `domain/remuneration` é seguro (morto), MAS a
     funcionalidade "calcular + exportar folha" (spec 001, US5) **nunca foi fiada**. Registrado
     como gap no backlog (B-06). Não é trabalho de "simplificação" — é feature a construir (de
     forma simples: função `duração × hour_rate` + campos de valor + exportação).

2. **overlap (prod=0) → ✅ NÃO é gap.** A detecção de sobreposição **existe e funciona**, porém
   **inline no `assignment_service.create()`** (não via `domain/overlap`): itera as alocações do
   mesmo dia e checa cruzamento de horário, tratando inclusive plantão que passa da meia-noite
   (`if existing_end <= existing_start: +24h`). Logo `domain/overlap` é **duplicata morta** →
   seguro deletar.

## Ordem sugerida de execução

1. **Grupo A** (deletar peso morto) — grande redução, risco baixo. *(resolver os 2 alertas antes)*
2. **Grupo B** (inline de consumidor único) — mecânico, incremental.
3. **Grupo D** (`read_models`/`query`, depois `rules`/`state_machines`, e colapsar `use_cases/`).
4. **Grupo C** permanece.

Estimativa: `domain/` de **118 → ~30-40 arquivos**, sem perder funcionalidade (paridade
garantida pela suíte verde da spec 003).
