# Database Compatibility — SQLite x PostgreSQL

**Data:** 2026-06-24

## Tipos de Dados

| Tipo SQLAlchemy | SQLite | PostgreSQL | Compatível |
|-----------------|--------|------------|------------|
| Integer | INTEGER | INTEGER | ✅ |
| String(N) | VARCHAR | VARCHAR | ✅ |
| Text | TEXT | TEXT | ✅ |
| Numeric(10,2) | DECIMAL | NUMERIC | ✅ |
| Boolean | INTEGER (0/1) | BOOLEAN | ✅ |
| Date | TEXT (ISO) | DATE | ✅ |
| Time | TEXT (ISO) | TIME | ✅ |
| DateTime(tz=True) | TEXT (ISO) | TIMESTAMPTZ | ✅ |

## Constraints

| Constraint | SQLite | PostgreSQL | Compatível |
|------------|--------|------------|------------|
| PRIMARY KEY | ✅ | ✅ | ✅ |
| FOREIGN KEY | ✅* | ✅ | ✅ |
| UNIQUE | ✅ | ✅ | ✅ |
| NOT NULL | ✅ | ✅ | ✅ |
| CHECK | ✅** | ✅ | ✅ |
| DEFAULT | ✅ | ✅ | ✅ |

\* SQLite não enforce FK por padrão. SQLAlchemy emite `PRAGMA foreign_keys=ON`.
\*\* SQLite suporta CHECK desde versão 3.37.0 (2021).

## Índices

| Feature | SQLite | PostgreSQL | Compatível |
|---------|--------|------------|------------|
| CREATE INDEX | ✅ | ✅ | ✅ |
| Unique Index | ✅ | ✅ | ✅ |
| Composite Index | ✅ | ✅ | ✅ |

## Enums

| Feature | SQLite | PostgreSQL | Compatível |
|---------|--------|------------|------------|
| ENUM type nativo | ❌ | ✅ | ⚠️ |
| VARCHAR + CHECK | ✅ | ✅ | ✅ |

**Decisão:** Usar VARCHAR + CHECK constraint para compatibilidade.

## ON DELETE Actions

| Action | SQLite | PostgreSQL | Compatível |
|--------|--------|------------|------------|
| CASCADE | ✅ | ✅ | ✅ |
| RESTRICT | ✅ | ✅ | ✅ |
| SET NULL | ✅ | ✅ | ✅ |
| SET DEFAULT | ✅ | ✅ | ✅ |

## server_default

| Valor | SQLite | PostgreSQL | Compatível |
|-------|--------|------------|------------|
| CURRENT_TIMESTAMP | ✅ | ✅ | ✅ |
| func.now() | ✅ | ✅ | ✅ |

## Pontos de Atenção

1. **PRAGMA foreign_keys:** Necessário habilitar em SQLite para enforcement de FK
2. **Tipo Numeric:** SQLite armazena como TEXT internamente — compatível
3. **Boolean:** SQLite usa 0/1, PostgreSQL usa true/false — SQLAlchemy abstrai
4. **Time/Date:** SQLite armazena como TEXT ISO — SQLAlchemy abstrai

## Conclusão

O modelo atual é **totalmente compatível** entre SQLite e PostgreSQL sem necessidade de ajustes.
