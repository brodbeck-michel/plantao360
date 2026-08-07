# Feature Specification: Log de auditoria das ações do usuário

**Feature Branch**: `007-log-auditoria`

**Created**: 2026-08-07

**Status**: Draft

**Input**: Registrar quem alterou o quê no sistema, com foco na escala (planilha) e horas extras.
Demanda levantada em 2026-08-07, logo após liberar o perfil MEDICO para editar a planilha: hoje
não há como identificar qual usuário incluiu, alterou ou removeu um plantão.

---

## Contexto e Decisão de Escopo

### O gatilho

Até 2026-08-07, apenas ADMIN e COORDENADOR editavam a escala. Na mesma data o perfil **MEDICO**
passou a ter acesso de edição à planilha (spec de vínculo usuário↔médico), aumentando o número de
pessoas que alteram a escala e, com isso, a necessidade de rastro. A pergunta do stakeholder foi
direta: *"temos os log de alterações pra num futuro poder identificar qual usuário alterou tal
turno?"*

### Levantamento do estado atual (2026-08-07)

- **`backend/app/audit/` é um esqueleto, não uma implementação.** `models.py` e `service.py` estão
  declarados no próprio código como *"contratos para implementação futura"*; `AuditService.log()`
  é um `pass`. `AuditLog` é uma classe Python simples — **não é modelo SQLAlchemy e não tem
  tabela**.
- **As tabelas operacionais não guardam autoria.** `shift_parts` e `shift_extras` herdam
  `TimestampMixin` (`created_at`/`updated_at`), ou seja, registram **quando** mudou, mas nenhum
  campo indica **quem** mudou.
- **Os logs de aplicação não identificam o usuário.** O backend emite eventos estruturados
  (`assignment.created.v1`, `assignment.updated.v1`, `assignment.removed.v1`, `user.created`,
  etc.) com `request_id`/`correlation_id`, mas **sem `user_id`**. Vão para stdout do contêiner e
  **não há volume de logs** no `docker-compose.prod.yml` — o histórico se perde a cada recriação de
  contêiner, isto é, **a cada deploy**.
- **O painel "Histórico" do workspace não é auditoria.** É o undo/redo da sessão
  (`use-undo-redo`), guardado em memória do navegador; desaparece ao recarregar a página.

**Conclusão:** hoje é impossível responder "quem removeu o plantão do dia X". A informação não
existe em lugar nenhum — não é questão de estar difícil de consultar.

### Decisão de escopo

Duas alternativas foram consideradas com o stakeholder:

- **(a) Mínimo:** adicionar `created_by`/`updated_by` nas atribuições. Barato, mas **não registra
  remoções** — justamente o caso em que a informação some — nem o valor anterior.
- **(b) Tabela de auditoria dedicada** ← **escolhida**. Registra criação, alteração **e remoção**,
  com valor antes/depois, e serve para qualquer entidade sem alterar as tabelas operacionais.

O escopo desta spec é a opção (b), **limitada às entidades que o médico e a gestão alteram no
dia a dia**: escala (atribuições/divisões de turno), horas extras, cadastro de médicos, usuários e
competências. Não é um sistema de auditoria genérico com captura automática de todo o ORM — isso
seria cerimônia acima da necessidade (Princípio I).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Registrar as alterações da escala e de horas extras (Priority: P1)

Como gestor, quero que toda inclusão, alteração e remoção de plantão e de hora extra seja
registrada com autor, data/hora e o que mudou — para conseguir apurar divergências na escala e no
pagamento depois que elas acontecem.

**Why this priority**: é a razão da feature. Sem isto, nada mais tem valor. Escala e horas extras
são o que impacta pagamento e o que o médico agora consegue alterar sozinho.

**Independent Test**: com o app no ar, logar como médico, adicionar-se a um turno, alterar o
horário e remover-se; consultar a tabela de auditoria e encontrar os três eventos com o usuário
correto, o turno correto e os valores antes/depois.

**Acceptance Scenarios**:

1. **Given** um usuário autenticado, **When** ele adiciona um médico a um turno, **Then** um
   registro de auditoria é gravado com ação `create`, recurso `assignment`, o id da atribuição, o
   usuário autor, a data/hora e o estado resultante (médico, turno, data, horário).
2. **Given** uma atribuição existente, **When** o horário dela é alterado (ajuste/divisão de
   turno), **Then** o registro guarda os valores **antes e depois** dos campos alterados.
3. **Given** uma atribuição existente, **When** ela é removida, **Then** o registro guarda o
   estado que existia **antes** da remoção — o rastro sobrevive ao dado apagado.
4. **Given** uma hora extra, **When** ela é criada ou excluída, **Then** o evento é registrado com
   médico, duração e justificativa.
5. **Given** qualquer um dos eventos acima, **When** a operação de negócio falha e sofre rollback,
   **Then** **nenhum** registro de auditoria fica gravado (auditoria e operação são atômicas).

---

### User Story 2 - Consultar o histórico de uma competência (Priority: P2)

Como gestor, quero consultar os registros filtrando por competência, usuário, tipo de recurso e
período de datas — para investigar um caso concreto sem precisar de acesso ao banco.

**Why this priority**: sem consulta, o dado existe mas não é utilizável pelo usuário final. É o
que transforma o registro em resposta. Depende da US1 e por isso vem depois.

**Independent Test**: com registros gravados pela US1, chamar o endpoint de consulta filtrando por
usuário e por intervalo de datas e conferir que o resultado bate com as ações executadas.

**Acceptance Scenarios**:

1. **Given** registros de auditoria existentes, **When** a gestão consulta filtrando por usuário,
   **Then** recebe apenas as ações daquele usuário, mais recentes primeiro, paginadas.
2. **Given** registros de várias competências, **When** a consulta filtra por intervalo de datas,
   **Then** apenas os eventos daquele intervalo retornam.
3. **Given** um usuário com perfil **MEDICO** ou **CONSULTA**, **When** ele chama o endpoint de
   auditoria, **Then** recebe **403** — a trilha é visível apenas para ADMIN e COORDENADOR.
4. **Given** um registro de auditoria gravado, **When** qualquer usuário tenta alterá-lo ou
   removê-lo pela API, **Then** não existe endpoint para isso (a trilha é somente-leitura).

---

### User Story 3 - Ver o histórico da competência dentro do workspace (Priority: P3)

Como gestor, quero ver o histórico de alterações da competência em uma aba do próprio workspace,
para não precisar sair da tela onde monto a escala.

**Why this priority**: é conveniência de acesso — o valor de investigação já foi entregue pela
US2 via API. Fica por último para não atrasar o registro, que é o que não pode ser reconstruído
depois.

**Independent Test**: abrir uma competência no workspace como ADMIN, acessar a aba de histórico e
ver a lista de eventos daquela competência; conferir que o perfil MEDICO não enxerga a aba.

**Acceptance Scenarios**:

1. **Given** um ADMIN ou COORDENADOR no workspace, **When** abre a aba de histórico, **Then** vê
   os eventos da competência em ordem cronológica inversa, com autor, ação, alvo e horário.
2. **Given** um usuário MEDICO no workspace, **When** a tela é renderizada, **Then** a aba de
   histórico **não aparece** e a rota/endpoint correspondente responde 403.
3. **Given** uma competência sem alterações, **When** a aba é aberta, **Then** exibe estado vazio
   informativo, sem erro.

---

### Edge Cases

- **Falha ao gravar a auditoria**: se o registro falhar, a operação de negócio **deve falhar
  junto** (mesma transação). Registro silenciosamente perdido é pior que erro visível, porque
  cria falsa confiança na trilha.
- **Ações do sistema sem usuário** (seed, migrations, rotinas): gravar com autor nulo e um marcador
  de origem `system`, nunca atribuir a um usuário real.
- **Usuário removido depois do evento**: o registro guarda `user_id` **e** o e-mail/nome como texto
  no momento da ação, para o rastro sobreviver à exclusão ou renomeação do usuário.
- **Dados sensíveis no diff**: nunca gravar `password_hash` nem qualquer credencial no
  antes/depois; a lista de campos gravados é explícita, não é "tudo que veio no request".
- **Volume**: a escala gera muitos eventos em lote (duplicar dia/semana). O registro deve suportar
  gravação em lote sem multiplicar transações, e a consulta precisa ser paginada e indexada.
- **Retenção**: a trilha cresce indefinidamente. Esta spec **não** implementa expurgo; define
  índices e paginação para o volume previsto (dezenas de usuários) e registra o tema como dívida.
- **Migração de dados existentes**: não há histórico anterior a recuperar — a trilha começa vazia
  na data do deploy. Isso deve estar explícito para quem consultar (não confundir "sem registro"
  com "nada aconteceu").

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE persistir, em tabela dedicada, um registro para cada operação de
  criação, alteração e remoção nas entidades: **atribuição de plantão** (`assignment`/`shift_part`),
  **hora extra** (`shift_extra`), **médico** (`doctor`), **usuário** (`user`) e **competência**
  (`period`).
- **FR-002**: Cada registro DEVE conter, no mínimo: data/hora (UTC), autor (id do usuário **e**
  identificação textual preservada), ação (`create`/`update`/`delete`), tipo de recurso, id do
  recurso, e o conteúdo do que mudou (estado antes e/ou depois, conforme a ação).
- **FR-003**: O registro de auditoria DEVE ocorrer na **mesma transação** da operação de negócio —
  ou os dois efeitos acontecem, ou nenhum.
- **FR-004**: O registro NÃO DEVE conter credenciais (`password_hash`, tokens) nem campos
  sensíveis não relacionados à ação; os campos gravados são declarados explicitamente por recurso.
- **FR-005**: O sistema DEVE expor endpoint de **consulta** paginada da trilha, com filtros por
  usuário, tipo de recurso, id de recurso, competência e intervalo de datas, ordenado do mais
  recente para o mais antigo.
- **FR-006**: O acesso à consulta DEVE ser restrito aos perfis **ADMIN** e **COORDENADOR**;
  demais perfis recebem 403.
- **FR-007**: A trilha DEVE ser **somente-leitura** pela API — não existem endpoints de alteração
  ou exclusão de registros de auditoria.
- **FR-008**: Ações executadas sem usuário autenticado (seed, rotinas internas) DEVEM ser gravadas
  com autor nulo e origem identificada como sistema, nunca atribuídas a um usuário real.
- **FR-009**: O frontend DEVE oferecer, no workspace, uma visão do histórico da competência para
  os perfis autorizados, e **não** exibir a aba para os demais.
- **FR-010**: A tabela DEVE ser criada por migration versionada e reversível, com índices que
  sustentem os filtros do FR-005 (por recurso+id, por autor e por data).
- **FR-011**: As jornadas existentes (escala, extras, cadastros, relatórios, dashboard) NÃO DEVEM
  ter mudança observável de comportamento além do registro passar a existir.
- **FR-012**: A suíte de testes DEVE terminar verde, com testes cobrindo: gravação nas três ações,
  atomicidade (rollback não deixa registro), ausência de campos sensíveis e o bloqueio 403 por
  perfil.

### Key Entities

- **AuditLog (registro de auditoria)**: evento imutável de alteração. Atributos: data/hora,
  autor (id + identificação textual), perfil do autor no momento, ação, tipo de recurso, id do
  recurso, competência relacionada (quando aplicável), estado antes, estado depois, origem
  (usuário/sistema) e id de correlação da requisição. Não possui relacionamento obrigatório com as
  tabelas operacionais — o registro sobrevive à remoção do dado auditado.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Dado um plantão qualquer alterado após o deploy, a gestão consegue identificar
  **quem** o alterou, **quando** e **o que** mudou, em menos de 1 minuto, sem acesso ao banco.
- **SC-002**: Um plantão **removido** continua rastreável: a trilha mostra o estado que existia
  antes da remoção e o autor da exclusão.
- **SC-003**: 100% das operações de criação/alteração/remoção das entidades do FR-001 geram
  registro — verificado por teste automatizado para cada rota coberta.
- **SC-004**: Nenhum registro de auditoria fica gravado quando a operação de negócio falha
  (teste de rollback).
- **SC-005**: Perfis MEDICO e CONSULTA recebem 403 na consulta da trilha (teste automatizado) e
  não enxergam a aba de histórico na interface.
- **SC-006**: Nenhuma credencial aparece nos registros — verificado por teste que inspeciona o
  conteúdo gravado ao criar/alterar usuário.
- **SC-007**: Suíte de testes verde (0 falhas), mantendo as 411 passagens atuais mais os novos
  testes.

## Assumptions

- **Volume compatível com consulta direta no banco**: dezenas de usuários e algumas centenas de
  eventos por competência. Não há necessidade de solução externa de logs, particionamento ou
  expurgo nesta fase — se o volume surpreender, o tema volta como dívida.
- **A trilha começa vazia**: não existe histórico anterior recuperável (a informação nunca foi
  gravada). Eventos anteriores ao deploy não podem ser reconstruídos.
- **Fuso horário**: registros gravados em UTC e convertidos para exibição, seguindo o padrão já
  usado nas demais tabelas.
- **O esqueleto `app/audit/` atual será substituído**, não estendido: os arquivos de contrato
  (`models.py`, `service.py`) serão reescritos com implementação real ou removidos se o desenho
  final não os aproveitar — decisão registrada no plan.
- **Escopo fechado nas 5 entidades do FR-001**: outras tabelas podem ser adicionadas depois
  reutilizando a mesma infraestrutura, sem mudança de contrato.
