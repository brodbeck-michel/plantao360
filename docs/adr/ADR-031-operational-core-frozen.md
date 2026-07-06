# ADR-031: Operational Core Frozen

## Status

Accepted

## Date

2026-07-06

## Context

O core operacional do Plantão360 atingiu estabilidade após 18 sprints de desenvolvimento. As funcionalidades fundamentais — competências, workspace, turnos, médicos, financeiro, relatórios e dashboard — estão funcionando e validadas.

Durante as Sprints 18.1-18.3, foram identificados e corrigidos bugs críticos de infraestrutura:
- Seed script gerava datas de calendário (01-30) em vez de datas de competência (26→25)
- Shift model faltava métodos `before_transition`/`after_transition` causando AttributeError
- Banco de dados SQLite não persistia entre rebuilds do Docker
- Períodos legados (1-5) tinham apenas 3 tipos de turno (T1/T2/T3) em vez de 5 (T1/T2/T3/R1/R2)

## Decision

Congelar (Frozen) o core operacional do Plantão360 a partir da tag `v1-operational-core`.

## Criteria

1. **Funcionalidade completa** — todos os módulos core operam sem bugs conhecidos
2. **Testes manuais aprovados** — criação, edição, exclusão, movimentação funcionam
3. **Dados normalizados** — todos os períodos têm 5 tipos de turno por dia
4. **Persistência garantida** — banco de dados persiste entre rebuilds do Docker
5. **API estável** — endpoints respondem corretamente
6. **Workspace funcional** — grade mostra todos os turnos com assignments

## Benefits

1. **Estabilidade** — o core não sofre alterações acidentais
2. **Previsibilidade** — stakeholders sabem o que está pronto
3. **Foco em homologação** — esforço direcionado para teste, não para desenvolvimento
4. **Base sólida** — funcionalidades futuras são construídas sobre uma base congelada
5. **Rastro de decisão** — ADR documenta o motivo do congelamento

## Consequences

- Alterações no core são restritas a bug fixes
- Novas funcionalidades são implementadas fora do core (módulos opcionais)
- Cada bug fix requer nova tag e validação
- Refatorações são adiadas para releases futuras

## Related

- Sprint 18.1: Fix competency dates in seed
- Sprint 18.2: Fix shift model and complete shift types
- Sprint 18.3: Normalize all legacy periods
- Sprint 18.4: Baseline and freeze
