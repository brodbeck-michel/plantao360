# Feature Specification: Produção Confiável & Deploy Simples (Fase 0)

**Feature Branch**: `002-producao-deploy`

**Created**: 2026-07-13

**Status**: Draft

**Input**: Estancar a fragilidade operacional do Plantão 360 antes do refactor de arquitetura.
Alinhado ao Princípio IV da constituição (Deploy Confiável).

---

## Contexto e Objetivo

Hoje o deploy de produção é frágil e difícil de operar:
- A imagem é **construída no próprio servidor** (`docker compose ... up --build`), o que já causou
  loops de restart.
- O banco de produção é **SQLite** (impróprio para acesso concorrente de vários usuários).
- As **migrations não estão versionadas no git** (`.gitignore` as exclui).
- Falta rotina de **backup** confiável do banco.

Esta feature entrega um deploy **previsível e simples**: o GitHub constrói as imagens, o
servidor apenas baixa e sobe, sobre Postgres, com migrations versionadas e backup. O alvo é
"subir uma nova versão em produção sem sofrer".

**Fora de escopo**: refactor da arquitetura interna (Fase 2), mudanças funcionais no produto
(paridade mantida). Integração com ERP/Tasy.

---

## User Scenarios & Testing *(mandatory)*

Stakeholder principal: o **operador/TI** (você) que publica e mantém o sistema em produção.

### User Story 1 - Publicar uma nova versão sem build no servidor (Priority: P1)

Ao concluir uma mudança, o operador publica uma nova versão em produção sem compilar nada no
servidor: o GitHub Actions constrói as imagens (backend e frontend) e as publica no registry;
no servidor, um único comando baixa a imagem pronta e sobe.

**Why this priority**: é a dor central relatada e a causa dos loops de restart. Resolve o
problema mais visível no dia a dia.

**Independent Test**: disparar o build no GitHub, depois no servidor rodar o comando de deploy
(pull + up) e ver a nova versão no ar, sem `--build` e sem erro de tabela/seed.

**Acceptance Scenarios**:

1. **Given** um commit publicado, **When** o pipeline de imagem roda, **Then** as imagens de
   backend e frontend ficam disponíveis no registry, versionadas por tag.
2. **Given** as imagens publicadas, **When** o operador roda o comando de deploy no servidor,
   **Then** os serviços sobem a partir das imagens prontas (sem compilar no servidor).
3. **Given** uma versão no ar, **When** o operador precisa voltar à versão anterior, **Then**
   consegue apontar para a tag anterior e subir (rollback) sem rebuild.

---

### User Story 2 - Banco de produção em Postgres (Priority: P1)

O sistema roda em produção sobre PostgreSQL, adequado a múltiplos usuários simultâneos, com as
migrations aplicadas de forma controlada antes de o serviço aceitar tráfego.

**Why this priority**: SQLite trava sob escrita concorrente; é risco direto para a operação
diária de escala e folha.

**Independent Test**: subir o ambiente de produção com Postgres, confirmar que as migrations
aplicam e que a aplicação lê/grava normalmente; simular dois usuários escrevendo sem erro de
lock.

**Acceptance Scenarios**:

1. **Given** o ambiente de produção, **When** os serviços sobem, **Then** a aplicação conecta
   ao Postgres e as migrations estão aplicadas (schema íntegro).
2. **Given** o Postgres indisponível no boot, **When** o backend inicia, **Then** ele aguarda o
   banco ficar saudável antes de tentar migrar/servir (sem loop de restart).
3. **Given** dois usuários gravando ao mesmo tempo, **When** ambos salvam, **Then** não há erro
   de "database is locked".

---

### User Story 3 - Migrations versionadas e histórico de schema no git (Priority: P1)

Todo o histórico de migrations vive no repositório, de modo que qualquer ambiente reproduz o
mesmo schema a partir do git.

**Why this priority**: sem as migrations no git, o schema de produção não é reproduzível — risco
sério para dados de folha.

**Independent Test**: clonar o repositório limpo e aplicar as migrations do zero, obtendo o
schema esperado.

**Acceptance Scenarios**:

1. **Given** o repositório, **When** alguém inspeciona o histórico, **Then** todas as migrations
   existentes estão versionadas (não ignoradas).
2. **Given** um checkout limpo, **When** roda-se a migração do zero, **Then** o schema resultante
   é o mesmo de produção.

---

### User Story 4 - Startup determinístico e seed seguro (Priority: P2)

A aplicação sobe de forma previsível: migrations aplicam antes de servir; o seed de dados
**nunca** roda automaticamente em produção — é um comando manual e explícito.

**Why this priority**: o seed acoplado ao boot foi a origem de falhas; separá-lo remove uma
classe inteira de erro.

**Independent Test**: subir produção e confirmar, pelos logs, que nenhum seed roda; rodar o seed
manualmente em um ambiente de teste e ver que popula sob demanda.

**Acceptance Scenarios**:

1. **Given** ENVIRONMENT=production, **When** o backend sobe, **Then** nenhum seed é executado.
2. **Given** um ambiente onde se deseja dados de exemplo, **When** o operador executa o comando
   de seed manualmente, **Then** os dados são populados sem afetar o fluxo de boot.

---

### User Story 5 - Segredos fora da imagem e backup do banco (Priority: P2)

Segredos (chave da aplicação, senha do admin inicial, credenciais do banco) são fornecidos no
momento do deploy, não embutidos na imagem publicada. Há uma rotina de backup do Postgres
restaurável.

**Why this priority**: segurança e continuidade — dado de folha não pode vazar na imagem nem se
perder.

**Independent Test**: inspecionar a imagem publicada e confirmar que não contém segredos; gerar
um backup do banco e restaurá-lo em um ambiente limpo.

**Acceptance Scenarios**:

1. **Given** a imagem publicada no registry, **When** ela é inspecionada, **Then** não contém
   segredos de produção.
2. **Given** um banco com dados, **When** o backup roda e é restaurado em ambiente limpo,
   **Then** os dados voltam íntegros.

---

### Edge Cases

- **Banco ainda subindo**: backend deve esperar o Postgres ficar saudável (não morrer em loop).
- **Migração falha**: o deploy deve falhar de forma visível, sem deixar o serviço meio-migrado
  aceitando tráfego.
- **Imagem sem a tag pedida**: o comando de deploy deve falhar claramente, não subir versão
  errada silenciosamente.
- **Gates de CI existentes**: os workflows atuais (Architecture Gate, Release Readiness) não
  podem bloquear indevidamente o novo pipeline de imagem — verificar compatibilidade.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: A construção das imagens de backend e frontend DEVE ocorrer no GitHub Actions e
  publicar em registry (GHCR), versionada por tag.
- **FR-002**: O compose de produção DEVE referenciar imagens prontas do registry (não `build:`);
  o servidor NUNCA compila em produção.
- **FR-003**: O deploy em produção DEVE ser executável em um único comando (baixar imagem + subir),
  com suporte a rollback para uma tag anterior.
- **FR-004**: Produção DEVE usar PostgreSQL; o driver correspondente DEVE constar nas dependências
  do backend.
- **FR-005**: O backend DEVE aguardar o banco ficar disponível antes de aplicar migrations e
  aceitar tráfego (sem loop de restart).
- **FR-006**: As migrations DEVEM aplicar automaticamente no deploy, antes de o serviço servir
  requisições; falha de migração DEVE abortar o deploy de forma visível.
- **FR-007**: Todas as migrations DEVEM ser versionadas no git (remover a exclusão do
  `.gitignore` e commitar as existentes).
- **FR-008**: O seed de dados NUNCA DEVE rodar automaticamente em produção; DEVE existir como
  comando manual explícito.
- **FR-009**: Segredos de produção NÃO DEVEM ser embutidos na imagem; DEVEM ser fornecidos no
  deploy (arquivo de ambiente/variáveis no servidor).
- **FR-010**: DEVE existir uma rotina documentada de backup do Postgres, restaurável em ambiente
  limpo.
- **FR-011**: O processo de deploy DEVE ser documentado em um guia curto (passo a passo do
  servidor).

### Key Entities

- **Imagem de produção**: artefato versionado (backend/frontend) publicado no registry e
  consumido pelo servidor.
- **Ambiente de produção**: conjunto de serviços (backend, frontend, banco) definido no compose
  de produção, parametrizado por segredos externos.
- **Backup do banco**: cópia restaurável do estado do Postgres.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Publicar uma nova versão em produção não exige nenhuma compilação no servidor.
- **SC-002**: Um deploy completo (baixar + subir) é feito com **um** comando e sem edição manual
  de arquivos no servidor.
- **SC-003**: Rollback para a versão anterior é feito apontando para a tag anterior, sem rebuild.
- **SC-004**: Sob dois ou mais usuários gravando simultaneamente, não ocorre erro de bloqueio de
  banco.
- **SC-005**: Um checkout limpo reproduz o schema de produção aplicando as migrations do zero.
- **SC-006**: Em produção, nenhum seed roda automaticamente (verificável nos logs de boot).
- **SC-007**: A imagem publicada não contém segredos de produção.
- **SC-008**: Um backup do banco pode ser gerado e restaurado com sucesso em ambiente limpo.

---

## Assumptions

- **Registry**: usa-se o GitHub Container Registry (GHCR) associado ao repositório
  `brodbeck-michel/plantao360`. *(Confirmado: deploy "pelo GitHub".)*
- **Servidor de produção**: Linux com Docker e Docker Compose, com acesso à internet para baixar
  imagens do GHCR.
- **Paridade funcional**: nenhuma funcionalidade muda; esta feature é puramente operacional.
- **Gatilho do build**: assume-se build por tag/release ou por push na branch de produção
  (a definir no plano); rollback por tag.
- **Backup**: assume-se dump do Postgres em arquivo (rotina simples), sem ferramenta externa de
  backup nesta fase.
