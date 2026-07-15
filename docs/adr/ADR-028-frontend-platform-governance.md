> ⚠️ **ADR HISTÓRICO — SUPERADO.** Registro mantido para rastreabilidade. A
> [Constituição](../../.specify/memory/constitution.md) (v1.1.0) supera os 31 ADRs onde houver
> conflito — em especial os de *freeze* e a arquitetura DDD/CQRS/event-sourcing, desmontada nas
> specs 003–006 (a `domain/` foi de 118 → ~13 arquivos; payroll/cobertura removidos). Índice e
> contexto em [docs/adr/README.md](README.md).

# ADR-028: Frontend Platform Governance

**Date:** 2026-06-27
**Status:** Accepted
**Sprint:** 13.5

---

## Context

O Frontend do Plantão 360 atingiu maturidade suficiente para ser transformado em uma plataforma de desenvolvimento. O Backend já possui Golden Module, IDP, Module Generator, Architecture Validator e Golden Guard. O Frontend precisa de equivalente.

---

## Decision

Declaramos a **Frontend Platform Governance** com os seguintes elementos:

### 1. Golden Lock
- Padrões congelados em `docs/frontend/golden-lock.md`
- Toda evolução requer ADR
- Toda evolução requer atualização do Golden Module
- Toda evolução requer atualização dos Templates
- Toda evolução requer atualização dos Validators

### 2. Feature Generator
- Gera feature completa automaticamente
- Estrutura, types, API, hooks, manifest
- Baseado no Golden Module (Doctor)

### 3. Templates
- Templates para todas as partes de uma feature
- Sincronizados com Golden Module
- Atualizados automaticamente

### 4. Manifest V2
- Campos: name, version, owner, maturity, routes, components, hooks, services, types, tests, shared_dependencies
- Validator obrigatório
- Versionamento

### 5. Architecture Validator V2
- Valida estrutura, imports, naming
- Valida uso de shared components
- Valida ausência de Axios direto
- Gera relatório

### 6. UX Validator
- Valida loading, empty state, error, success
- Valida ARIA, keyboard, screen reader
- Valida responsividade
- Gera relatório

### 7. Template Drift Detector
- Compara features com Golden Module
- Detecta divergências
- Gera relatório

### 8. Component Catalog
- Catálogo automático de componentes
- Props, responsabilidades, reuso
- Preparado para Storybook

### 9. Frontend Score
- Score de qualidade por feature
- Critérios: arquitetura, reuso, performance, a11y, UX, testes
- Grade: A+, A, B, C, D, F

### 10. Feature Maturity
- Níveis: Experimental, Alpha, Beta, Production Ready, Golden
- Processo de promoção definido

### 11. Blueprint Library
- Blueprints oficiais: List, Detail, Form, Wizard, Dashboard, Settings, Timeline, Analytics
- Obrigatórios

### 12. UX Decision Log
- Todas as decisões visuais documentadas
- Nenhuma decisão implícita

### 13. CLI Unificada
- Comandos padronizados
- `npm run feature:create`
- `npm run frontend:validate`
- `npm run frontend:score`
- `npm run frontend:review`
- `npm run frontend:drift`

---

## Consequences

### Positivas
1. **Consistência** — Todas as features seguem mesmo padrão
2. **Velocidade** — Novas features criadas automaticamente
3. **Qualidade** — Validators garantem compliance
4. **Manutenibilidade** — Padrões documentados
5. **Escalabilidade** — Crescimento previsível

### Negativas
1. **Complexidade** — Mais ferramentas para aprender
2. **Overhead** — Processo mais burocrático
3. **Curva de aprendizado** — Equipe precisa conhecer as ferramentas

---

## Implementation

### Arquivos Criados
- `tools/` — 11 ferramentas
- `tools/templates/` — Templates para todas as partes
- `docs/frontend/golden-lock.md`
- `docs/frontend/feature-maturity.md`
- `docs/frontend/blueprint-library.md`
- `docs/frontend/ux-decisions.md`
- `docs/frontend/frontend-idp.md`

---

## References

- `tools/` — Ferramentas do Frontend IDP
- `docs/frontend/golden-lock.md`
- `docs/frontend/feature-maturity.md`
- `docs/frontend/blueprint-library.md`
- `docs/frontend/ux-decisions.md`
- `docs/adr/ADR-027-golden-frontend-module.md`
