# Quickstart — Validação da spec 007 (log de auditoria)

Roteiro para provar que a trilha grava o que deve, não grava o que não deve, e não quebra nada.
Pré-requisito: Docker funcionando.

## 1. Suíte de testes (gate de todo commit)

```bash
docker compose exec -T backend python -m pytest app/tests -q
```

**Baseline antes da feature (2026-08-07): 411 passed, 2 failed.**

As 2 falhas são `test_settings_factory.py::test_development_settings_defaults` e
`::test_production_settings_defaults` — **pré-existentes e ambientais** (dependem de `LOG_LEVEL` /
`SECRET_KEY` do contêiner de dev; falham também com o código desta feature revertido, verificado
por `git stash` em 2026-08-07). Não são regressão desta spec e não devem ser "corrigidas" aqui.

**Esperado ao final**: 411 + novos testes passando; as mesmas 2 falhas ambientais; **zero** falha
nova.

## 2. Migration (num banco limpo)

```bash
docker compose exec -T backend sh -c "alembic upgrade head && alembic downgrade -1 && alembic upgrade head"
```

**Esperado**: sobe até `011_audit_logs`, downgrade dropa a tabela, upgrade recria — sem erro.

Conferir o schema:

```bash
docker compose exec -T backend python -c "
from sqlalchemy import inspect
from app.database.session import engine
i = inspect(engine)
print('colunas:', [c['name'] for c in i.get_columns('audit_logs')])
print('indices:', [x['name'] for x in i.get_indexes('audit_logs')])
"
```

## 3. Gravação de ponta a ponta (US1 / SC-001, SC-002)

Subir o app e obter um token:

```bash
docker compose up -d
TOKEN=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@plantao360.local","password":"admin123"}' \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")
```

**3.1 — Criar, alterar e remover uma atribuição** (usar um `shift_id` válido da competência
corrente) e depois consultar a trilha:

```bash
curl -s "http://localhost:8000/api/v1/audit?resource=assignment&size=10" \
  -H "Authorization: Bearer $TOKEN" | python3 -m json.tool
```

**Esperado**: três registros (`create`, `update`, `delete`), mais recentes primeiro, cada um com
`user_label` do admin, `resource_id` da atribuição e:
- `create` → `before: null`, `after` preenchido
- `update` → `before` e `after` só com os campos que mudaram
- `delete` → `before` preenchido (o estado que existia), `after: null` ← **é o SC-002**

**3.2 — Hora extra**: criar e excluir uma hora extra e conferir os dois registros com médico,
duração e justificativa.

## 4. Senha nunca aparece na trilha (SC-006)

```bash
curl -s -X POST http://localhost:8000/api/v1/users -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Audit Teste","email":"audit.teste@x.com","password":"senha123","role":"CONSULTA"}' > /dev/null

curl -s "http://localhost:8000/api/v1/audit?resource=user&size=5" -H "Authorization: Bearer $TOKEN" \
  | grep -ci "password\|senha123" 
```

**Esperado**: `0` — nenhuma ocorrência de senha ou hash na resposta.

## 5. Bloqueio por perfil (SC-005)

```bash
TOK_MED=$(curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"<usuario MEDICO>","password":"<senha>"}' \
  | python3 -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/api/v1/audit -H "Authorization: Bearer $TOK_MED"
```

**Esperado**: `403`.

## 6. Interface (US3)

Frontend em http://localhost:3001.

**Como ADMIN** (`admin@plantao360.local` / `admin123`):
1. Abrir uma competência no workspace.
2. Abrir a aba de histórico → lista de eventos em ordem cronológica inversa, com autor, ação,
   alvo e horário.
3. Alterar um plantão na aba Planilha e voltar ao histórico → o evento novo aparece no topo.
4. Numa competência sem alterações → estado vazio informando desde quando a trilha existe.

**Como MEDICO**: a aba de histórico **não** aparece; as abas visíveis continuam sendo apenas
Planilha e Financeiro.

## 7. Paridade das jornadas (FR-011)

Percorrer, como ADMIN, sem nenhuma mudança de comportamento além da trilha passar a existir:
escala (incluir/mover/remover, duplicar dia e semana), horas extras, divisão de turno, cadastro de
médicos, usuários, competências, relatórios e dashboard.

Na **duplicação de semana**, conferir que a operação continua com o tempo de resposta de antes
(D2 do plan: `record_many` com um único `add_all`).
