# Feature Specification: Colapso final da camada `domain/` (Fase 2 — passo 3)

**Feature Branch**: `005-colapso-domain-final`

**Created**: 2026-07-14

**Status**: Draft

**Input**: Terminar a simplificação da camada `app/domain/` colapsando o que sobrou da spec 004 —
o **Grupo D** do levantamento (`read_models`, `query`, `rules`, `state_machines`), a camada
`use_cases/`, e o **cluster acoplado adiado** (`coverage → financial → payroll_competency` + `base`
+ restos vivos de `remuneration`/`value_objects`) — com **paridade funcional total**, protegido pela
suíte verde (638, spec 003/004).

---

## Contexto e Objetivo

A spec 004 (Grupos A+B) reduziu `app/domain/` de **88 → 53** arquivos removendo peso morto e
inlinando abstrações de consumidor único que eram, na prática, data classes. Deliberadamente adiou
um **cluster acoplado** cujo colapso exige tratar **comportamento** (não só dados): as máquinas de
estado (`state_machines`), as regras (`rules`), e o agregado `payroll_competency` que amarra
`coverage`, `financial`, `base`, `remuneration` e `value_objects/shift_time_range`.

Esta feature termina o colapso: leva `domain/` de **~53 para ~30–40** arquivos, deixando apenas a
fundação legítima (`constants`, `errors`, `events`) e o que codifica regra/estado de negócio real —
agora no lugar certo (dentro dos services), sem camadas de cerimônia. **Sem alterar nenhum
comportamento observável do produto**: mesmas telas, mesmos endpoints, mesmos resultados.

**Diferença-chave vs spec 004**: lá, mover era quase sempre `dataclass + to_dict`. Aqui há
**comportamento real** — transições de estado permitidas e regras de negócio. Preservá-lo
exatamente é a regra inviolável; a suíte verde é o juiz, com atenção redobrada a `state_machines` e
`rules`.

**Fora de escopo**: `constants`/`errors`/`events` (fundação, permanecem); o **cálculo de
remuneração em R$** (gap B-06 — feature separada; deletar/mover as data classes de `remuneration`
**não** implementa a folha); frontend; contratos de API (não mudam).

---

## User Scenarios & Testing *(mandatory)*

Stakeholder: o **mantenedor** (você/eu). Valor: uma base final enxuta e barata de manter, com a
mesma funcionalidade para os usuários (médico/gestão) e sem dependências invertidas.

### User Story 1 - Consolidar read models e query objects nos services (Priority: P1)

Os módulos de leitura `read_models` e `query` — objetos de dados/consulta consumidos pelos services
de leitura — são movidos para dentro desses services e removidos, eliminando a camada intermediária.

**Why this priority**: é a maior fatia de baixo risco do que resta (dados, padrão já validado na
spec 004), e reduz `domain/` de forma imediata.

**Independent Test**: após mover os objetos de `read_models`/`query` para `dashboard_service`/
`query_service` e deletá-los, a suíte segue verde e os endpoints de dashboard/consulta retornam o
mesmo resultado.

**Acceptance Scenarios**:

1. **Given** um objeto de `read_models` ou `query` usado por um único service, **When** ele é
   embutido no service e o módulo é removido, **Then** a suíte continua com 0 falhas e o endpoint
   correspondente retorna resposta idêntica.
2. **Given** um objeto de leitura usado por mais de um service, **When** o cluster é colapsado,
   **Then** ele passa a viver em **um** lugar sem recriar uma camada de consumidor único.

---

### User Story 2 - Colapsar rules e state_machines preservando o comportamento (Priority: P1)

As regras (`rules`) e máquinas de estado (`state_machines`) — que codificam **transições permitidas
e regras de negócio reais** — são movidas para dentro dos services/agregados que as usam, sem alterar
nenhuma transição ou decisão de regra.

**Why this priority**: é o coração comportamental do Grupo D; colapsá-la corretamente é o que torna
a simplificação segura. É também o maior risco — por isso tem verificação reforçada.

**Independent Test**: após inlinar uma regra/máquina de estado no seu consumidor, os testes de
comportamento (transições válidas/inválidas, decisões de regra) e os de API passam idênticos.

**Acceptance Scenarios**:

1. **Given** uma máquina de estado (ex.: período, plantão, alocação, folha), **When** sua lógica de
   transições é movida para o service/agregado consumidor, **Then** toda transição que era permitida
   continua permitida e toda proibida continua proibida (mesmos erros).
2. **Given** uma regra de negócio, **When** ela é embutida no consumidor, **Then** a decisão da regra
   (aceita/rejeita, mesmo valor/mensagem) é idêntica à de antes.

---

### User Story 3 - Colapsar o cluster do agregado payroll resolvendo o acoplamento (Priority: P1)

O cluster adiado pela spec 004 — `coverage`, `financial`, o agregado `payroll_competency`
(`domain/payroll`), e as peças que ele amarra (`base`/AggregateRoot, data classes de `remuneration`,
`value_objects/shift_time_range`) — é colapsado **junto**, movendo a lógica para os services
(`coverage_service`, `payroll_service`) de forma que **nenhuma dependência fique invertida**
(domain → service).

**Why this priority**: era o nó que impedia o fechamento na spec 004; resolvê-lo é o que permite
remover `base` e os restos vivos e atingir a meta de tamanho.

**Independent Test**: após o colapso, `payroll_service` produz os mesmos resultados de folha
(ciclo draft→review→approve→export, versões, selo, auditoria, governança) e `coverage_service`
consolida igual; a suíte e os testes de API seguem verdes; nenhum módulo de `domain/` importa de um
service.

**Acceptance Scenarios**:

1. **Given** o agregado `payroll_competency` e seus colaboradores (`coverage`/`financial`/`base`/
   `remuneration` DTOs), **When** a lógica é consolidada nos services, **Then** o comportamento da
   folha e da cobertura é idêntico e nenhum import domain→service permanece.
2. **Given** a remoção de `base` (AggregateRoot), **When** todos os seus consumidores já foram
   colapsados, **Then** nenhum import remanescente o referencia e a suíte segue verde.
3. **Given** que as data classes de `remuneration` são movidas/removidas, **When** o passo é feito,
   **Then** a folha **continua sem calcular valor em R$** — o gap B-06 permanece intacto e separado
   (esta feature não o implementa nem o piora).

---

### User Story 4 - Colapsar a camada `use_cases/` nos services (Priority: P2)

A camada intermediária `use_cases/` (assignments, periods) — que orquestra chamando muito `domain`
— é avaliada e colapsada nos services correspondentes quando for um repasse fino, mantendo a
orquestração real onde ela agrega valor.

**Why this priority**: reduz mais uma camada de indireção (Princípio I), mas depende de US1–US3
estarem feitas (o `use_cases` consome as peças colapsadas ali); por isso P2.

**Independent Test**: após colapsar um use_case no seu service, o endpoint que o aciona responde
idêntico e a suíte segue verde.

**Acceptance Scenarios**:

1. **Given** um use_case que é repasse fino para um service, **When** sua lógica é movida para o
   service e o use_case é removido, **Then** a rota correspondente retorna o mesmo resultado.
2. **Given** um use_case com orquestração genuína, **When** avaliado, **Then** ele é mantido (ou
   simplificado) sem perder comportamento — não se força colapso que recrie complexidade.

---

### User Story 5 - Garantir paridade e não-regressão (Priority: P1)

Ao final, a aplicação entrega exatamente as mesmas funcionalidades e contratos de API de antes, e
isso é **comprovado** — suíte verde, contratos idênticos, sem imports quebrados nem invertidos, e o
app dev funcionando.

**Why this priority**: paridade funcional é a regra inviolável desta fase; sem prova, a
simplificação não é confiável — ainda mais tratando comportamento (estado/regras).

**Independent Test**: a suíte (spec 003/004) permanece verde; os testes de integração de API
permanecem verdes (contratos idênticos); `grep` não acha import de produto quebrado **nem** import
domain→service; o app dev sobe e os fluxos principais funcionam.

**Acceptance Scenarios**:

1. **Given** o colapso concluído, **When** a suíte completa roda, **Then** 0 falhas e 0 erros.
2. **Given** o colapso concluído, **When** os endpoints são comparados, **Then** rotas e formatos de
   resposta são idênticos.
3. **Given** o colapso concluído, **When** se conta `domain/`, **Then** há **~30–40** arquivos
   (de ~53), sem perder funcionalidade.

---

### Edge Cases

- **Comportamento escondido numa transição/regra**: ao inlinar uma máquina de estado, se uma
  transição tinha efeito colateral (evento emitido, auditoria), o efeito deve ser preservado no novo
  local — não só a checagem de "pode transicionar".
- **Peça com consumo transitivo remanescente**: como na spec 004, uma peça "de consumidor único"
  pode ter um consumidor domain-interno escondido; ela **não** é removida até todos os usos serem
  tratados (por isso o cluster do payroll colapsa junto).
- **`base` cedo demais**: `base` (AggregateRoot) só sai depois que `payroll_competency` e as
  máquinas de estado que o herdam já foram colapsados; confirmar por grep que nada o importa.
- **Inversão de dependência**: nenhum módulo de `domain/` pode passar a importar de `services/` —
  se um passo levaria a isso, a ordem/estratégia é ajustada para que a dependência fique
  service→service ou service→domain (nunca o contrário).
- **Gap de remuneração (B-06)**: mover/remover as data classes de `remuneration` não cria nem quita
  a folha em R$; o gap continua registrado no backlog, separado desta feature.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Os módulos de leitura `read_models` e `query` DEVEM ser consolidados nos services que
  os consomem e removidos de `domain/`.
- **FR-002**: As `rules` e `state_machines` DEVEM ser movidas para dentro dos seus consumidores
  **preservando exatamente** as transições permitidas/proibidas e as decisões de regra (mesmos
  resultados, erros e efeitos colaterais).
- **FR-003**: O cluster `coverage`/`financial`/`payroll_competency`/`base`/restos de `remuneration`
  e `value_objects` DEVE ser colapsado nos services (`coverage_service`, `payroll_service`) de forma
  que **nenhuma dependência fique invertida** (domain → service).
- **FR-004**: A camada `use_cases/` DEVE ser colapsada nos services onde for repasse fino; onde
  houver orquestração genuína, PODE ser mantida/simplificada sem perda de comportamento.
- **FR-005**: Nenhum comportamento observável do produto PODE mudar — mesmas telas, mesmas
  transições/regras, mesmos resultados.
- **FR-006**: Os contratos de API (rotas e formatos de resposta) DEVEM permanecer idênticos.
- **FR-007**: A suíte de testes DEVE permanecer verde (0 falhas / 0 erros) **a cada passo**
  incremental — inline-and-delete, nunca big-bang.
- **FR-008**: Ao final, NÃO PODE haver import de produto apontando para módulo removido, **nem**
  import de `domain/` apontando para `services/`.
- **FR-009**: Os módulos de fundação (`constants`, `errors`, `events`) DEVEM permanecer.
- **FR-010**: O cálculo de remuneração em R$ (B-06) NÃO faz parte desta feature; a folha continua
  sem calcular valor ao final dela.

### Key Entities

Não há novas entidades de dados. A "entidade" afetada é a **estrutura de código** do backend — a
camada `domain/` restante (leitura, regras, estado, agregado payroll) e os services/`use_cases` que
a consomem. Nenhum model, migration, rota ou schema de API muda.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A suíte termina com **0 falhas e 0 erros** (igual ou melhor que o baseline de 638
  passando; total pode variar só por testes de módulo removido, nunca por falha).
- **SC-002**: **0 imports de produto** para módulos removidos **e 0 imports domain→service**
  (verificável por busca).
- **SC-003**: Os contratos de API permanecem idênticos (mesmas rotas e formatos), verificável pelos
  testes de integração de API que já passam.
- **SC-004**: A camada `domain/` reduz de **~53 para ~30–40** arquivos ao final desta feature, sem
  perder funcionalidade — fechando a meta original de 118 → 30–40 da Fase 2.
- **SC-005**: O app dev sobe e os fluxos principais (escala, extras, cobertura, dashboard,
  períodos/folha, usuários) funcionam exatamente como antes.
- **SC-006**: Cada passo de colapso é um incremento com a suíte verde (rastreável no histórico de
  commits).

---

## Assumptions

- **A suíte verde é a rede de segurança**: 638 passando (spec 003/004) é o critério objetivo de
  paridade a cada passo; comportamento de estado/regra é coberto pelos testes de service/API.
- **O levantamento e a spec 004 são a fonte de escopo**: o Grupo D e o cluster adiado definem o que
  entra; `constants`/`errors`/`events` ficam de fora (fundação).
- **Ordem de menor risco primeiro**: US1 (read_models/query, dados) antes de US2 (rules/state) e US3
  (cluster payroll); US4 (use_cases) por último por depender das anteriores.
- **Sem mudança de contrato**: a API pública não muda; o frontend não é tocado.
- **Remuneração é gap à parte (B-06)**: mover/remover as data classes do motor antigo não cria nem
  quita a dívida da folha em R$.
- **`use_cases/` pode ficar parcialmente**: se um use_case tiver orquestração real, mantê-lo é
  aceitável (Princípio I é contra indireção vazia, não contra orquestração legítima).
