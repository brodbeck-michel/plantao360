# Implementation Plan: Colapso final da camada `domain/` (Fase 2 — passo 3)

**Branch**: `005-colapso-domain-final` | **Date**: 2026-07-14 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification de `specs/005-colapso-domain-final/spec.md` + `docs/levantamento-domain.md`
+ os achados da spec 004 (cluster adiado).

## Summary

Terminar a redução de `app/domain/` (~53 arquivos) colapsando o **Grupo D** (`read_models`, `query`,
`rules`, `state_machines`), a camada `use_cases/` e o **cluster do agregado payroll**
(`coverage`, `financial`, `payroll_competency`, `base`, restos de `remuneration`/`value_objects`) —
**sem mudar comportamento nem contrato de API**. Mecânica: **inline-and-delete incremental** com a
suíte verde (638, spec 003/004) como juiz de paridade **entre cada passo**, mais uma **checagem
anti-inversão** (nenhum `domain/` passa a importar de `services/`). Nunca big-bang. Meta: `domain/`
**~53 → ~30–40** arquivos, fechando a Fase 2.

## Technical Context

**Language/Version**: Python 3.12 (backend FastAPI).

**Primary Dependencies**: sem novas dependências — refactor interno.

**Storage**: inalterado (mesmos models/migrations).

**Testing**: pytest via imagem `plantao360-backend-test`; a suíte é a rede de segurança. Atenção
extra aos testes de **comportamento** (transições de estado, decisões de regra) e de API.

**Target Platform**: backend; frontend e API pública **não** mudam.

**Project Type**: Web app (backend). Escopo: só a organização interna do código do backend.

**Performance Goals**: N/A (comportamento idêntico).

**Constraints**: paridade funcional total; nenhum contrato de API alterado; suíte verde a cada
passo; **nenhuma dependência domain→service**; sem tocar `constants`/`errors`/`events`/`exceptions`
(fundação); B-06 (cálculo de remuneração em R$) fora de escopo.

**Scale/Scope**: ~30 arquivos de `domain/` a colapsar (read_models 8, query 6, rules 3,
state_machines 5, coverage 1, financial 1, payroll 2, remuneration 3, value_objects 1, base 1) +
19 arquivos de `use_cases/` (assignments 10, periods 8, base 1). Meta: `domain/` → ~30–40 arquivos.

## Constitution Check

*GATE: antes da pesquisa e reavaliado após o design.*

| Princípio | Avaliação |
|---|---|
| **I. Simplicidade Deliberada** | ✅ Elimina as últimas camadas de cerimônia (read models, query objects, use_cases de repasse) e reúne regra/estado no seu dono; reduz para `rota→service→model`. |
| **II. Regra no Backend** | ✅ A regra continua no backend — só muda de lugar (do módulo/máquina para o service), sem vazar para o frontend. |
| **III. Testes do que Importa** | ✅ A suíte verde é o critério de paridade; testes de comportamento (transições/regras) e de API cobrem o que erra caro. |
| **IV. Deploy Confiável** | ✅ Sem impacto operacional. |
| **V. Foco no Usuário Real** | ✅ Mesma funcionalidade, menos custo de manutenção. |

**Resultado**: PASS. Nenhuma violação — Complexity Tracking vazio. (Nota: onde um `use_case` tiver
orquestração genuína, mantê-lo é permitido — o Princípio I é contra indireção vazia, não contra
orquestração legítima.)

## Project Structure

### Documentation (this feature)

```text
specs/005-colapso-domain-final/
├── plan.md              # Este arquivo
├── research.md          # Mecânica e decisões (Phase 0)
├── quickstart.md        # Como validar paridade a cada passo (Phase 1)
└── checklists/          # Checklist de qualidade da spec
```

**data-model.md / contracts/**: não se aplicam — não há entidades novas e os **contratos de API não
mudam** (a garantia é justamente essa). Registrado aqui em vez de arquivos vazios (Princípio I).

### Source Code (o que muda)

```text
backend/app/
├── domain/
│   ├── (CONSOLIDAR→service)  read_models, query        → query_service / dashboard_service
│   ├── (INLINE→service, por vertical)  rules, state_machines
│   ├── (COLAPSAR cluster)  coverage, financial → coverage_service;
│   │                       payroll (competency+governance) → payroll_service;
│   │                       remuneration (data classes), value_objects/shift_time_range
│   ├── (MOVER enum antes de deletar rules)  rules/business_rules.BusinessRuleCode → errors/constants
│   ├── (DELETAR por ÚLTIMO)  base  (AggregateRoot; só depois de competency + state_machines)
│   └── (MANTER)  constants, errors, events, exceptions
├── services/     # recebem a lógica (query/dashboard/coverage/payroll/assignment/shift/extra)
├── use_cases/    # colapsar nos services onde for repasse fino (assignments, periods)
└── tests/        # testes de comportamento permanecem; testes de módulo removido saem/adaptam
```

**Structure Decision**: mudança contida em `app/domain/**`, nos services consumidores, na camada
`use_cases/**`, no `validators/payroll_governance_validator.py` e nos testes. Nenhum model,
migration, rota ou schema de API é alterado. As **rotas de API** que hoje importam objetos `query`
passam a importá-los do service (direção `api→service`, permitida — não é inversão).

## Complexity Tracking

> Sem violações — seção vazia.

## Mecânica e ordem (detalhe em `/speckit-tasks`)

**Padrão por passo (o "loop" de segurança, herdado da spec 004 + anti-inversão):**
1. Confirmar (grep) os consumidores do alvo (produto, domain, tests).
2. Mover a lógica para o(s) service(s)/local certo; ajustar imports (inclusive rotas de API →
   passam a importar do service); adaptar/mover testes.
3. Limpar `__init__`/reexports que apontem para o removido.
4. **Rodar a suíte** → verde. `grep app.domain.<modulo>` em produto → 0. **`grep app.services backend/app/domain`
   → 0** (nenhuma inversão domain→service).
5. Commit do passo (incremento verde e reversível).

**Ordem (menor risco → maior; ver research.md para o porquê de cada uma):**
1. **US1 — read_models + query** (dados; padrão da spec 004). Objetos de leitura/consulta para
   `query_service`/`dashboard_service`; summaries mortos saem. Rotas de API passam a importar os
   `query` do service.
2. **US2+US4 por VERTICAL** (rules/state_machines são compartilhados com `use_cases` → colapsam
   juntos, um vertical por vez): **assignments** (`use_cases/assignments` + `assignment_rules` +
   `assignment_state_machine` → `assignment_service`), **periods** (`use_cases/periods` +
   `period_state_machine` → o service/use_case de período), **shift** (`shift_rules` +
   `shift_state_machine` → `shift_service`), **extra** (`extra_state_machine` → `extra_service`).
   Antes de deletar `rules`: mover `business_rules.BusinessRuleCode` para `errors`/`constants`
   (consumido pela fundação `errors`).
3. **US3 — cluster payroll**: `coverage`+`financial` → `coverage_service`; `payroll_competency`+
   `governance`+`payroll_state_machine` → `payroll_service` (validator passa a chamar o service);
   `remuneration` data classes e `value_objects/shift_time_range` caem com seus consumidores;
   **`base` (AggregateRoot) por ÚLTIMO** — só depois que `payroll_competency` e as state_machines
   que o herdam já foram colapsados (confirmar por grep que nada o importa).
4. **US5 — paridade final**: suíte 0 falhas; testes de API verdes; grep sem import quebrado nem
   invertido; `domain/` em ~30–40; app dev sobe e fluxos funcionam.

**Verificação de paridade (a cada passo e no fim):** suíte 0 falhas; testes de integração de API
verdes (contratos idênticos); `grep` sem imports quebrados **nem invertidos**; app dev sobe.

Ver [research.md](./research.md) (decisões/mecânica) e [quickstart.md](./quickstart.md) (validação).
