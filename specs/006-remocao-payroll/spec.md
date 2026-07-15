# Feature Specification: Remoção da superfície payroll/cobertura sem uso (B-07)

**Feature Branch**: `006-remocao-payroll`

**Created**: 2026-07-15

**Status**: Draft

**Input**: Simplificação do cluster payroll (B-07): mapear o uso real do agregado payroll_competency
(717 linhas) + governance + coverage/financial/remuneration/base/payroll_state_machine que restaram
em app/domain/ após a spec 005; remover a cerimônia não usada e colapsar o núcleo vivo restante,
com paridade funcional protegida pela suíte.

---

## Contexto e Decisão de Escopo

A spec 005 encerrou o colapso da `domain/` (118 → 32 arquivos) mas adiou o cluster payroll como
dívida **B-07**, condicionado a "analisar o fluxo real de folha antes de mexer". Essa análise foi
feita em 2026-07-15 e o resultado muda o tamanho da oportunidade:

**Levantamento de uso real (2026-07-15):**

- **Nenhuma tela do frontend chama os 14 endpoints de payroll (`/payrolls*`) nem os 2 de
  cobertura (`/coverage*`).** O diretório `frontend/src/features/payroll` está vazio; as rotas SPA
  de payroll existem como constantes mas não estão registradas no `App.tsx`; o dashboard exibe
  status de payroll *hardcoded* (`'Pendente'`).
- **O fluxo real de pagamento** (confirmado pelo stakeholder — ver B-06, descartado) é a **aba
  Relatórios**, que gera PDF/Excel/CSV **inteiramente no cliente** a partir da escala operacional,
  inclusive o cálculo horas × valor/hora. Não toca nenhum endpoint de payroll/cobertura.
- O `payroll_service` (507 linhas) faz todas as transições de status **direto no modelo** com `if`
  simples; o agregado `PayrollCompetency` (717 linhas) é instanciado em um único método
  (`validate_readiness`), como objeto descartável em memória, sem persistir nada do que o agregado
  "governa" (selo, versões, checklist).
- `PayrollGovernanceValidator` tem **zero referências** (classe morta). Vários DTOs de governança
  são importados e nunca usados.
- O fechamento de período **não** dispara a consolidação de cobertura — o `CoverageEngine` só é
  alcançável pelos 2 endpoints `/coverage*`, que nada chama.
- A folha oficial (honorários, impostos) é feita no **ERP** — não é papel desta aplicação
  (esclarecimento do stakeholder, 2026-07-14).

**Decisão do stakeholder (2026-07-15): remoção total.** Endpoint sem usuário real sai
(Constituição, Princípio V). Em vez de colapsar ~1900 linhas de `domain/` para dentro de services
que também não têm usuário, remove-se a superfície inteira: endpoints, services, schemas,
repositories, modelos e tabelas — com backup prévio e migration reversível.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Remover a superfície payroll/cobertura de ponta a ponta (Priority: P1)

Como mantenedor do sistema, removo os 14 endpoints de payroll e 2 de cobertura, seus services
(`payroll_service`, `coverage_service`), schemas, repositories, validators, modelos e tabelas
(`payrolls`, `coverage_snapshots`, `financial_snapshots`, `financial_facts`) — porque nenhum
usuário real (médico ou gestão) percorre esse fluxo. O pagamento continua sendo feito como hoje:
aba Relatórios → PDF/Excel → financeiro.

**Why this priority**: é a remoção que destrava todo o resto — o cluster `domain/` (B-07) só
existe para servir esses services. Removida a superfície, o cluster vira código morto trivial.

**Independent Test**: subir o app dev, percorrer as jornadas vivas (login, períodos, escala,
extras, relatórios, dashboard, usuários) e verificar que nada mudou; chamar `/api/v1/payrolls`
e confirmar que a rota não existe mais; suíte de testes verde.

**Acceptance Scenarios**:

1. **Given** o app dev no ar após a remoção, **When** gestão abre a aba Relatórios e gera o
   relatório PDF/Excel da competência, **Then** o resultado é idêntico ao de antes da remoção.
2. **Given** a API no ar, **When** qualquer rota `/api/v1/payrolls*` ou `/api/v1/coverage*` é
   chamada, **Then** responde 404 (rota inexistente), sem erro 500.
3. **Given** a suíte de testes, **When** executada após a remoção (testes do código removido saem
   junto), **Then** 0 falhas / 0 erros, e nenhum teste de fluxo vivo foi alterado.
4. **Given** um banco com dados nas tabelas removidas, **When** a migration de remoção roda,
   **Then** ela droppa as tabelas de forma reversível (downgrade recria o schema) e o deploy
   documenta backup prévio obrigatório.

---

### User Story 2 - Remover o cluster `domain/` e a fundação órfã (Priority: P2)

Como mantenedor, removo o que restou em `app/domain/` que só existia para servir a superfície
removida: `payroll/` (agregado + governança), `coverage/`, `financial/`, `remuneration/`, `base/`
(AggregateRoot) e `state_machines/` — e, na sequência, varro a fundação (`constants`, `errors`,
`events`, `exceptions`) removendo o que ficou sem consumidor (ex.: `payroll_status`,
`snapshot_status`, `financial_fact_status`, `payroll_errors`, eventos `PAYROLL_*`/`COVERAGE_*`).

**Why this priority**: é o encerramento formal do B-07 — a `domain/` fica contendo apenas
fundação com consumidor vivo comprovado, zero comportamento.

**Independent Test**: `grep` sem nenhum import de produto quebrado; suíte verde; inspeção de
`domain/` mostrando apenas arquivos com consumidor vivo.

**Acceptance Scenarios**:

1. **Given** a US1 concluída, **When** o cluster `domain/` é removido, **Then** nenhum import de
   produção quebra e a suíte segue verde.
2. **Given** a fundação da `domain/`, **When** a varredura de órfãos termina, **Then** todo
   arquivo restante em `domain/` tem pelo menos um consumidor de produção fora de testes.

---

### User Story 3 - Limpeza cruzada de resíduos payroll (Priority: P3)

Como mantenedor, removo os resíduos que referenciam o conceito de payroll fora do cluster:
analytics/KPI de payroll no `query_service` e seus endpoints (`/query/payroll`, `/kpi/payroll`,
`explain de reabertura de competência`) — que também não têm consumo no frontend —, o
`PayrollGovernanceValidator` morto, e as constantes/rotas/query-keys mortas do frontend
(`ROUTES.PAYROLL*`, `queryKeys.payroll`, empty-state de payroll).

**Why this priority**: é acabamento — evita que um leitor futuro encontre referências a um
conceito que não existe mais no backend. Não bloqueia o valor das US1/US2.

**Independent Test**: `grep -i payroll` no repositório retorna apenas histórico (docs/specs,
migrations antigas) — nenhum código de produção vivo.

**Acceptance Scenarios**:

1. **Given** o dashboard no ar, **When** a gestão navega por todas as abas, **Then** nenhuma tela
   quebra e nenhum dado exibido muda (o status de payroll exibido hoje é hardcoded).
2. **Given** o código após a limpeza, **When** se busca `payroll` no código de produção
   (backend + frontend), **Then** só restam ocorrências em documentação e migrations históricas.

---

### Edge Cases

- **Dados em produção nas tabelas removidas**: a migration droppa tabelas que podem conter dados
  (criados via API/testes/seed). Mitigação: backup obrigatório antes do deploy (rotina já existe,
  `scripts/backup.sh`) + downgrade da migration recria o schema (dados não voltam — aceito pelo
  stakeholder, o fluxo nunca teve UI).
- **Consumidores de eventos `PAYROLL_*`/`COVERAGE_*`**: verificar no plan se o event dispatcher
  tem subscribers (ex.: auditoria) antes de remover os nomes de evento.
- **Seed**: `seed_data.py` pode semear payroll/snapshots — ajustar para não referenciar modelos
  removidos.
- **Migrations históricas**: permanecem intactas (histórico de schema é código); apenas uma nova
  migration de drop é adicionada.
- **Testes de API dos endpoints removidos**: saem junto com os endpoints; o número total da suíte
  diminui — a paridade é medida pelos testes dos fluxos vivos, que não podem mudar.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema NÃO DEVE mais expor os endpoints `/payrolls*` (14) e `/coverage*` (2);
  as rotas, services, schemas, repositories e validators correspondentes DEVEM ser removidos.
- **FR-002**: As tabelas `payrolls`, `coverage_snapshots`, `financial_snapshots` e
  `financial_facts` DEVEM ser removidas por migration versionada e reversível (downgrade recria o
  schema), e o procedimento de deploy DEVE documentar backup prévio.
- **FR-003**: O pacote `app/domain/` DEVE conter, ao final, apenas arquivos com consumidor de
  produção vivo (fundação: constantes, erros, eventos e exceções em uso) — zero comportamento
  (agregados, engines, state machines, builders).
- **FR-004**: Os endpoints de analytics/KPI de payroll (`/query/payroll`, `/kpi/payroll` e o
  explain de reabertura de competência) DEVEM ser removidos, após confirmação (no plan) de que
  nenhuma tela os consome.
- **FR-005**: As jornadas vivas do usuário (login, períodos, escala/auto-escala, extras, trocas,
  relatórios, dashboard, usuários/RBAC, auditoria) NÃO DEVEM sofrer nenhuma mudança observável —
  mesmas telas, mesmos contratos, mesmos resultados.
- **FR-006**: A suíte de testes DEVE terminar verde (0 falhas/0 erros); testes do código removido
  saem junto; nenhum teste de fluxo vivo pode ser alterado para "passar".
- **FR-007**: A remoção DEVE ser incremental (um bloco coeso por commit, suíte verde entre
  passos), no padrão das specs 004/005.
- **FR-008**: Documentação DEVE ser atualizada ao final: backlog (B-07 encerrado), HANDOFF e
  spec 001 (capacidade "remuneração" anotada com o escopo real: relatório, não folha).

### Key Entities

- **Payroll (competência de folha)**: registro de ciclo de vida (draft → calculated → ... → paid)
  sem valores monetários — **a remover** (nunca teve UI; o ciclo real acontece no ERP).
- **CoverageSnapshot / FinancialSnapshot / FinancialFact**: consolidações derivadas da escala,
  geradas só pelos endpoints de cobertura que nada chama — **a remover** (o relatório vivo deriva
  os mesmos dados diretamente da escala, no cliente).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Médico e gestão percorrem todas as jornadas vivas sem nenhuma mudança perceptível
  (validação manual no navegador, mesmo roteiro do SC-005 da spec 004).
- **SC-002**: O relatório de pagamento (PDF/Excel/CSV) gerado após a remoção é idêntico ao gerado
  antes, para a mesma competência.
- **SC-003**: `app/domain/` termina apenas com fundação em uso — nenhum arquivo de comportamento;
  todo arquivo restante tem consumidor de produção comprovável.
- **SC-004**: Redução líquida de pelo menos **3.000 linhas** de código de produção (remoção real,
  não relocação) — cluster domain (~1.900), services (~720), rotas (~360), mais schemas,
  repositories, modelos e validators.
- **SC-005**: Suíte de testes com 0 falhas/0 erros; nenhum contrato de endpoint vivo alterado
  (testes de API dos fluxos vivos passam sem modificação).
- **SC-006**: B-07 marcado como encerrado no backlog, com este spec como registro da decisão.

## Assumptions

- **Nenhum consumidor externo da API**: a aplicação é de intranet e o único cliente conhecido é o
  frontend deste repositório. Se existir integração externa não documentada com `/payrolls*`,
  a premissa cai e o escopo deve ser revisto.
- **Dados históricos de payroll/snapshots não têm valor de negócio**: o fluxo nunca teve interface
  e a folha oficial vive no ERP. O backup de rotina cobre o risco residual.
- **A decisão de escopo (remoção total) foi tomada pelo stakeholder em 2026-07-15**, entre as
  alternativas: (a) remover tudo ← escolhida; (b) manter ciclo básico sem governança; (c) manter
  API intacta e só colapsar a `domain/`.
- **Eventos e auditoria**: assume-se que os eventos `PAYROLL_*`/`COVERAGE_*` não alimentam nenhum
  consumidor vivo além de log; verificação explícita no plan antes da remoção.
