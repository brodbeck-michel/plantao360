# Research — Log de auditoria das ações do usuário (spec 007)

**Data**: 2026-08-07. Verificações feitas por leitura de código e grep no repositório
(`backend/app/audit/`, `models/`, `api/routes/`, `services/`, `core/`, `docker-compose.prod.yml`,
`frontend/src/features/operational/`).

## R1 · O que existe hoje de auditoria?

- **Decisão**: **não existe auditoria funcional**. O pacote `app/audit/` é contrato vazio e deve
  ser **substituído** por implementação real (não estendido).
- **Rationale**: evidências no código:
  - `app/audit/models.py` — cabeçalho literal *"Audit models - contratos para implementação
    futura"*, `# TODO: Implementar com SQLAlchemy`. `AuditLog` é classe Python pura: sem `Base`,
    sem `__tablename__`, sem colunas mapeadas. **Não existe tabela.**
  - `app/audit/service.py` — *"contratos para implementação futura"*; `AuditService.log()` tem
    corpo `pass` com `# TODO: Persistir no banco de dados`. **Chamar não grava nada.**
  - `app/audit/events.py` — enum `AuditAction`, único artefato aproveitável.
  - `grep` por `AuditService` fora de `app/audit/` e dos testes: **nenhum consumidor**. Os testes
    `test_audit_{models,interface,actions}.py` exercitam apenas o contrato em memória.
- **Alternativas**: estender o esqueleto — rejeitado; não há o que estender além do enum. O
  desenho novo pode reaproveitar `AuditAction` e descartar o resto.

## R2 · As tabelas operacionais guardam autoria?

- **Decisão**: **não**. Nenhum campo de autor em nenhuma tabela; a trilha precisa vir de fora.
- **Rationale**: `ShiftPart` e `ShiftExtra` herdam `TimestampMixin` (`created_at`, `updated_at`
  com `server_default=func.now()` / `onupdate`). Registram **quando**, nunca **quem**. `Doctor` e
  `User` idem (`User` ganhou `doctor_id` em 2026-08-07, sem autoria). Nenhuma tabela tem
  `created_by`/`updated_by`.
- **Alternativas**: adicionar `created_by`/`updated_by` (opção (a) do spec) — rejeitado pelo
  stakeholder: não cobre **remoção**, que é o caso em que a informação desaparece de vez, nem
  guarda valor anterior.

## R3 · Os logs de aplicação servem como trilha?

- **Decisão**: **não servem**. Não identificam o usuário e não sobrevivem ao deploy.
- **Rationale**: dois problemas independentes, cada um já suficiente:
  1. **Sem autor**: `assignment_service` emite `logger.info("assignment.created.v1",
     extra={"assignment_id": ...})`. O `JsonFormatter` (`core/logging.py`) injeta `request_id` e
     `correlation_id` do contexto — **não há `user_id`** em lugar nenhum do formatter nem dos
     `extra`.
  2. **Sem persistência**: `docker-compose.prod.yml` declara volume apenas para o Postgres
     (`plantao360_pg_data`). Os logs vão para stdout do contêiner e **somem quando o contêiner é
     recriado** — o que acontece em todo deploy (`scripts/deploy.sh` faz `up -d`).
- **Alternativas**: adicionar `user_id` ao log + volume/coletor de logs — rejeitado para este
  escopo: resolveria a autoria mas deixaria a consulta fora do produto (grep em arquivo), sem
  filtro por competência e sem controle de acesso por perfil (FR-005/FR-006). Fica registrado
  como melhoria independente de observabilidade.

## R4 · O painel "Histórico" do workspace é auditoria?

- **Decisão**: **não**; é undo/redo de sessão. A US3 adiciona uma visão nova, sem removê-lo.
- **Rationale**: `components/workspace/HistoryPanel.tsx` consome `HistoryAction[]` de
  `hooks/use-undo-redo` — estado React em memória, alimentado pelas ações locais e usado para
  desfazer/refazer. Some ao recarregar a página; não conhece o autor (é sempre o próprio usuário)
  nem persiste.
- **Alternativas**: reaproveitar o painel para exibir a trilha — rejeitado: são conceitos
  diferentes (desfazer ação minha × investigar ação de terceiro). Misturar confundiria o usuário.
  A US3 entra como **aba** do workspace, ao lado das existentes.

## R5 · Onde interceptar para gravar o registro?

- **Decisão**: gravar **na camada de rota/service da operação**, dentro da transação já existente,
  passando o usuário autenticado explicitamente. Sem hooks automáticos de ORM.
- **Rationale**: o padrão do projeto já entrega o usuário na rota via
  `Depends(get_current_user)`, e as rotas controlam a transação (`db.commit()` explícito ao final —
  ver `routes/period.py`, `routes/users.py`). Gravar no mesmo `session` antes do commit garante a
  atomicidade do FR-003 sem infraestrutura nova. Um `event.listen` de SQLAlchemy capturaria tudo
  automaticamente, mas não teria acesso natural ao usuário da requisição (exigiria contexto
  global), gravaria tabelas fora do escopo e tornaria o comportamento implícito — contrário ao
  Princípio I.
- **Alternativas**:
  - *Hooks de ORM (`after_insert`/`after_update`/`after_delete`)*: rejeitado — implícito, capta
    seed/migrations sem querer, e o autor viria de variável de contexto.
  - *Middleware HTTP registrando request/response*: rejeitado — não sabe o id do recurso afetado
    nem o valor anterior; geraria trilha inútil para "quem removeu o plantão X".
  - *Decorator `@audited`* (`validators/audit_decorator.py` existe): avaliado no plan; só entra se
    não exigir mágica de introspecção. Preferência por chamada explícita.

## R6 · Quais rotas precisam gravar (inventário do escopo FR-001)?

- **Decisão**: as rotas abaixo são o alvo; a cobertura é verificada por teste (SC-003).
- **Rationale**: levantamento das rotas que alteram as 5 entidades do FR-001:

| Recurso | Rotas que alteram | Observação |
|---|---|---|
| `assignment` (escala) | `POST /assignments`, `PUT /assignments/{id}`, `DELETE /assignments/{id}` | inclui divisão/ajuste de turno (mesmo endpoint) |
| `assignment` (lote) | duplicar dia / duplicar semana | geram N atribuições — exigem gravação em lote (edge case de volume) |
| `shift_extra` | `POST /extras`, `DELETE /extras/{id}`, transições de status | aprovação/rejeição também são alteração |
| `doctor` | `POST /doctors`, `PUT /doctors/{id}`, ativar/inativar | inclui mudança de RQE/data de carreira, que altera valor/hora |
| `user` | `POST /users`, `PUT /users/{id}`, ativar/inativar, trocar senha | **nunca gravar a senha** (FR-004); registrar apenas "senha alterada" |
| `period` | criar, atualizar, mudar status | fechamento/reabertura de competência |

- **Alternativas**: começar só por `assignment` — rejeitado: `shift_extra` afeta pagamento
  diretamente e é editável pelo médico; sairia incompleto no ponto mais sensível.

## R7 · Como o perfil MEDICO afeta o desenho?

- **Decisão**: a trilha é **invisível** para MEDICO (FR-006), e a aba do workspace não é
  renderizada para ele (FR-009).
- **Rationale**: em 2026-08-07 o MEDICO passou a editar a planilha e teve o acesso reduzido a
  Planilha + Financeiro, com o financeiro de terceiros cortado **no servidor**
  (`workspace_service._doctor_payload`, `routes/dashboard.py`). A trilha exporia justamente o que
  foi cortado (quem trabalhou onde, alterações de valor/hora de colegas) — precisa do mesmo
  cuidado: bloqueio no endpoint, não só ocultação da aba.
- **Alternativas**: permitir que o médico veja a própria trilha — não pedido; adiciona filtro e
  superfície sem demanda. Registrado como possibilidade futura.

## R8 · Formato do "antes/depois"

- **Decisão**: JSON com **apenas os campos declarados por recurso**, e no `update` apenas os
  campos que efetivamente mudaram.
- **Rationale**: atende FR-004 (nada de credencial) e mantém o registro legível e pequeno.
  Serializar o objeto inteiro arrastaria `password_hash` no caso de `user` e campos irrelevantes
  nos demais. A lista explícita por recurso é a proteção — não depende de lembrar de filtrar.
- **Alternativas**: guardar o payload bruto da requisição — rejeitado: não tem o valor anterior,
  não tem o resultado real após validação, e carrega o que o cliente mandou (inclusive senha).

## Riscos residuais

- **Retenção/crescimento**: sem expurgo nesta fase (premissa da spec). Se o volume crescer além do
  previsto, entra como dívida — a tabela é isolada, então tratar depois não afeta o resto.
- **Cobertura incompleta**: se uma rota nova alterar as entidades sem gravar, a trilha fica com
  buraco silencioso. Mitigação: teste por rota (SC-003) e nota no HANDOFF para novas rotas.
- **Ações em lote**: duplicar semana pode gerar dezenas de registros de uma vez; o plan deve
  definir se grava um registro por atribuição (rastreável, verboso) ou um agregado (compacto,
  menos preciso). Preferência inicial: **um por atribuição**, por ser o que responde "quem
  colocou este plantão".
