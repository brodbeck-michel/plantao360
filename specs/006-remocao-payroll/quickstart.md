# Quickstart — Validação da spec 006 (remoção payroll/cobertura)

Roteiro para provar, de ponta a ponta, que a remoção não mudou nada que o usuário usa.
Pré-requisito: Docker funcionando.

## 1. Suíte de testes (gate de todo commit)

```bash
docker build -t plantao360-backend-test ./backend
docker run --rm -e ENVIRONMENT=test plantao360-backend-test python -m pytest -p no:cacheprovider -q
```

**Esperado**: 0 falhas / 0 erros (total diminui ~17 arquivos vs. 632 — só testes do código removido).

## 2. Migration (num banco limpo)

```bash
docker run --rm -e ENVIRONMENT=test plantao360-backend-test sh -c "alembic upgrade head && alembic downgrade -1 && alembic upgrade head"
```

**Esperado**: sobe até `008_drop_payroll`, downgrade recria `payrolls`, upgrade droppa de novo — sem erro.

## 3. App dev no navegador (SC-001/SC-002)

```bash
docker compose -f docker-compose.yml up -d --build
# frontend: http://localhost:3001 · Swagger: http://localhost:8000/api/v1/docs
# login dev: admin@plantao360.local / admin123
```

Percorrer e comparar com o comportamento anterior:

1. **Login** e navegação por todas as abas (dashboard, períodos, escala/turnos, extras, usuários).
2. **Aba Relatórios**: gerar Escala PDF, Escala Excel, Escala CSV e Análise de Cobertura para a
   mesma competência usada antes da remoção → conteúdo idêntico (SC-002).
3. **Dashboard**: todos os cards carregam; `/api/v1/query/dashboard` responde 200.
4. **Swagger**: grupos *Payrolls* e *Coverage* não existem mais; grupos vivos inalterados.
5. **API removida**: `curl http://localhost:8000/api/v1/payrolls` → **404** (sem 500).

## 4. Greps de encerramento (SC-003, US3)

```bash
# nenhum import de produto quebrado
docker run --rm plantao360-backend-test python -c "import app.main"
# payroll só em histórico (docs/specs/migrations)
git grep -il payroll -- backend/app frontend/src
# domain/ só fundação
git ls-files "backend/app/domain/*.py"
```

**Esperado**: import OK; grep sem resultados em código de produção; `domain/` contém apenas
`constants/`, `errors/`, `events/`, `exceptions/` (e nenhum deles órfão).

## 5. Produção (quando for deployar)

1. `./scripts/backup.sh` (obrigatório — a migration droppa `payrolls`).
2. Deploy normal: `TAG=vX ./scripts/deploy.sh` (migrations aplicam no boot).
3. Repetir o passo 3 no ambiente de produção.
