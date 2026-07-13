# Research — Colapso da `domain/`

Decisões de mecânica (Decisão / Justificativa / Alternativas descartadas). Ancoradas no
levantamento e na constituição.

## D1 — Inline-and-delete incremental, um módulo por commit

**Decisão**: cada módulo é tratado num passo isolado, seguido de suíte verde e commit. Nunca
mover vários de uma vez.

**Justificativa**: a suíte verde só é útil como rede se rodar **entre** passos pequenos — assim,
se algo ficar vermelho, sabe-se exatamente qual passo causou. Cada commit é reversível.

**Alternativas descartadas**: big-bang (deletar tudo e consertar depois) — perde a rastreabilidade
e transforma a suíte num muro de falhas sem sinal claro.

## D2 — Verificação de paridade objetiva a cada passo

**Decisão**: o critério de "não quebrou" é triplo e mecânico:
1. Suíte `pytest` → **0 falhas / 0 erros**.
2. `grep app.domain.<modulo>` no código de produto (fora de `domain/` e `tests/`) → **0** após a
   remoção (nenhum import quebrado).
3. Testes de integração de API (`test_*_api`) verdes → contratos idênticos.

**Justificativa**: paridade tem que ser **provada**, não presumida (FR-003/004). Os três checks
cobrem comportamento (suíte), integridade de imports (grep) e contrato (API tests).

**Alternativas descartadas**: revisão manual "parece ok" — não é prova.

## D3 — Grupo A: deletar módulo + seus testes juntos

**Decisão**: ao remover um módulo morto (prod=0), remover também os testes que existiam **apenas
para ele** (medidos: overlap 1, remuneration 6, value_objects 5, calendar/metrics/snapshots/
transitions 1 cada, contracts 2, base 3).

**Justificativa**: esses testes cobrem o **módulo morto**, não comportamento de produto (que não
os usa). Mantê-los seria testar código que não existe mais. O comportamento real (ex.: overlap)
já é coberto pelos testes de service/API.

**Alternativas descartadas**: manter os testes — quebrariam a coleção (imports para módulos
removidos) e não agregam valor.

## D4 — `base` sai por último no Grupo A

**Decisão**: `domain/base` (aggregate_root) só é removido depois que todos os módulos que o
importam já saíram; confirmar por `grep app.domain.base` que nada remanescente o usa.

**Justificativa**: o levantamento mostra `base` com prod=0 mas **dom=4** (usos internos por outros
módulos de domain). Alguns desses podem ser de módulos que ficam temporariamente; remover `base`
antes deles quebraria imports.

**Alternativas descartadas**: remover `base` cedo — risco de import quebrado até o resto sair.

## D5 — Grupo B: mover a lógica para o único service, não criar módulo novo

**Decisão**: a lógica de um módulo de consumidor único é **embutida** no service que a usa (como
funções/métodos privados ou trechos no fluxo), e o módulo é deletado. Não se cria um novo módulo
"helper".

**Justificativa**: Princípio I — abstração de consumidor único é indireção; o lugar da lógica é o
consumidor. Reduz a profundidade para `rota→service→model`.

**Alternativas descartadas**: renomear/mover o módulo para outra pasta — continuaria sendo camada
extra de consumidor único.

## D6 — `payroll` (2 consumidores) tratado com cuidado

**Decisão**: `domain/payroll` tem 2 consumidores (`payroll_service` + `payroll_governance_validator`).
Inlinar a parte usada por cada um; se a lógica for genuinamente compartilhada entre os dois,
mantê-la em **um** lugar (o service) e o validator passa a chamá-lo — sem módulo `domain/payroll`.

**Justificativa**: 2 consumidores próximos ainda cabem em "colapsar", desde que não se recrie a
indireção. Avaliar no momento do passo.

**Alternativas descartadas**: deixar `payroll` para o Grupo D — desnecessário; é pequeno (2 arqs).

## D7 — Não tocar `constants`/`errors`/`events` nem Grupo D

**Decisão**: fora do escopo. `constants`/`errors`/`events` são fundação (dezenas de consumidores);
`read_models`/`query`/`rules`/`state_machines` e `use_cases/` ficam para uma feature seguinte.

**Justificativa**: manter o escopo pequeno e de baixo risco; o Grupo D exige análise de
comportamento (regras/transições) que merece sua própria spec.

## Observações

- **Remuneração (B-06)**: deletar `domain/remuneration` remove o motor morto, mas **não**
  implementa a folha. Antes de deletar, vale copiar a fórmula útil (`hour_rate × duração`) para o
  backlog/rascunho da futura feature, para não reinventar. O gap permanece no backlog.
- **`policies` → `use_cases/periods`**: `use_cases/` é Grupo D (fica), mas o módulo `policies`
  (consumidor único ali) pode ser inlinado agora; a camada `use_cases/` em si é avaliada depois.
- **Baseline**: suíte em 738 passing (spec 003); qualquer número menor de passing ao final deve
  ser explicado (testes de módulo morto removidos reduzem o total, mas não pode haver falhas).
