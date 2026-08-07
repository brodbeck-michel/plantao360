# Implementation Plan: Log de auditoria das ações do usuário

**Branch**: `007-log-auditoria` | **Date**: 2026-08-07 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/007-log-auditoria/spec.md`

## Summary

Criar uma trilha de auditoria real: tabela `audit_logs`, gravação **na mesma transação** das
operações que alteram escala, horas extras, médicos, usuários e competências, endpoint de consulta
restrito a ADMIN/COORDENADOR e uma aba de histórico no workspace. O pacote `app/audit/` atual é
esqueleto declarado como "implementação futura" (`log()` é um `pass`, `AuditLog` não é modelo) —
será **substituído**, aproveitando apenas o enum `AuditAction`. Evidências e alternativas
descartadas: [research.md](research.md); esquema e campos gravados: [data-model.md](data-model.md).

## Technical Context

**Language/Version**: Python 3.12 (backend), TypeScript/React 18 + MUI 5 (frontend)

**Primary Dependencies**: FastAPI, SQLAlchemy 2, Alembic, Pydantic; React Query, MUI

**Storage**: Postgres (produção) / SQLite (dev/teste). Migration `011_audit_logs` (create + drop)

**Testing**: pytest via Docker (`docker compose exec backend python -m pytest app/tests`);
baseline atual **411 passed** (+2 falhas pré-existentes e ambientais em `test_settings_factory`,
que falham também sem esta feature — ver quickstart §1)

**Target Platform**: intranet Docker Compose (imagens via GHCR)

**Project Type**: web app (backend + frontend)

**Performance Goals**: consulta paginada respondendo em <500 ms para a competência corrente;
gravação não pode adicionar mais de uma escrita por operação de negócio

**Constraints**: atomicidade com a operação (FR-003); zero credencial na trilha (FR-004);
somente-leitura pela API (FR-007); nenhuma mudança observável nas jornadas existentes (FR-011)

**Scale/Scope**: 5 recursos, ~15 rotas instrumentadas, 1 tabela nova, 1 endpoint de consulta,
1 aba de frontend

## Constitution Check

*GATE: aprovado (pré-research e re-avaliado pós-design — sem violações).*

- **I. Simplicidade Deliberada**: uma tabela, um service, uma chamada explícita por rota. Foram
  **rejeitados** hooks automáticos de ORM e middleware genérico (research R5) justamente por
  esconderem comportamento. O esqueleto morto de `app/audit/` sai — a feature reduz código não
  usado enquanto adiciona código usado.
- **II. Regra de negócio no backend**: a gravação e o bloqueio por perfil ficam no servidor. A
  ocultação da aba no frontend é conveniência, **não** é o controle — o endpoint responde 403
  independentemente (FR-006), no mesmo padrão adotado no corte financeiro do perfil MEDICO.
- **III. Testes do que importa**: testes cobrem o que quebra em silêncio — gravação nas três
  ações, rollback sem registro, ausência de credencial e 403 por perfil (FR-012). Não haverá teste
  de getter/setter.
- **IV. Deploy Confiável**: tabela criada por migration versionada e reversível; nenhuma alteração
  em tabela existente, então o rollback não arrisca dado operacional.
- **V. Foco no Usuário Real**: a demanda partiu do stakeholder (2026-08-07) e nasceu de uma
  mudança concreta — o médico passou a editar a escala. A US3 (aba no workspace) existe para o
  gestor investigar sem sair da tela onde trabalha.

**Complexity Tracking**: N/A — nenhuma violação a justificar.

## Project Structure

### Documentation (this feature)

```text
specs/007-log-auditoria/
├── spec.md
├── plan.md              # este arquivo
├── research.md          # Fase 0 — estado atual, alternativas descartadas, inventário de rotas
├── data-model.md        # Fase 1 — tabela audit_logs, campos por recurso, invariantes
├── quickstart.md        # Fase 1 — roteiro de validação
├── checklists/requirements.md
└── tasks.md             # Fase 2
```

### Source Code (repository root) — alvos

```text
backend/app/
├── models/audit_log.py                     # NOVO — modelo SQLAlchemy (substitui o contrato morto)
├── models/__init__.py                      # editar: registrar AuditLog
├── audit/models.py, audit/service.py       # DELETAR (contratos vazios — research R1)
├── audit/events.py                         # manter (enum AuditAction reaproveitado)
├── services/audit_service.py               # NOVO — record() + consulta paginada
├── schemas/audit/                          # NOVO — AuditLogResponseDTO, AuditQueryDTO
├── api/routes/audit.py                     # NOVO — GET /audit (ADMIN/COORDENADOR)
├── api/app.py                              # editar: registrar o router
├── api/routes/assignment.py                # editar: gravar create/update/delete (+ lote)
├── api/routes/extra.py                     # editar: gravar create/delete/transições
├── api/routes/doctors.py                   # editar: gravar create/update/ativar-inativar
├── api/routes/users.py                     # editar: gravar create/update/ativar-inativar/senha
├── api/routes/period.py                    # editar: gravar create/update/status
└── tests/…                                 # NOVOS — unit (service) + integration (rotas, 403, rollback)

backend/alembic/versions/
└── 20260807_011_audit_logs.py              # NOVA migration (down_revision = 010_user_doctor_link)

frontend/src/
├── features/operational/services/audit-api.ts                 # NOVO — cliente da consulta
├── features/operational/components/tabs/AuditTab.tsx          # NOVO — aba de histórico
├── features/operational/components/workspace/WorkspaceTabs.tsx # editar: nova aba + visibilidade
├── features/operational/pages/workspace-page.tsx              # editar: render da aba por perfil
└── rbac.ts                                                    # editar: módulo 'auditoria'
```

**Structure Decision**: estrutura existente; nenhum diretório novo além de `schemas/audit/`. O
modelo vai para `models/` (junto dos demais), não para `app/audit/` — o pacote `audit/` fica
apenas com o enum, seguindo a organização já usada no projeto (modelo em `models/`, service em
`services/`, rota em `api/routes/`).

## Decisões de desenho

### D1 · Como o autor chega ao service

Chamada **explícita** a partir da rota, que já recebe `Depends(get_current_user)` e controla o
`db.commit()`. O `AuditService.record(...)` faz `session.add()` no **mesmo** `session` da
operação; o commit da rota persiste os dois efeitos juntos, satisfazendo o FR-003 sem
infraestrutura de contexto. Rejeitados: hooks de ORM e middleware (research R5).

### D2 · Ações em lote (duplicar dia/semana)

**Um registro por atribuição criada** (research R9). É o que responde "quem colocou este plantão",
que é a pergunta original. Para não multiplicar transações, o service expõe `record_many(...)`
com um único `add_all()` — mesma transação, uma ida ao banco.

### D3 · O que fazer com `app/audit/` e seus testes

`models.py` e `service.py` são deletados junto com os testes que exercitam só o contrato vazio
(`test_audit_models.py`, `test_audit_interface.py`). `events.py` (enum `AuditAction`) é mantido e
passa a ser usado de verdade; `test_audit_actions.py` sobrevive. Isso mantém a contagem da suíte
honesta: testes de contrato morto saem, testes de comportamento real entram.

### D4 · Perfil MEDICO

Sem acesso à trilha (FR-006). O bloqueio é no endpoint por `require_role("ADMIN","COORDENADOR")`;
a aba não é renderizada para ele no workspace (mesmo padrão do corte financeiro feito em
2026-08-07: servidor bloqueia, interface acompanha).

### D5 · Resumo legível (`summary`)

Gerado no momento da gravação, em português, com os nomes já resolvidos
(ex.: `"Removeu Maria Oliveira do T3 de 12/07"`). Evita que a tela precise reconstruir texto a
partir do JSON e mantém a trilha legível mesmo se o cadastro mudar depois.

## Estratégia de execução (Fase 2 gera tasks a partir daqui)

Ordem **de dentro para fora**: fundação → gravação → consulta → interface. Cada passo é um commit
com a suíte verde.

1. **Fundação (US1a)**: modelo `AuditLog`, migration 011, `AuditService.record/record_many`,
   remoção dos contratos mortos. Gate: suíte verde; `alembic upgrade head` e `downgrade -1` em
   banco limpo; teste unitário do service (3 ações + invariantes do data-model).
2. **Gravação — escala e extras (US1b)** 🎯 **MVP**: instrumentar `assignment.py` (create, update,
   delete, lote) e `extra.py`. Gate: teste de integração por rota provando o registro; teste de
   rollback (operação que falha não deixa registro).
3. **Gravação — cadastros (US1c)**: `doctors.py`, `users.py`, `period.py`. Gate: teste específico
   provando que a senha **não** aparece na trilha (SC-006).
4. **Consulta (US2)**: `schemas/audit/`, `services/audit_service` (consulta paginada com filtros),
   `routes/audit.py`, registro no `app.py`. Gate: teste de filtros + teste de 403 para
   MEDICO/CONSULTA/FINANCEIRO.
5. **Interface (US3)**: `audit-api.ts`, `AuditTab.tsx`, aba no `WorkspaceTabs`, visibilidade por
   perfil, `rbac.ts`. Gate: validação no navegador (quickstart §4) como ADMIN e como MEDICO,
   com screenshot.

## Riscos e mitigações

| Risco | Mitigação |
|---|---|
| Rota nova esquecer de gravar (buraco silencioso) | Teste por rota (SC-003) + nota no HANDOFF para toda rota que alterar as 5 entidades |
| Trilha crescer sem limite | Fora de escopo por premissa; tabela isolada permite tratar depois sem tocar no operacional. Registrar no backlog |
| Credencial vazar no diff | Lista explícita de campos por recurso (data-model) + teste dedicado (SC-006) |
| Gravação atrapalhar operação em lote | `record_many` com `add_all()` único; medir na validação de duplicar semana |
| Confundir "sem registro" com "nada aconteceu" | Estado vazio da aba informa a data de início da trilha |
