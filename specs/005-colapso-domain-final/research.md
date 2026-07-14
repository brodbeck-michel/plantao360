# Research — Colapso final da `domain/` (Grupo D + cluster payroll)

Decisões de mecânica (Decisão / Justificativa / Alternativas descartadas), ancoradas no mapa de
consumidores levantado em 2026-07-14 e na constituição. Estende as decisões da spec 004.

## D1 — Manter o loop inline-and-delete incremental (1 módulo/commit, suíte verde)

**Decisão**: mesma mecânica da spec 004 — cada módulo num passo isolado, suíte verde e commit; nunca
mover vários de uma vez.

**Justificativa**: comprovadamente segura na spec 004 (20 passos, 0 regressões). Com comportamento
em jogo (estado/regras), a rastreabilidade passo-a-passo é ainda mais valiosa.

**Alternativas descartadas**: big-bang — perde o sinal de qual passo regrediu.

## D2 — Verificação de paridade agora é QUÁDRUPLA (+ anti-inversão)

**Decisão**: o critério de "não quebrou" ganha um quarto check além dos três da spec 004:
1. Suíte `pytest` → 0 falhas / 0 erros.
2. `grep app.domain.<modulo>` em produto → 0 após remoção (sem import quebrado).
3. Testes de integração de API (`test_*_api`) verdes → contratos idênticos.
4. **`grep -rE "app\.services" backend/app/domain` → 0** (nenhum módulo de domain importa de service).

**Justificativa**: o risco novo desta feature é criar uma inversão domain→service ao colapsar o
cluster payroll (FR-008). O check 4 a detecta mecanicamente a cada passo.

**Alternativas descartadas**: confiar na revisão manual — não é prova.

## D3 — read_models e query: consolidar nos services; API importa `query` do service

**Decisão**: `read_models` (summaries) e `query` (query objects) vão para `query_service`/
`dashboard_service`. As **rotas de API** que hoje importam objetos `query` (`api/routes/query.py`,
`api/routes/dashboard.py`) passam a importá-los do service.

**Justificativa**: são data classes (padrão validado na spec 004). `api→service` é a direção normal
(a API já depende dos services), então não há inversão. Summaries sem consumidor de produto
(candidatos: `assignment_summary`, `period_summary`, `shift_summary` — confirmar no passo) saem como
peso morto (D3 da spec 004).

**Alternativas descartadas**: deixar os `query` num módulo próprio "compartilhado" API+service —
seria manter uma camada de consumidor múltiplo desnecessária.

## D4 — rules + state_machines colapsam POR VERTICAL, junto com os use_cases

**Decisão**: `assignment_rules`/`assignment_state_machine` são consumidos por `assignment_service`
**e** por vários `use_cases/assignments/*`; idem `period_state_machine` (service/use_case de
período), `shift_rules`/`shift_state_machine` (`shift_service`), `extra_state_machine`
(`extra_service`). Colapsar cada **vertical** como unidade: primeiro reduzir os `use_cases` daquele
vertical ao service (ou fazê-los consumir o service), de modo que a regra/máquina fique com **um**
consumidor, e só então inliná-la nesse service.

**Justificativa**: se inlinar a regra/máquina num service enquanto os `use_cases` ainda a importam,
os `use_cases` teriam de importar do service — arriscando inversão/duplicação. Tratar o vertical
inteiro mantém `rota→service→model` limpo. É o ponto onde US2 (rules/state) e US4 (use_cases) se
entrelaçam — por isso o plano os executa juntos por vertical, apesar de US4 ser P2 na spec.

**Alternativas descartadas**: (a) inlinar rules/state antes de mexer nos use_cases — cria consumo
múltiplo/inversão; (b) deixar use_cases intactos — mantém uma camada de cerimônia que a feature quer
remover.

## D5 — Mover `business_rules.BusinessRuleCode` para a fundação ANTES de deletar `rules`

**Decisão**: `domain/errors/error_catalog.py` importa `BusinessRuleCode` de
`domain/rules/business_rules`. `errors` é Grupo C (fundação, permanece). Antes de deletar `rules`,
mover `BusinessRuleCode` (enum/catálogo de códigos) para dentro de `errors` (ou `constants`), e
apontar os consumidores para o novo lar.

**Justificativa**: a fundação não pode depender de um módulo que será removido. O enum é
constante/catálogo — cabe naturalmente em `errors`/`constants` (Grupo C).

**Alternativas descartadas**: manter `rules` só por causa do enum — deixaria um módulo inteiro vivo
por uma constante; mover a constante é mais simples (Princípio I).

## D6 — Preservar o COMPORTAMENTO das máquinas de estado, não só a checagem

**Decisão**: ao inlinar uma `state_machine`, preservar **todos** os efeitos: transições permitidas/
proibidas, os erros/mensagens em transição inválida, e efeitos colaterais (eventos emitidos,
auditoria) que hoje acontecem no fluxo. O agregado `payroll_competency` mantém versões/selo/eventos
— essa semântica de agregado vai junto para `payroll_service`.

**Justificativa**: a regra inviolável é paridade de comportamento; uma máquina de estado é lógica,
não dado. A suíte de comportamento + API é o juiz.

**Alternativas descartadas**: reduzir a máquina a um dicionário de transições sem os efeitos —
perderia eventos/auditoria (regressão silenciosa).

## D7 — Cluster payroll: ordem interna e `base` por último

**Decisão**: dentro de US3: (a) `coverage`+`financial` → `coverage_service` (consumidor único de
produto); (b) `payroll_competency`+`governance`+`payroll_state_machine` → `payroll_service`, com o
`payroll_governance_validator` passando a chamar o service; (c) `remuneration` (data classes) e
`value_objects/shift_time_range` caem quando seus consumidores (competency; shift rules) já foram
colapsados; (d) **`base` (AggregateRoot) por ÚLTIMO** — só depois que `payroll_competency` e as
`state_machines` que o herdam já saíram, confirmando por grep que nada o importa.

**Justificativa**: é a ordem que dissolve o acoplamento sem deixar import quebrado nem invertido em
nenhum ponto intermediário (a razão pela qual a spec 004 adiou tudo isto junto).

**Alternativas descartadas**: remover `base`/DTOs cedo — quebra imports enquanto o agregado ainda
existe.

## D8 — `use_cases/` pode ficar parcialmente (orquestração legítima)

**Decisão**: onde um `use_case` for repasse fino para um service, colapsá-lo; onde houver
orquestração real (validação + autorização + auditoria + evento em sequência, como `BasePeriodUseCase`),
avaliar manter/simplificar sem forçar colapso que recrie complexidade no service.

**Justificativa**: Princípio I é contra indireção **vazia**, não contra orquestração que agrega
valor. O objetivo é remover cerimônia, não empurrar tudo para services gigantes.

**Alternativas descartadas**: colapsar `use_cases` 100% sempre — poderia inchar services e misturar
responsabilidades.

## Observações

- **Meta de tamanho**: com o Grupo D + cluster colapsados, `domain/` deve ficar só com `constants`,
  `errors`, `events`, `exceptions` (+ o que sobreviver de regra/estado genuíno que não caiba num
  service). Estimativa ~30–40 arquivos, fechando a meta 118→30–40 da Fase 2.
- **B-06 intocado**: mover/remover as data classes de `remuneration` não implementa a folha em R$;
  o gap permanece no backlog (a fórmula já foi resgatada na spec 004).
- **Baseline**: suíte em 638 passing (spec 004); número final menor só por testes de módulo removido,
  nunca por falha.
