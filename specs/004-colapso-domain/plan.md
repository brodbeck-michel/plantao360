# Implementation Plan: Colapso da camada `domain/` (Fase 2 — passo 2)

**Branch**: `004-colapso-domain` | **Date**: 2026-07-13 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/004-colapso-domain/spec.md` +
`docs/levantamento-domain.md`

## Summary

Reduzir a camada `app/domain/` (~118 arquivos) removendo peso morto (Grupo A, prod=0) e
colapsando abstrações de consumidor único (Grupo B) para dentro do único service que as usa —
**sem mudar comportamento nem contrato de API**. Mecânica: **inline-and-delete incremental**, com
a suíte verde (738 passando, spec 003) como juiz de paridade **entre cada passo**. Nunca big-bang.

## Technical Context

**Language/Version**: Python 3.12 (backend FastAPI).

**Primary Dependencies**: sem novas dependências — é refactor interno.

**Storage**: inalterado (mesmos models/migrations).

**Testing**: pytest via imagem `plantao360-backend-test`; a suíte é a rede de segurança.

**Target Platform**: backend; frontend e API pública **não** mudam.

**Project Type**: Web app (backend). Escopo: só a organização interna do código do backend.

**Performance Goals**: N/A (comportamento idêntico).

**Constraints**: paridade funcional total; nenhum contrato de API alterado; suíte verde a cada
passo; sem tocar `constants`/`errors`/`events` (fundação); sem tocar Grupo D nem a remuneração (B-06).

**Scale/Scope**: ~23 arquivos a deletar (Grupo A) + ~20 a inlinar (Grupo B); ~21 testes de
Grupo A saem junto. Meta: `domain/` → ~30–40 arquivos.

## Constitution Check

*GATE: antes da pesquisa e reavaliado após o design.*

| Princípio | Avaliação |
|---|---|
| **I. Simplicidade Deliberada** | ✅ É a aplicação direta: elimina abstração de consumidor único e peso morto; reduz profundidade para `rota→service→model`. |
| **II. Regra no Backend** | ✅ A regra continua no backend — apenas muda de lugar (do módulo para o service), sem sair para o frontend. |
| **III. Testes do que Importa** | ✅ A suíte verde é o critério de paridade; testes de módulo morto saem, mas o comportamento real segue coberto pelos testes de service/API. |
| **IV. Deploy Confiável** | ✅ Sem impacto operacional. |
| **V. Foco no Usuário Real** | ✅ Mesma funcionalidade, menos custo de manutenção. |

**Resultado**: PASS. Nenhuma violação — Complexity Tracking vazio.

## Project Structure

### Documentation (this feature)

```text
specs/004-colapso-domain/
├── plan.md              # Este arquivo
├── research.md          # Mecânica e decisões (Phase 0)
├── quickstart.md        # Como validar paridade a cada passo (Phase 1)
└── checklists/          # Checklist de qualidade da spec
```

**data-model.md / contracts/**: não se aplicam — não há entidades novas e os **contratos de API
não mudam** (a garantia é justamente essa). Registrado aqui em vez de arquivos vazios (Princípio I).

### Source Code (o que muda)

```text
backend/app/
├── domain/
│   ├── (DELETAR)  entities, services, reports, calendar, metrics, snapshots,
│   │              transitions, contracts, overlap, value_objects, remuneration, base
│   ├── (INLINE→service, depois deletar)  timeline, policies, coverage, financial,
│   │              projections, analytics, explainability, kpi, payroll
│   └── (MANTER)   constants, errors, events   (+ Grupo D intacto: read_models, query,
│                  rules, state_machines)
├── services/     # recebem a lógica inlinada (coverage_service, dashboard_service,
│                 #   query_service, payroll_service)
├── use_cases/    # policies inlina em use_cases/periods (Grupo D fica; só o policy entra)
└── tests/        # testes de módulos mortos saem; testes de comportamento permanecem
```

**Structure Decision**: mudança contida em `app/domain/**`, nos 4-5 services consumidores e nos
testes correspondentes. Nenhum model, migration, rota ou schema de API é alterado.

## Complexity Tracking

> Sem violações — seção vazia.

## Mecânica e ordem (detalhe em `/speckit-tasks`)

**Padrão por passo (o "loop" de segurança):**
1. Confirmar (grep) que o módulo-alvo não tem consumidor de produto **ou** tem exatamente um.
2. Grupo A: deletar o módulo + seus testes. Grupo B: mover a lógica para o único service, ajustar
   o import, adaptar/mover os testes; depois deletar o módulo.
3. Limpar qualquer `__init__`/reexport que aponte para o removido.
4. **Rodar a suíte** → tem que ficar verde. `grep app.domain.<modulo>` no código de produto → 0.
5. Commit do passo (incremento verde e reversível).

**Ordem (menor risco primeiro):**
1. **Grupo A** — deletar peso morto. `base` por ÚLTIMO no grupo (tem 4 usos internos: só cai
   depois que os módulos que o usam já saíram; confirmar por grep que nada remanescente o importa).
2. **Grupo B** — inline de consumidor único, um módulo por commit: começar pelos de 1 arquivo
   (`timeline`, `coverage`, `financial`, `policies`), depois os maiores (`projections`,
   `explainability`, `kpi`, `analytics`) e por fim `payroll` (2 consumidores: service + validator).

**Verificação de paridade (a cada passo e no fim):** suíte 0 falhas; testes de integração de API
verdes (contratos idênticos); `grep` sem imports quebrados; app dev sobe e fluxos funcionam.

Ver [research.md](./research.md) (decisões/mecânica) e [quickstart.md](./quickstart.md) (validação).
