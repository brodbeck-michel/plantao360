# Implementation Plan: Remoção da superfície payroll/cobertura sem uso (B-07)

**Branch**: `006-remocao-payroll` | **Date**: 2026-07-15 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/006-remocao-payroll/spec.md`

## Summary

Remover de ponta a ponta a superfície payroll/cobertura que **nenhum usuário usa** (decisão do
stakeholder, 2026-07-15): rotas, services, schemas, repositories, validators, modelos, tabela
`payrolls` (migration reversível + backup) e o cluster `domain/` que só existia para servi-la.
O research ampliou o inventário com dois blocos mortos descobertos: **`routes/query.py` +
`query_service.py`** (router nunca registrado — código inalcançável) e **`integrations/`**
(scaffolding de ERPs consumido só pelo próprio teste). Total: **~70 arquivos / ~6.600 linhas de
produção removidas**, sem nenhuma mudança observável nas jornadas vivas. Detalhes e evidências:
[research.md](research.md); estado do banco: [data-model.md](data-model.md).

## Technical Context

**Language/Version**: Python 3.12 (backend), TypeScript/React 18 (frontend — só limpeza de constantes mortas)

**Primary Dependencies**: FastAPI, SQLAlchemy 2, Alembic, Pydantic; React Query/MUI (intocados)

**Storage**: Postgres (produção) / SQLite (dev/teste). Migration `008_drop_payroll` (drop + downgrade recria)

**Testing**: pytest via Docker (`plantao360-backend-test`); suíte atual 632 verde + 93 de API

**Target Platform**: intranet Docker Compose (imagens via GHCR)

**Project Type**: web app (backend + frontend)

**Performance Goals**: N/A (remoção; nenhum caminho quente alterado)

**Constraints**: paridade estrita das jornadas vivas (FR-005); remoção incremental com suíte verde por commit (FR-007); backup antes do deploy (FR-002)

**Scale/Scope**: ~70 arquivos / ~6.600 linhas de produção + 17 arquivos de teste do código removido

## Constitution Check

*GATE: aprovado (pré-research e re-avaliado pós-design — sem violações).*

- **I. Simplicidade Deliberada**: é a materialização do princípio — remoção líquida, não
  relocação. Nenhuma abstração nova entra.
- **II. Regra de negócio no backend**: nenhuma regra viva muda de lugar. (O cálculo do relatório
  já era client-side antes desta feature; corrigi-lo é fora de escopo — anotado no backlog.)
- **III. Testes do que importa**: testes removidos são exclusivamente do código removido;
  nenhum teste de fluxo vivo é alterado. Suíte verde é gate de cada commit.
- **IV. Deploy Confiável**: tabela sai por migration versionada e reversível; backup prévio
  documentado; imagem construída no CI como sempre.
- **V. Foco no Usuário Real**: remove-se exatamente o que nenhum usuário percorre.

**Complexity Tracking**: N/A — nenhuma violação a justificar.

## Project Structure

### Documentation (this feature)

```text
specs/006-remocao-payroll/
├── spec.md
├── plan.md              # este arquivo
├── research.md          # Fase 0 — riscos resolvidos + inventário consolidado
├── data-model.md        # Fase 1 — tabelas/modelos removidos, estado final da domain/
├── quickstart.md        # Fase 1 — roteiro de validação
├── checklists/requirements.md
└── tasks.md             # Fase 2 (/speckit-tasks — não criado pelo plan)
```

### Source Code (repository root) — alvos da remoção

```text
backend/app/
├── api/app.py                        # remover registros/imports coverage, payroll (query nunca foi registrado)
├── api/routes/{payroll,coverage,query}.py          # deletar
├── services/{payroll,coverage,query}_service.py    # deletar
├── schemas/payroll/                                # deletar (6 arquivos)
├── repositories/{payroll,coverage_snapshot,financial_snapshot,financial_fact}_repository.py  # deletar
├── models/{payroll,coverage_snapshot,financial_snapshot,financial_fact}.py + __init__.py     # deletar/editar
├── validators/payroll_governance_validator.py      # deletar (morto)
├── seed/seed_data.py                               # remover import morto de Payroll
├── domain/{payroll,coverage,financial,remuneration,base,state_machines}/                     # deletar
├── domain/constants/{payroll_status,snapshot_status,financial_fact_status,financial_fact_type,inconsistency_type,rule_status}.py  # deletar (órfãs)
├── domain/errors/payroll_errors.py                 # deletar (verificar error_catalog)
├── domain/events/event_names.py                    # editar: remover nomes PAYROLL_*/COVERAGE_*/FINANCIAL_* mortos
├── integrations/                                   # deletar pacote inteiro (28 arquivos)
└── tests/…                                         # 17 arquivos de teste do código removido (research R7)

backend/alembic/versions/
└── 20260715_008_drop_payroll.py                    # nova migration (drop + downgrade recria payrolls)

frontend/src/
├── routes/routes.ts                                # remover ROUTES.PAYROLL*/COVERAGE*/READINESS mortos
├── services/query-keys.ts                          # remover queryKeys.payroll / query.payroll / kpi.payroll
├── shared/components/operational/OperationalEmptyState.tsx  # remover contexto 'payroll'
└── App.tsx                                         # remover rota READINESS→DashboardPage se confirmada morta
```

**Structure Decision**: estrutura existente (backend + frontend); nenhum diretório novo. A única
adição é a migration 008.

## Estratégia de execução (Fase 2 gera tasks a partir daqui)

Ordem **de fora para dentro** (o inverso do inline-and-delete): primeiro a borda HTTP, depois
services, depois dados, depois a `domain/` — assim cada commit remove só código já inalcançável,
e a suíte fica verde em todos os passos.

1. **US1a — Borda HTTP**: deregistrar e deletar `routes/{payroll,coverage,query}.py`; editar
   `app.py`. Gate: suíte verde; Swagger sem as rotas; 93 testes de API vivos intactos.
2. **US1b — Services e apoio**: deletar `payroll_service`, `coverage_service`, `query_service`,
   validator morto, `schemas/payroll/`, 4 repositories. Gate: suíte verde; grep sem import.
3. **US1c — Dados**: deletar 4 modelos + entradas no `models/__init__` + import morto no seed;
   migration `008_drop_payroll` (drop `payrolls`; drop condicional das 3 tabelas de snapshot;
   downgrade recria `payrolls` conforme migration 003). Gate: suíte verde; `alembic upgrade head`
   e `downgrade -1` funcionam num banco limpo.
4. **US2 — Cluster `domain/`**: deletar `payroll/`, `coverage/`, `financial/`, `remuneration/`,
   `base/`, `state_machines/` + testes correspondentes; depois varrer fundação órfã (constants
   R6, `payroll_errors`, nomes de evento mortos). Gate: suíte verde; todo arquivo restante em
   `domain/` tem consumidor de produção.
5. **US3 — Resíduos**: deletar `integrations/` + teste de arquitetura; limpar constantes mortas
   do frontend (sem mudança visual — o rótulo "Payroll: Pendente" hardcoded fica, anotado para o
   lote B-02/B-04). Gate: `grep -i payroll` só encontra docs/specs/migrations históricas;
   build do frontend passa.
6. **Encerramento**: validação no navegador (quickstart), atualizar backlog (B-07 encerrado),
   HANDOFF e nota de escopo na spec 001; release note com aviso de backup.

**Verificação de paridade (tripla, padrão specs 004/005)**: suíte 0 falhas por commit + grep de
imports quebrados + testes de API vivos sem modificação. Validação final no navegador conforme
[quickstart.md](quickstart.md).

**Riscos e mitigação**:
- *Tabela `payrolls` com dados em produção* → backup obrigatório antes do deploy (release note);
  downgrade recria schema.
- *Import esquecido* (ex.: `error_catalog`, re-exports em `__init__`) → gate de grep por commit.
- *Frontend build quebrar por constante removida* → US3 roda `vite build` como gate.
