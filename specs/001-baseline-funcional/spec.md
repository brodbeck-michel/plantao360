# Feature Specification: Plantão 360 — Baseline Funcional

**Feature Branch**: `001-baseline-funcional`

**Created**: 2026-07-13

**Status**: Draft

**Input**: Documentação do escopo real do produto (papéis, jornadas e 8 capacidades), como referência oficial para a simplificação da arquitetura com paridade funcional.

---

## Contexto e Objetivo

O Plantão 360 já existe e está em uso interno na Unimed Tubarão (intranet, poucas dezenas de
usuários). Esta especificação **não descreve funcionalidade nova** — ela fixa o *escopo real
que os usuários usam*, para servir de contrato durante a simplificação da arquitetura.

Regra de ouro desta baseline: **paridade funcional**. Nada que o usuário usa hoje pode
desaparecer. O que muda é a complexidade interna do código, não o que o produto faz.

**Fora de escopo desta spec**: decisões técnicas (linguagem, camadas, banco). Elas vivem na
constituição e no `plan.md`.

---

## User Scenarios & Testing *(mandatory)*

Papéis reais: **Médico** plantonista, **Gestão** (que também coordena a escala e cuida do
financeiro) e **Admin/TI**. As jornadas abaixo estão priorizadas: se apenas a P1 existisse, já
haveria um produto que entrega valor.

### User Story 1 - Gestão abre o período e os plantões (Priority: P1)

A Gestão cria um período (por exemplo, um mês) e define os plantões daquele período (data e
tipo — diurno/noturno — com a cobertura esperada de médicos), deixando-os abertos para
inscrição. A Gestão também pode alocar médicos diretamente e ajustar a escala.

**Why this priority**: é o coração do sistema. Sem os plantões abertos, nenhuma outra
capacidade (inscrição do médico, extras, cobertura, folha) tem sobre o que operar.

**Independent Test**: criar um período, adicionar plantões e vê-los abertos na grade do
período, com a cobertura esperada.

**Acceptance Scenarios**:

1. **Given** que não existe período para o mês, **When** a Gestão cria o período e adiciona
   plantões por data e tipo, **Then** os plantões aparecem na grade do período com a cobertura
   esperada e ficam abertos para inscrição.
2. **Given** um plantão aberto, **When** a Gestão aloca um médico diretamente, **Then** a
   alocação é registrada e a cobertura do plantão é atualizada.
3. **Given** um plantão já existente para (período, data, tipo), **When** a Gestão tenta criar
   outro idêntico, **Then** o sistema impede a duplicação.

---

### User Story 2 - Médico se escala e consulta a sua escala (Priority: P1)

O médico vê os plantões abertos do período e **se inscreve** nos que deseja pegar. Depois de
inscrito, consulta a sua escala (os plantões em que está, com data, tipo e horário). A Gestão
confere a escala resultante.

**Why this priority**: é o uso mais frequente e o motivo pelo qual o médico entra no sistema —
montar a própria escala e acompanhá-la.

**Independent Test**: com plantões abertos, o médico logado se inscreve em alguns e passa a vê-los
na sua escala; não consegue se inscrever em plantões que conflitam no horário.

**Acceptance Scenarios**:

1. **Given** plantões abertos no período, **When** o médico se inscreve em um plantão, **Then**
   a alocação é registrada e o plantão passa a constar na escala dele.
2. **Given** que o médico já está em um plantão, **When** ele tenta se inscrever em outro que se
   sobrepõe no horário, **Then** o sistema **bloqueia** e explica o conflito.
3. **Given** que o médico está inscrito em plantões, **When** ele acessa a sua escala, **Then**
   vê a lista/calendário dos seus plantões (e não os dos outros), com data, tipo e horário.
4. **Given** um médico sem plantões no período, **When** ele acessa a sua escala, **Then** vê
   uma indicação clara de que não há plantões.

---

### User Story 3 - Médico registra plantão extra (Priority: P2)

Além da escala normal, o médico registra um plantão ou horas extras que realizou. O extra
conta diretamente para a remuneração; a Gestão confere no fechamento do período (sem etapa de
aprovação prévia).

**Why this priority**: afeta pagamento e é rotina, mas depende da escala já existir (P1).

**Independent Test**: um médico registra um extra; o extra aparece imediatamente no cálculo de
remuneração daquele médico e no fechamento da Gestão.

**Acceptance Scenarios**:

1. **Given** um período aberto, **When** o médico registra um extra (data, tipo, duração),
   **Then** o extra é registrado e passa a contar para a remuneração do médico.
2. **Given** um extra registrado, **When** a Gestão revisa no fechamento, **Then** consegue
   ajustá-lo ou removê-lo, e a alteração fica na auditoria.

---

### User Story 4 - Troca / cobertura de plantão (Priority: P2)

Quando um médico não pode cumprir um plantão, registra-se uma troca/cobertura: outro médico
assume aquele plantão. A substituição vale a partir do registro (sem aprovação prévia); a
Gestão confere no fechamento.

**Why this priority**: é como a operação lida com imprevistos; afeta quem será pago pelo
plantão.

**Independent Test**: registrar uma cobertura de um médico por outro em um plantão; a escala e
a remuneração passam a refletir o médico que efetivamente cobriu.

**Acceptance Scenarios**:

1. **Given** um plantão alocado ao Médico A, **When** registra-se uma cobertura pelo Médico B,
   **Then** o plantão passa a ser atribuído ao Médico B para fins de escala e remuneração, e o
   registro fica na auditoria.
2. **Given** uma troca que gera sobreposição de horário para o Médico B, **When** ela é
   registrada, **Then** o sistema **bloqueia** e explica o conflito.

---

### User Story 5 - Cálculo e exportação da remuneração (Priority: P1)

A Gestão fecha a remuneração do período: o sistema **calcula** os valores a pagar por médico
(com base no tipo de plantão/hora e nos extras aprovados) e **exporta** um relatório para o
financeiro/folha.

**Why this priority**: é o entregável financeiro do sistema — o resultado que justifica a
existência do controle de escala e extras. Crítico e sensível (dinheiro).

**Independent Test**: com escala, extras aprovados e trocas resolvidas de um período, gerar o
cálculo e a exportação; conferir que os totais por médico batem com as regras de valor.

**Acceptance Scenarios**:

1. **Given** um período com escala e extras aprovados, **When** a Gestão gera a remuneração,
   **Then** o sistema apresenta o valor a pagar por médico, detalhando plantões normais e
   extras.
2. **Given** a remuneração calculada, **When** a Gestão exporta, **Then** é gerado um relatório
   para o financeiro em formato que ele consiga consumir.
3. **Given** um período com a remuneração fechada, **When** alguém tenta alterar um plantão já
   fechado, **Then** o sistema impede ou exige reabertura controlada, e a auditoria registra.

---

### User Story 6 - Dashboard / indicadores do período (Priority: P3)

A Gestão vê um painel com resumos operacionais (cobertura dos plantões, buracos na escala) e
financeiros (custo do período) para acompanhar o mês.

**Why this priority**: agrega valor de acompanhamento, mas o produto funciona sem ele.

**Independent Test**: abrir o dashboard de um período com dados e conferir que os números
refletem a escala e a remuneração daquele período.

**Acceptance Scenarios**:

1. **Given** um período com escala, **When** a Gestão abre o dashboard, **Then** vê indicadores
   de cobertura e de custo coerentes com os dados do período.

---

### User Story 7 - Administração de usuários e acesso (Priority: P2)

O Admin/TI cadastra usuários, define o papel de cada um (Médico, Gestão, Admin) e controla o
acesso. Cada papel só enxerga e faz o que lhe cabe.

**Why this priority**: é pré-condição de segurança para tudo, mas é operação pontual (não
diária).

**Independent Test**: criar usuários de cada papel e verificar que as permissões são
respeitadas (um médico não acessa a folha; a gestão não administra usuários; etc.).

**Acceptance Scenarios**:

1. **Given** um usuário com papel Médico, **When** ele tenta acessar o fechamento de folha,
   **Then** o acesso é negado.
2. **Given** um usuário com papel Gestão, **When** ele acessa a montagem de escala e a folha,
   **Then** o acesso é permitido.
3. **Given** um usuário com papel Admin, **When** ele cadastra/edita usuários e papéis,
   **Then** as mudanças passam a valer no controle de acesso.

---

### Edge Cases

- **Sobreposição de plantões**: o mesmo médico não pode ocupar dois plantões cujos horários se
  cruzam — o sistema deve detectar e bloquear (regra de negócio no backend).
- **Duplicidade de plantão**: não pode haver dois plantões idênticos para (período, data, tipo).
- **Alteração após fechamento**: mudanças em plantões/extras de um período com folha fechada
  exigem controle (bloqueio ou reabertura auditada).
- **Inscrição em plantão lotado**: se um plantão já atingiu a cobertura esperada, o médico não
  deve conseguir se inscrever (ou o sistema sinaliza excesso), conforme regra da Gestão.
- **Revisão no fechamento**: como extras e trocas contam direto, a conferência da Gestão no
  fechamento é o ponto de controle — ajustes ali devem ser auditados.
- **Período vazio**: consultar escala/dashboard de um período sem plantões deve exibir estado
  vazio claro, não erro.
- **Plantão sem cobertura mínima**: a grade deve sinalizar plantões abaixo da cobertura esperada.

---

## Requirements *(mandatory)*

### Functional Requirements

**Períodos e plantões**
- **FR-001**: O sistema DEVE permitir à Gestão criar um período (intervalo de datas) e listá-lo.
- **FR-002**: O sistema DEVE permitir definir plantões dentro de um período, cada um com data,
  tipo (diurno/noturno) e cobertura esperada de médicos.
- **FR-003**: O sistema DEVE impedir plantões duplicados para a mesma combinação de período,
  data e tipo.

**Escala / alocação**
- **FR-004**: O sistema DEVE permitir que a Gestão abra plantões e aloque/desaloque médicos, e
  que o médico **se inscreva** (auto-escala) em plantões abertos e cancele a própria inscrição.
- **FR-005**: O sistema DEVE bloquear a alocação/inscrição de um médico em plantões com
  horários sobrepostos, explicando o conflito — independentemente de a ação partir da Gestão ou
  do próprio médico.
- **FR-006**: O sistema DEVE apresentar a grade do período mostrando plantões, médicos alocados
  e sinalização de cobertura insuficiente.
- **FR-007**: O médico DEVE conseguir visualizar apenas os seus próprios plantões do período.

**Extras**
- **FR-008**: O médico DEVE conseguir registrar um plantão/horas extras (data, tipo, duração).
- **FR-009**: Extras DEVEM contar para a remuneração a partir do registro (sem aprovação
  prévia); a Gestão pode revisar, ajustar ou remover no fechamento, com registro em auditoria.

**Cobertura / trocas**
- **FR-010**: O sistema DEVE permitir registrar a cobertura de um médico por outro em um
  plantão; a substituição vale a partir do registro (sem aprovação prévia).
- **FR-011**: Após a troca, escala e remuneração DEVEM refletir o médico que efetivamente
  cobriu; a Gestão pode revisar no fechamento, e a alteração fica em auditoria.

**Remuneração**
- **FR-012**: O sistema DEVE calcular, no backend, o valor a pagar por médico em um período,
  considerando os plantões realizados (refletindo as trocas registradas) e os extras
  registrados.
- **FR-013**: O cálculo DEVE usar uma tabela de valores configurável que pode variar por médico
  e por tipo de plantão (não fixos em código). Quando não houver valor específico para um
  médico, aplica-se o valor padrão do tipo de plantão.
- **FR-014**: O sistema DEVE exportar um relatório de remuneração do período consumível pelo
  financeiro.
- **FR-015**: O sistema DEVE controlar alterações em períodos com remuneração fechada (impedir
  ou exigir reabertura auditada).

**Dashboard**
- **FR-016**: O sistema DEVE apresentar à Gestão indicadores operacionais (cobertura, buracos)
  e financeiros (custo) coerentes com o período selecionado.

**Auditoria**
- **FR-017**: O sistema DEVE registrar quem alterou o quê e quando nas operações sensíveis
  (escala, extras, trocas, fechamento e reabertura de folha).

**Acesso**
- **FR-018**: O sistema DEVE autenticar usuários e aplicar controle de acesso por papel
  (Médico, Gestão, Admin), restringindo cada papel às suas ações.
- **FR-019**: O Admin DEVE conseguir criar/editar usuários e atribuir papéis.

**Transversal**
- **FR-020**: Toda regra de negócio, validação e cálculo DEVE ocorrer no backend; o frontend
  apenas apresenta e coleta dados (Princípio II da constituição).

### Key Entities

- **Período**: intervalo (ex.: mês) que agrupa os plantões e serve de unidade para escala,
  fechamento e remuneração. Possui status (aberto/fechado).
- **Plantão**: uma vaga de trabalho em uma data e tipo (diurno/noturno), com cobertura
  esperada e horário; pertence a um período.
- **Médico**: profissional plantonista, com dados de identificação e vínculo às alocações.
- **Alocação (escala)**: relação entre um médico e um plantão (quem faz o quê).
- **Extra**: plantão/horas adicionais registradas por um médico; conta direto para a
  remuneração, sujeito a revisão da Gestão no fechamento.
- **Cobertura/Troca**: substituição de um médico por outro em um plantão; vale a partir do
  registro, sujeita a revisão no fechamento.
- **Tabela de valores**: configuração dos valores a pagar por tipo de plantão, com possibilidade
  de valor específico por médico; base do cálculo de remuneração.
- **Remuneração do período**: resultado do cálculo por médico (valores por plantões e extras),
  com estado de fechamento e artefato de exportação.
- **Registro de auditoria**: histórico de alterações sensíveis (autor, ação, momento).
- **Usuário / Papel**: identidade de acesso e o papel que define suas permissões.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A Gestão consegue abrir a escala de um período (criar período e adicionar
  plantões) e o médico consegue se inscrever nos plantões abertos, ambos sem suporte técnico.
- **SC-002**: Um médico encontra os seus plantões do período em até 1 minuto após o login.
- **SC-003**: 100% das tentativas de alocar um médico em plantões sobrepostos são bloqueadas
  (nenhuma sobreposição chega à folha).
- **SC-004**: A remuneração calculada de um período bate com a conferência manual em 100% dos
  casos de teste (nenhuma diferença de valor por médico).
- **SC-005**: A exportação para o financeiro é gerada em um único fluxo, sem edição manual do
  arquivo.
- **SC-006**: Toda alteração sensível (escala, extras, trocas, fechamento) é rastreável na
  auditoria (autor, ação, data/hora).
- **SC-007**: Nenhuma funcionalidade usada hoje deixa de existir após a simplificação
  (paridade funcional verificada contra esta baseline).

---

## Assumptions

- **Modelo de escala (auto-escala)**: a Gestão abre o período e os plantões; o médico se
  inscreve nos plantões abertos e a Gestão confere. A Gestão também pode alocar diretamente.
  *(Confirmado com o usuário em 2026-07-13.)*
- **Extras e trocas sem aprovação prévia**: contam para a remuneração a partir do registro; o
  controle é a revisão da Gestão no fechamento do período. *(Confirmado em 2026-07-13.)*
- **Valores de remuneração por tabela médico/tipo**: os valores podem variar por tipo de
  plantão e por médico; sem valor específico, usa-se o padrão do tipo. Mantida pela
  Gestão/Admin. *(Confirmado em 2026-07-13.)*
- **Tipos de plantão**: assume-se pelo menos diurno e noturno; outros tipos podem existir como
  configuração.
- **Escala de uso**: dezenas de usuários simultâneos no máximo (aplicação interna).
- **Autenticação**: reaproveita o mecanismo de login/RBAC já existente no sistema.
- **Exportação financeira**: formato tabular consumível pelo financeiro (ex.: planilha);
  integração automática com ERP está fora do escopo desta baseline.

---

## Decisões Confirmadas (2026-07-13)

As três questões abertas da primeira versão foram resolvidas com o usuário:

1. **Propriedade da escala** → auto-escala: a Gestão abre os plantões, o médico se inscreve.
2. **Aprovação de extras/trocas** → não há aprovação prévia; contam direto, revisão no fechamento.
3. **Valores de remuneração** → tabela configurável por médico e por tipo de plantão.
