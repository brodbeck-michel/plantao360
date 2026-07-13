# Feature Specification: Baseline de Testes Confiável (Fase 2 — passo 1)

**Feature Branch**: `003-baseline-de-testes`

**Created**: 2026-07-13

**Status**: Draft

**Input**: Estabelecer uma suíte de testes verde e confiável para servir de rede de segurança
da simplificação do `domain/` (Fase 2). Sem isso, refatorar é refatorar no escuro.

---

## Contexto e Objetivo

Ao preparar a Fase 2 (colapso do `domain/`), rodamos a suíte do backend e encontramos:

- **744 testes coletados**, **692 passam**, **52 falham**, **1 erro de coleção**.
- Nenhuma falha foi causada pela Fase 0 — são todas **pré-existentes**.

Um suíte 52/744 vermelho **não é uma rede de segurança**: não dá para saber se uma quebra
durante o refactor é nova ou já existia. Esta feature torna a suíte **confiável** — verde num
comando — para que a Fase 2 possa medir cada passo (verde antes, verde depois).

Guiado pelo Princípio III da constituição: **testar o que importa**. Testes que travam a
mudança e verificam trivialidade são passivo, não ativo.

**Fora de escopo**: qualquer mudança de comportamento do produto; a simplificação do `domain/`
em si (isso é o passo 2 da Fase 2, uma feature seguinte).

---

## Diagnóstico das 52 falhas (+1 erro de coleção)

| Grupo | Arquivos | Qtd | Causa raiz | Ação proposta |
|---|---|---|---|---|
| **Integração sem auth** | `test_extra_api` (10), `test_period_api` (9), `test_doctors_api` (8), `test_assignment_api` (8), `test_shift_api` (6), `test_database` (1) | ~42 | O RBAC (Sprint 19) passou a exigir autenticação; o cliente de teste não envia token → `401` | **Consertar**: fixture de cliente autenticado compartilhada |
| **Bootstrap** | `test_bootstrap` (1) | 1 | Provável dependência do fluxo de auth/admin | **Consertar** |
| **Testes-contadores frágeis** | `test_domain_events`, `test_remuneration_events`, `test_payroll_events`, `test_shift_constants` | 4 | Asserções de "número mágico" (ex.: `assert 45 == 38`) que quebram a cada constante nova | **Deletar** (testam trivialidade) |
| **Fixtures desatualizadas** | `test_doctor_mapper` (2), `test_shift_service` (1) | 3 | Campos novos (`specialty`, `doctor_type`) não refletidos nas fixtures | **Consertar** |
| **Teste obsoleto** | `test_settings_factory` (1) | 1 | Testa defaults antigos, antes do hardening de segredos | **Atualizar** para o comportamento atual |
| **Erro de coleção** | `test_manifests` (`manifest_loader`) | (bloqueia coleção) | Cerimônia de "module manifest" (ADR-016) sem módulo no path | **Deletar** (peça morta) |

Além disso: existe um **gate de cobertura `--cov-fail-under=80`** que, sozinho, reprova a suíte
mesmo com testes passando — número irreal para este contexto.

> Hipótese central (a validar no plano): **~42 das 52 falhas têm uma única causa** (cliente de
> teste sem autenticação). Uma fixture compartilhada deve resolvê-las em bloco.

---

## User Scenarios & Testing *(mandatory)*

Stakeholder: o **mantenedor** (você/eu). O valor é uma rede de segurança confiável para a Fase 2.

### User Story 1 - Suíte verde num comando (Priority: P1)

Rodar a suíte de testes do backend e obter **0 falhas** (fora testes explicitamente marcados
como pulados e justificados), num único comando reproduzível.

**Why this priority**: é a definição de "rede de segurança". Sem verde confiável, nenhuma
simplificação do `domain/` pode ser medida.

**Independent Test**: `pytest` (no ambiente de teste) retorna 0 falhas e 0 erros de coleção.

**Acceptance Scenarios**:

1. **Given** o repositório atual, **When** rodo a suíte, **Then** o resultado é 0 falhas e 0
   erros de coleção.
2. **Given** a suíte verde, **When** um teste passa a falhar depois de uma mudança, **Then** a
   falha é sinal confiável de regressão (não ruído pré-existente).

---

### User Story 2 - Testes de integração autenticados (Priority: P1)

Os testes de API que hoje falham com `401` passam a autenticar via uma fixture compartilhada,
refletindo o RBAC real do produto.

**Why this priority**: é a maior fatia das falhas (~42) e cobre justamente os fluxos críticos
(plantões, extras, escala, períodos, folha) que a Fase 2 precisa proteger.

**Independent Test**: os testes de `test_*_api.py` passam usando um cliente autenticado.

**Acceptance Scenarios**:

1. **Given** um endpoint protegido por RBAC, **When** o teste usa a fixture de cliente
   autenticado, **Then** recebe resposta de sucesso (não `401`).
2. **Given** a fixture compartilhada, **When** um novo teste de API é escrito, **Then** ele
   reaproveita a autenticação sem repetir setup.

---

### User Story 3 - Remover testes-cerimônia frágeis (Priority: P2)

Testes que verificam contagens/números mágicos e artefatos de cerimônia (manifests) são
removidos, pois testam trivialidade e travam a evolução.

**Why this priority**: reduzem ruído e desbloqueiam a coleção (`manifest_loader`), mas não
protegem comportamento real.

**Independent Test**: após a remoção, a coleção não tem erros e nenhum teste falha por "número
mágico" desatualizado.

**Acceptance Scenarios**:

1. **Given** um teste que apenas conta itens de um enum, **When** ele é avaliado, **Then** é
   removido (ou substituído por um teste de comportamento, se houver valor real).
2. **Given** o `test_manifests` que quebra a coleção, **When** removido, **Then** a suíte coleta
   sem erro.

---

### User Story 4 - Atualizar testes fora de sincronia (Priority: P2)

Testes cujas fixtures/asserções ficaram desatualizadas em relação ao schema atual (campos
`specialty`, `doctor_type`; hardening de segredos) são atualizados para o comportamento vigente.

**Why this priority**: recuperam cobertura real que só está vermelha por desatualização.

**Independent Test**: `test_doctor_mapper`, `test_shift_service` e `test_settings_factory` passam
refletindo o schema/validações atuais.

**Acceptance Scenarios**:

1. **Given** o DTO de Doctor que exige `specialty`/`doctor_type`, **When** a fixture fornece
   esses campos, **Then** o teste do mapper passa.
2. **Given** o hardening de segredos em produção, **When** o teste de settings é atualizado,
   **Then** ele valida o comportamento atual (falha rápida com segredo fraco).

---

### User Story 5 - Gate de cobertura realista (Priority: P3)

O gate de cobertura deixa de reprovar artificialmente. Define-se um limite realista para o
estado atual (ou remove-se o `--cov-fail-under` fixo), sem fingir uma cobertura que não existe.

**Why this priority**: um gate irreal ensina a equipe a ignorar o CI — pior que não ter gate.

**Independent Test**: a suíte verde não é reprovada apenas pelo número de cobertura.

**Acceptance Scenarios**:

1. **Given** a suíte verde, **When** roda com o gate, **Then** não é reprovada por cobertura
   irreal; o limite reflete o estado atual e pode subir depois.

---

### Edge Cases

- **Falha que reaparece só em CI**: a fixture de auth deve funcionar igual local e no CI.
- **Teste removido que tinha valor real escondido**: antes de deletar um teste-contador, checar
  se ele não cobre, de fato, alguma regra (se cobrir, converter em teste de comportamento).
- **Cobertura cai ao deletar testes**: aceitável se os testes removidos eram cerimônia; o que
  importa é cobertura de comportamento, não o número absoluto.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A suíte do backend DEVE rodar com **0 falhas e 0 erros de coleção** num único
  comando reproduzível no ambiente de teste.
- **FR-002**: DEVE existir uma **fixture compartilhada de cliente autenticado** para os testes
  de integração de API, refletindo o RBAC real.
- **FR-003**: Os testes-cerimônia frágeis (contagens de enum/eventos; `test_manifests`) DEVEM
  ser removidos, salvo quando cobrirem comportamento real (caso em que são convertidos).
- **FR-004**: Os testes desatualizados (mapper de Doctor, shift service, settings de produção)
  DEVEM ser atualizados para o schema/validações atuais.
- **FR-005**: O gate de cobertura DEVE refletir um valor realista do estado atual (ou ser
  removido como gate rígido), sem mascarar cobertura inexistente.
- **FR-006**: Qualquer teste intencionalmente pulado DEVE ser marcado como `skip` com
  justificativa registrada (nada de falha silenciosa).
- **FR-007**: A ação de cada teste (consertado / atualizado / removido) DEVE ser registrada,
  para rastreabilidade da triagem.
- **FR-008**: Nenhuma mudança de comportamento do produto DEVE ocorrer nesta feature (apenas
  testes e configuração de teste).

### Key Entities

- **Suíte de testes**: conjunto de testes do backend que serve de portão de regressão.
- **Fixture de autenticação**: utilitário de teste que produz um cliente autenticado por papel.
- **Relatório de triagem**: registro de o que foi consertado, atualizado ou removido e por quê.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A suíte roda com **0 falhas e 0 erros de coleção**.
- **SC-002**: As ~42 falhas de integração por `401` são resolvidas (a grande maioria por uma
  fixture compartilhada).
- **SC-003**: Os fluxos críticos (plantões, extras, escala, períodos, folha) têm testes de API
  passando com cliente autenticado.
- **SC-004**: Cada um dos 52 testes que falhavam tem um destino registrado (consertado /
  atualizado / removido com justificativa).
- **SC-005**: O comportamento do produto permanece idêntico (nenhuma mudança fora de testes e
  config de teste), verificável no app dev.
- **SC-006**: A partir daqui, uma falha de teste durante a Fase 2 é sinal confiável de regressão.

---

## Assumptions

- **Uma causa raiz domina** as falhas de integração (cliente sem autenticação pós-RBAC); a
  fixture compartilhada resolve o grosso. *(A validar no plano.)*
- **Ambiente de teste** usa SQLite (`ENVIRONMENT=test`), como hoje; sem necessidade de Postgres
  para a suíte unitária/integração.
- **Deletar testes-cerimônia é aceitável** e desejável (Princípio III) — eles não cobrem
  comportamento real.
- **O objetivo não é 100% de cobertura**, e sim uma suíte verde e significativa que sirva de
  rede para o refactor.
