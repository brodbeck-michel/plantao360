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
