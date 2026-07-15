> ⚠️ **ADR HISTÓRICO — SUPERADO.** Registro mantido para rastreabilidade. A
> [Constituição](../../.specify/memory/constitution.md) (v1.1.0) supera os 31 ADRs onde houver
> conflito — em especial os de *freeze* e a arquitetura DDD/CQRS/event-sourcing, desmontada nas
> specs 003–006 (a `domain/` foi de 118 → ~13 arquivos; payroll/cobertura removidos). Índice e
> contexto em [docs/adr/README.md](README.md).

# ADR-004: SQLite Dev + PostgreSQL Prod

## Status

Aceito

## Data

2026-06-24

## Contexto

Definir banco de dados para desenvolvimento e produção.

## Problema

Equilibrar facilidade de desenvolvimento local com robustez em produção.

## Decisão

- **Desenvolvimento**: SQLite (arquivo local)
- **Produção**: PostgreSQL (container Docker)

## Consequências

### Positivas
- SQLite: Zero config, arquivo único, portável, sem container
- PostgreSQL: ACID completo, concorrência, extensões, backup profissional
- Alembic suporta ambos nativamente
- SQLAlchemy abstrai diferenças

### Negativas
- SQLite não suportaconcorrência de escrita
- Diferenças de SQL entre SQLite e PostgreSQL
- Testes em SQLite podem não revelar bugs de PostgreSQL

## Alternativas Descartadas

1. **PostgreSQL em dev**: Mais pesado, requer container mesmo para dev
2. **MySQL**: Menos features que PostgreSQL para o caso de uso
