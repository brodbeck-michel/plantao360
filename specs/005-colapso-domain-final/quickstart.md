# Quickstart — Validar o colapso final da `domain/` (paridade)

Como validar cada passo do inline-and-delete e o resultado final. A implementação vem do
`/speckit-tasks` → `/speckit-implement`. Estende o quickstart da spec 004 com a **checagem
anti-inversão**.

## Pré-requisitos

- Docker funcionando; imagem de teste: `docker build -t plantao360-backend-test ./backend`.
- Suíte verde de partida (spec 004): **638 passed, 0 failed**.

## O loop de segurança (a cada módulo) — QUÁDRUPLO

```bash
# 1. quem consome o alvo? (produto / domain / tests)
grep -rnE "app\.domain\.<modulo>" backend/app --include=*.py

# 2. aplicar o passo: mover a logica para o service/local certo (inclui ajustar rotas de API
#    para importarem do service) e adaptar/mover testes  [feito na implementacao]

# 3. rebuild + suite verde
docker build -t plantao360-backend-test ./backend
docker run --rm -e ENVIRONMENT=test plantao360-backend-test python -m pytest -p no:cacheprovider -q

# 4a. nenhum import de produto quebrado para o modulo removido
grep -rnE "app\.domain\.<modulo>\b" backend/app --include=*.py | grep -v /tests/ || echo "OK: sem import de produto"

# 4b. ANTI-INVERSAO: nenhum modulo de domain importa de services
grep -rnE "app\.services" backend/app/domain --include=*.py || echo "OK: sem inversao domain->service"

# 5. commit do passo (incremento verde)
```

**Espera-se a cada passo**: suíte `0 failed / 0 errors`; grep 4a sem resultado em produto; grep 4b
sem resultado.

## Validação final

| Critério | Como verificar | Espera-se |
|---|---|---|
| **SC-001** suíte verde | rodar a suíte completa | 0 failed / 0 errors |
| **SC-002** sem import quebrado nem invertido | grep 4a (todos os módulos removidos) + grep 4b | nenhum resultado |
| **SC-003** contratos idênticos | `pytest app/tests/integration -q` (test_*_api) | verdes |
| **SC-004** redução | `find backend/app/domain -name '*.py' -not -name '__init__.py' | wc -l` | ~30–40 (de ~53) |
| **SC-005** app funciona | subir o dev (`docker compose -f docker-compose.yml up -d --build`) e percorrer escala/extras/cobertura/dashboard/períodos-folha/usuários | comportamento idêntico |

## Prova de que só o backend interno mudou

```bash
git diff --name-only <antes>..HEAD | grep -vE "backend/app/(domain|services|use_cases|validators)/|backend/app/tests/|specs/|docs/" \
  && echo "ATENCAO: mudanca fora do escopo" || echo "OK: so domain/services/use_cases/validators/tests"
```

Espera-se **nenhum** arquivo de `models`, `api/routes` (exceto ajuste de import de `query`),
`schemas`, migrations ou do `frontend/`.

## Atenção especial ao COMPORTAMENTO (Grupo D)

Diferente da spec 004 (data classes), aqui há estado e regras. Ao validar cada vertical:

- **Transições de estado**: um teste que exercia transição válida deve continuar passando; um que
  exercia transição inválida deve continuar recebendo o **mesmo** erro/mensagem.
- **Efeitos colaterais**: eventos emitidos e entradas de auditoria em cada transição devem
  permanecer (não só a checagem "pode transicionar").
- **Decisões de regra**: mesma entrada → mesma decisão (aceita/rejeita, mesmo valor/código).

## Se a suíte ficar vermelha num passo

Sinal confiável de regressão daquele passo. Opções: reverter o commit do passo, ou ajustar o inline
(a lógica movida deve ser equivalente ao comportamento anterior — inclusive efeitos colaterais). Não
seguir para o próximo módulo com a suíte vermelha.
