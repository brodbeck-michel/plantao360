# Quickstart — Validar o Baseline de Testes Verde

Como rodar a suíte e confirmar que ficou verde e confiável. A implementação vem do
`/speckit-tasks` → `/speckit-implement`.

## Pré-requisitos

- Docker funcionando.
- Imagem de teste: `docker build -t plantao360-backend-test ./backend` (camada de pip em cache).

## Rodar a suíte completa

```bash
docker build -t plantao360-backend-test ./backend
docker run --rm -e ENVIRONMENT=test plantao360-backend-test python -m pytest -p no:cacheprovider -q
```

**Antes** (baseline medido em 2026-07-13): `52 failed, 692 passed` + 1 erro de coleção
(`test_manifests`).

**Depois (esperado)**: `0 failed`, `0 errors`, coleção sem erro. (`--ignore` do
`test_manifests` deixa de ser necessário, pois o arquivo é removido.)

## Validações por frente

| Frente | Como verificar | Espera-se |
|---|---|---|
| **Auth integração** (SC-002/003) | `pytest app/tests/integration -q` | Todos os `test_*_api` passam (sem `401`) |
| **Cerimônia removida** (SC-004) | `pytest --collect-only -q` | Coleção sem erro; sem testes de "número mágico" |
| **Desatualizados** (SC-004) | `pytest app/tests/unit/test_doctor_mapper.py app/tests/unit/test_settings_factory.py -q` | Passam refletindo o schema/hardening atuais |
| **Gate de cobertura** (SC-001) | rodar a suíte completa | Não reprova por cobertura; número reflete o real |
| **Sem mudança de produto** (SC-005) | `git diff --name-only` | Só arquivos sob `app/tests/**` e `pyproject.toml` |

## Confirmar que nada de produto mudou

```bash
git diff --name-only origin/master..HEAD -- backend/app | grep -v '/tests/' || echo "OK: nenhum arquivo de app fora de tests"
```

Espera-se que apenas `backend/app/tests/**` (e `backend/pyproject.toml`) apareçam — nenhum
arquivo de `app/api`, `app/services`, `app/domain`, `app/models`.

## Registro da triagem (SC-004)

Ao final, cada um dos 52 testes que falhavam deve ter um destino documentado
(consertado / atualizado / removido) — no `tasks.md` e no resumo da implementação.

## Próximo passo

Com a suíte verde e confiável, a Fase 2 continua com o **colapso do `domain/`** (feature
seguinte): a partir daqui, qualquer teste que ficar vermelho durante o refactor é sinal
confiável de regressão.
