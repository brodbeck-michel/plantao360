# Quickstart — Validar o colapso da `domain/` (paridade)

Como validar cada passo do inline-and-delete e o resultado final. A implementação vem do
`/speckit-tasks` → `/speckit-implement`.

## Pré-requisitos

- Docker funcionando; imagem de teste: `docker build -t plantao360-backend-test ./backend`.
- Suíte verde de partida (spec 003): **738 passed, 0 failed**.

## O loop de segurança (a cada módulo)

```bash
# 1. (Grupo A) o modulo nao tem consumidor de produto?  (esperado: nada)
grep -rE "app\.domain\.<modulo>" backend/app --include=*.py | grep -v "/domain/" | grep -v "/tests/"

# 2. aplicar o passo: deletar (Grupo A) ou inline+deletar (Grupo B)  [feito na implementacao]

# 3. rebuild + suite verde
docker build -t plantao360-backend-test ./backend
docker run --rm -e ENVIRONMENT=test plantao360-backend-test python -m pytest -p no:cacheprovider -q

# 4. nenhum import de produto quebrado para o modulo removido
grep -rE "app\.domain\.<modulo>\b" backend/app --include=*.py | grep -v "/tests/" || echo "OK: sem import de produto"

# 5. commit do passo (incremento verde)
```

**Espera-se a cada passo**: suíte `0 failed / 0 errors`; grep do passo 4 sem resultado em código
de produto.

## Validação final

| Critério | Como verificar | Espera-se |
|---|---|---|
| **SC-001** suíte verde | rodar a suíte completa | 0 failed / 0 errors |
| **SC-002** sem import quebrado | `grep -rE "app\.domain\.(entities\|services\|reports\|calendar\|metrics\|snapshots\|transitions\|contracts\|overlap\|value_objects\|remuneration\|base\|timeline\|policies\|coverage\|financial\|projections\|analytics\|explainability\|kpi\|payroll)" backend/app --include=*.py \| grep -v /tests/` | nenhum resultado em produto |
| **SC-003** contratos idênticos | `pytest app/tests/integration -q` (test_*_api) | verdes |
| **SC-004** redução | contar arquivos: `find backend/app/domain -name '*.py' -not -name '__init__.py'` | de ~118 para ~30–40 |
| **SC-005** app funciona | subir o dev (`docker compose -f docker-compose.yml up -d --build`) e percorrer escala/extras/dashboard/usuários | comportamento idêntico |

## Prova de que só o backend interno mudou

```bash
git diff --name-only <antes>..HEAD | grep -vE "backend/app/(domain|services|use_cases)/|backend/app/tests/|specs/" \
  && echo "ATENCAO: mudanca fora do escopo" || echo "OK: so domain/services/use_cases/tests"
```

Espera-se **nenhum** arquivo de `models`, `api/routes`, `schemas`, migrations ou do `frontend/`.

## Se a suíte ficar vermelha num passo

É sinal confiável de regressão daquele passo. Opções: reverter o commit do passo, ou ajustar o
inline (a lógica movida deve ser byte-a-byte equivalente ao comportamento anterior). Não seguir
para o próximo módulo com a suíte vermelha.
