# Implementation Plan: Baseline de Testes Confiável (Fase 2 — passo 1)

**Branch**: `003-baseline-de-testes` | **Date**: 2026-07-13 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `specs/003-baseline-de-testes/spec.md`

## Summary

Levar a suíte do backend de **692/744 (52 falhas + 1 erro de coleção)** para **verde e
confiável**, sem mudar comportamento do produto. Achado central da investigação: as ~42 falhas
de integração têm **uma única causa** — os testes montam um app FastAPI e sobrescrevem `get_db`,
mas **não** sobrescrevem a dependência de auth `get_current_user`, então os endpoints (protegidos
por `Depends(get_current_user)` / `require_role(...)`) retornam `401`. Como `require_role`
internamente depende de `get_current_user`, **sobrescrever apenas `get_current_user`** por um
usuário ADMIN falso destrava todos. O restante é deletar testes-cerimônia, atualizar fixtures
desatualizadas e relaxar o gate de cobertura.

## Technical Context

**Language/Version**: Python 3.12.

**Primary Dependencies**: pytest, FastAPI `TestClient`, SQLAlchemy (SQLite in-memory nos testes).

**Storage**: SQLite in-memory por teste (`ENVIRONMENT=test`); sem Postgres.

**Testing**: pytest; execução via imagem Docker (`plantao360-backend-test`).

**Target Platform**: suíte de testes do backend (não afeta runtime de produção).

**Project Type**: Web app (backend). Esta feature toca **apenas** testes e config de teste.

**Performance Goals**: N/A. Objetivo é confiabilidade (0 falhas, 0 erros de coleção).

**Constraints**: nenhuma mudança de comportamento do produto. Alterar somente `app/tests/**`,
`conftest.py` e configuração de pytest (`pyproject.toml`/`pytest.ini`).

**Scale/Scope**: ~52 testes falhando + 1 erro de coleção, distribuídos em ~13 arquivos.

## Constitution Check

*GATE: antes da pesquisa e reavaliado após o design.*

| Princípio | Avaliação |
|---|---|
| **I. Simplicidade Deliberada** | ✅ Fix de causa única (uma sobrescrita de dependência); deleta cerimônia em vez de "consertar" trivialidade. |
| **II. Regra no Backend** | ✅ N/A — não toca regra de negócio. |
| **III. Testes do que Importa** | ✅ É a materialização direta: consertar o que cobre comportamento, deletar o que testa número mágico. |
| **IV. Deploy Confiável** | ✅ Sem impacto operacional. |
| **V. Foco no Usuário Real** | ✅ Habilita a Fase 2 (simplificação) com segurança. |

**Resultado**: PASS. Sem violações → Complexity Tracking vazio.

## Project Structure

### Documentation (this feature)

```text
specs/003-baseline-de-testes/
├── plan.md              # Este arquivo
├── research.md          # Decisões técnicas (Phase 0)
├── quickstart.md        # Como validar o verde (Phase 1)
└── checklists/          # Checklist de qualidade da spec
```

**data-model.md / contracts/**: não se aplicam — feature de testes, sem entidades novas nem
contratos de API (Princípio I: não criar artefatos vazios).

### Source Code (arquivos afetados — apenas testes/config)

```text
backend/
├── app/tests/
│   ├── integration/
│   │   ├── conftest.py           # (novo) helper de auth compartilhado (override de get_current_user)
│   │   ├── test_extra_api.py      # aplica override de auth (10)
│   │   ├── test_period_api.py     # aplica override de auth (9)
│   │   ├── test_doctors_api.py    # aplica override de auth (8)
│   │   ├── test_assignment_api.py # aplica override de auth (8)
│   │   ├── test_shift_api.py       # aplica override de auth (6)
│   │   ├── test_database.py        # ajustar (1)
│   │   └── test_bootstrap.py       # ajustar (1)
│   └── unit/
│       ├── test_doctor_mapper.py       # atualizar fixture (specialty/doctor_type) (2)
│       ├── test_shift_service.py       # atualizar (1)
│       ├── test_settings_factory.py    # atualizar p/ hardening (1)
│       ├── test_manifests.py           # DELETAR (import manifest_loader inexistente)
│       ├── test_domain_events.py       # DELETAR asserção de contagem (1)
│       └── domain/
│           ├── test_shift_constants.py     # revisar/atualizar (1)
│           ├── test_remuneration_events.py # DELETAR contagem (1)
│           ├── test_payroll_events.py      # DELETAR contagem (1)
│           └── test_financial_events.py    # DELETAR contagem (1)
└── pyproject.toml (ou pytest.ini)     # relaxar --cov-fail-under
```

**Structure Decision**: mudança contida em `backend/app/tests/**` + config de pytest. Nenhum
arquivo de aplicação (`app/api`, `app/services`, `app/domain`, `app/models`) é alterado.

## Complexity Tracking

> Sem violações — seção vazia.

## Abordagem por frente (detalhe em `/speckit-tasks`)

1. **Auth nos testes de integração** (FR-002, ~42): helper compartilhado em
   `app/tests/integration/conftest.py` que instala
   `app.dependency_overrides[get_current_user] = lambda: <User ADMIN falso>`. Cada `client`
   fixture existente passa a aplicá-lo (uma linha). Resolve router-level e `require_role`.
2. **Deletar cerimônia** (FR-003): remover `test_manifests.py` e as asserções de contagem
   (`test_domain_events`, `test_remuneration_events`, `test_payroll_events`; revisar
   `test_shift_constants`). Antes de deletar, confirmar que não há asserção de comportamento real.
3. **Atualizar desatualizados** (FR-004): fixtures de `test_doctor_mapper` (incluir
   `specialty`/`doctor_type`), `test_shift_service`, e `test_settings_factory` (refletir o
   hardening — segredo forte ou asserção de que rejeita fraco).
4. **Gate de cobertura** (FR-005): relaxar `--cov-fail-under=80` para um valor realista do estado
   atual (ou remover o gate rígido), sem mascarar cobertura.
5. **Fechamento** (FR-001/006/007): suíte 0 falhas / 0 erros; qualquer skip com justificativa;
   registrar o destino de cada teste.

Ver [research.md](./research.md) (decisões) e [quickstart.md](./quickstart.md) (validação).
