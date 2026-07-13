# Feature Specification: Colapso da camada `domain/` (Fase 2 — passo 2)

**Feature Branch**: `004-colapso-domain`

**Created**: 2026-07-13

**Status**: Draft

**Input**: Simplificar a arquitetura do backend removendo peso morto e abstrações de consumidor
único da camada `app/domain/`, com **paridade funcional total**, guiado por
`docs/levantamento-domain.md` e protegido pela suíte verde (spec 003).

---

## Contexto e Objetivo

O backend carrega uma camada `app/domain/` super-engenhariada (30 módulos, 118 arquivos, estilo
DDD/CQRS) construída além da necessidade. O levantamento de acoplamento (2026-07-13) mediu, por
módulo, quantos consumidores de **produto** cada um tem, revelando: muitos módulos não são usados
por nenhum código de produto (só por testes), e vários outros têm **um único** consumidor.

Esta feature remove esse excesso **sem alterar nenhum comportamento do produto**. É simplificação
interna: as mesmas telas, os mesmos endpoints, os mesmos resultados — com muito menos código para
manter (Princípio I da constituição).

**Fora de escopo**: `constants`/`errors`/`events` (fundação, permanecem);
`read_models`/`query`/`rules`/`state_machines` e a camada `use_cases/` (Grupo D, avaliados numa
feature futura); e o **cálculo de remuneração** (gap B-06 — feature nova, não simplificação).

---

## User Scenarios & Testing *(mandatory)*

Stakeholder: o **mantenedor** (você/eu). O valor é uma base enxuta e barata de manter, com a
mesma funcionalidade para os usuários finais (médico/gestão).

### User Story 1 - Remover módulos mortos (Priority: P1)

Os módulos de `domain/` que **nenhum código de produto** usa são removidos (junto com seus
testes), reduzindo a superfície de código sem afetar o produto.

**Why this priority**: é a maior redução com o menor risco — nada de produto depende deles.

**Independent Test**: após remover os módulos do Grupo A, a suíte continua verde e a aplicação
sobe e responde igual.

**Acceptance Scenarios**:

1. **Given** um módulo do Grupo A (ex.: `remuneration`, `overlap`, `value_objects`), **When** ele
   e seus testes são removidos, **Then** a suíte continua com 0 falhas e nenhum import de produto
   quebra.
2. **Given** a aplicação após a remoção, **When** um usuário percorre os fluxos (escala, extras,
   folha, dashboard), **Then** o comportamento é idêntico ao de antes.

---

### User Story 2 - Inline de abstrações de consumidor único (Priority: P1)

Cada módulo de `domain/` usado por **um único** service tem sua lógica movida para dentro desse
service, e o módulo é removido — eliminando a indireção proibida pelo Princípio I.

**Why this priority**: é o coração da simplificação — colapsa a profundidade de camada para
`rota → service → model`, mantendo a funcionalidade.

**Independent Test**: após mover a lógica de um módulo do Grupo B para o seu único consumidor e
deletar o módulo, os testes desse service passam e a resposta da API é idêntica.

**Acceptance Scenarios**:

1. **Given** um módulo do Grupo B (ex.: `projections` → dashboard, `kpi`/`analytics`/
   `explainability` → query, `coverage`/`financial` → coverage), **When** sua lógica é embutida no
   único service consumidor e o módulo é deletado, **Then** a suíte continua verde e o endpoint
   correspondente retorna o mesmo resultado.
2. **Given** o processo incremental, **When** cada módulo é colapsado, **Then** a suíte roda
   verde **entre** os passos (nunca big-bang).

---

### User Story 3 - Garantir paridade e não-regressão (Priority: P1)

Ao final, a aplicação entrega exatamente as mesmas funcionalidades e contratos de API de antes, e
isso é comprovado — não presumido.

**Why this priority**: paridade funcional é a regra inviolável desta fase; sem prova, a
simplificação não é confiável.

**Independent Test**: a suíte verde (spec 003) permanece verde; os contratos de API (rotas,
formatos de resposta) permanecem idênticos; o app dev sobe e os fluxos principais funcionam.

**Acceptance Scenarios**:

1. **Given** o colapso concluído, **When** a suíte completa roda, **Then** o resultado é 0 falhas
   e 0 erros.
2. **Given** o colapso concluído, **When** os endpoints são comparados com o comportamento
   anterior, **Then** rotas e formatos de resposta são idênticos (nenhuma mudança de contrato).
3. **Given** o colapso concluído, **When** se conta o código da `domain/`, **Then** há redução
   substancial de arquivos/linhas em relação ao ponto de partida.

---

### Edge Cases

- **Lógica compartilhada escondida**: se, ao inlinar, descobrir-se que um módulo "de consumidor
  único" na verdade é usado por outro caminho, ele **não** é deletado até o uso ser tratado.
- **Teste que cobre módulo removido**: o teste sai junto com o módulo morto; se ele cobria
  comportamento real (e não o módulo em si), o comportamento deve continuar coberto por outro
  teste (do service).
- **Reexport via `__init__`**: remover um módulo exige limpar reexports/`__init__` que o
  referenciem, para não deixar import quebrado.
- **Gap de remuneração (B-06)**: deletar o motor morto `domain/remuneration` **não** implementa a
  folha; o gap continua registrado no backlog, separado desta feature.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Os módulos de `domain/` sem consumidor de produto (Grupo A do levantamento) DEVEM
  ser removidos, junto com os testes que existiam apenas para eles.
- **FR-002**: Cada módulo de `domain/` com consumidor único (Grupo B) DEVE ter sua lógica movida
  para dentro do service consumidor e ser removido.
- **FR-003**: Nenhum comportamento observável do produto PODE mudar — mesmas telas, mesmos
  cálculos, mesmos resultados.
- **FR-004**: Os contratos de API (rotas e formatos de resposta) DEVEM permanecer idênticos.
- **FR-005**: A suíte de testes DEVE permanecer verde (0 falhas / 0 erros) **a cada passo**
  incremental — a simplificação é inline-and-delete, nunca big-bang.
- **FR-006**: Ao final, NÃO PODE haver import de produto apontando para um módulo removido
  (nenhum import quebrado).
- **FR-007**: Os módulos de fundação (`constants`, `errors`, `events`) DEVEM permanecer.
- **FR-008**: O Grupo D (`read_models`, `query`, `rules`, `state_machines`, `use_cases/`) e o gap
  de remuneração (B-06) NÃO fazem parte desta feature.

### Key Entities

Não há novas entidades de dados. A "entidade" afetada é a **estrutura de código** do backend
(a camada `domain/` e os services que a consomem).

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A suíte de testes termina com **0 falhas e 0 erros** (igual ou melhor que o baseline
  de 738 passando).
- **SC-002**: **0 imports de produto** apontando para módulos removidos (verificável por busca).
- **SC-003**: Os contratos de API permanecem idênticos (mesmas rotas e formatos de resposta),
  verificável pelos testes de integração de API que já passam.
- **SC-004**: A camada `domain/` reduz de ~118 arquivos para aproximadamente **30–40** ao final
  do escopo desta feature (Grupos A + B), sem perder funcionalidade.
- **SC-005**: O app dev sobe e os fluxos principais (escala, extras, cobertura, dashboard,
  usuários) funcionam exatamente como antes.
- **SC-006**: Cada passo de colapso é um incremento com a suíte verde (rastreável no histórico de
  commits).

---

## Assumptions

- **A suíte verde é a rede de segurança**: a spec 003 deixou a suíte confiável (738 passando); ela
  é o critério objetivo de paridade a cada passo.
- **O levantamento é a fonte da verdade de escopo**: os Grupos A e B de `docs/levantamento-domain.md`
  definem exatamente o que deletar e o que inlinar.
- **Sem mudança de contrato**: a API pública não muda; frontend não é tocado.
- **Ordem de menor risco primeiro**: Grupo A (deletar) antes do Grupo B (inline).
- **Remuneração é gap à parte**: deletar o motor morto não cria nem quita a dívida de B-06.
