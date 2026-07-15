# Docs históricos

Documentos mantidos apenas para rastreabilidade. Descrevem estados/processos que **não refletem
mais o sistema atual** — arquivados na Fase 3 (2026-07-15) para desafogar `docs/`.

- **SPRINT0.md**, **sprint-12-completo.md**, **sprint-13-completo.md**, **sprint-13-5-completo.md**
  — relatórios de sprints antigas.
- **golden-module.md**, **golden-module-lock.md** — o padrão "golden module" (arquitetura enterprise
  congelada), removido nas specs 004–006.
- **domain-model-readiness.md** — prontidão do modelo de domínio DDD, colapsado nas specs 004–006.
- **levantamento-domain.md** — o mapa que guiou o colapso da `domain/` (118 → ~13 arquivos). Já
  **executado**; útil só como registro de como foi feito.

Diretórios de governança/tooling da arquitetura enterprise removida (referenciavam scripts
`tools/` que já não existem — o CI legado e o `tools/` foram removidos na Fase 3):

- **architecture/** — processo de mudança e baseline da arquitetura enterprise.
- **developer/** — onboarding no "IDP" (module generators, architecture linters).
- **engineering/** — baselines de engenharia (golden guard, validate_architecture).
- **modules/** — manifestos de módulo (conceito removido).

Fontes vigentes: [Constituição](../../.specify/memory/constitution.md), `docs/HANDOFF.md`,
`docs/deploy.md`, `docs/backlog-melhorias.md` e `specs/`.
