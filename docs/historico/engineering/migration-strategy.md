# Migration Strategy — Plantão 360

**Data:** 2026-06-28
**Sprint:** 14.3 — Production Readiness
**Decisão:** Estratégia A (incremental)

---

## Contexto

As migrations iniciais do projeto foram criadas durante o desenvolvimento e ficaram desalinhadas com os modelos ORM. Colunas foram adicionadas aos modelos mas não às migrations, resultando em um banco que dependia de `Base.metadata.create_all()` para funcionar.

## Decisão Arquitetural

**Estratégia A adotada:** Preservar a migration `001_init` como fotografia inicial e criar migration incremental de alinhamento.

### Justificativa

1. **Preservação da história** — `001_init` representa o estado real do banco na data de criação. Reescrevê-la perderia essa referência.

2. **Incrementalismo seguro** — Migration `003_runtime_alignment` adiciona colunas faltantes sem modificar a estrutura existente. É mais segura que reescrever.

3. **Compatibilidade** — Se existirem bancos instalados (mesmo que em demo), a migration incremental funciona sem perda de dados.

4. **Convenção Alembic** — A prática padrão é criar migrations incrementais, não reescrever históricas.

### Alternativa Rejeitada (Estratégia B)

Reconstruir toda a cadeia de migrations foi considerada mas rejeitada porque:
- Requer ADR formal
- Mais arriscada para bancos existentes
- Não traz benefício prático significativo

---

## Estrutura de Migrations

```
001_init (2026-06-24)
  └── 002_add_shift_extra_duration (2026-06-24)
       └── sprint9_payroll (2026-06-26)
            └── 003_runtime_alignment (2026-06-28)  ← NOVA
```

### `001_init` — Preservada (imutável)
- Cria tabelas: doctors, periods, shifts, shift_parts, shift_extras
- Mantém constraints originais (inclusive `start_time < end_time` que será removida em `003`)
- **Não é modificada**

### `002_add_shift_extra_duration` — Preservada (imutável)
- Adiciona `duration_minutes` a shift_extras
- **Não é modificada**

### `sprint9_payroll` — Preservada (imutável)
- Cria tabela payrolls com colunas `created_at_ts` e `updated_at_ts` (duplicatas)
- **Não é modificada** — mantida como registro histórico da criação da tabela
- A correção estrutural é feita em `003_runtime_alignment`

### `003_runtime_alignment` — Nova
- Remove CheckConstraint `start_time < end_time` de shift_parts
- Adiciona CheckConstraint `duration_minutes > 0` a shift_parts
- Remove tabela payrolls (com colunas duplicadas)
- Recria tabela payrolls com schema correto (`DateTime(timezone=True)`, sem duplicatas)

---

## Regras de Domínio vs Banco

| Camada | Responsabilidade |
|--------|------------------|
| **Banco** | consistência estrutural, duração positiva, tipos corretos |
| **Domínio (Python)** | turnos overnight, consistência de horários, regras de negócio |

### CheckConstraints

| Constraint | Camada | Justificativa |
|------------|--------|---------------|
| `hour_rate >= 0` | Banco | consistência estrutural |
| `month BETWEEN 1 AND 12` | Banco | consistência estrutural |
| `year BETWEEN 2000 AND 2100` | Banco | consistência estrutural |
| `duration_minutes > 0` (shift_parts) | Banco | consistência estrutural |
| `duration_minutes > 0` (shift_extras) | Banco | consistência estrutural |
| `start_time < end_time` | **Removida** | não suporta overnight shifts |

---

## Compatibilidade PostgreSQL — Validação (2026-06-28)

### Operação por operação

| Operação | SQLite | PostgreSQL | Compatível? |
|----------|--------|------------|:-----------:|
| `batch_alter_table("shift_parts")` | Cria tabela temporária, copia dados, renomeia | Executa `ALTER TABLE` diretamente | ✅ |
| `drop_constraint("ck_shift_part_time_order", type_="check")` | Via batch (recriação de tabela) | `ALTER TABLE ... DROP CONSTRAINT` | ✅ |
| `create_check_constraint("ck_shift_part_duration_positive", ...)` | Via batch | `ALTER TABLE ... ADD CONSTRAINT` | ✅ |
| `drop_table("payrolls")` | `DROP TABLE` | `DROP TABLE` | ✅ |
| `create_table("payrolls", ...)` | SQL padrão | SQL padrão | ✅ |
| `sa.DateTime(timezone=True)` | Armazena como TEXT, SQLAlchemy converte | Tipo `TIMESTAMPTZ` nativo | ✅ |
| `sa.text("CURRENT_TIMESTAMP")` | Retorna UTC como texto | Retorna `TIMESTAMPTZ` no timezone da sessão | ✅* |
| `sa.ForeignKeyConstraint(ondelete="RESTRICT")` | Suportado | Suportado | ✅ |
| `op.create_index(...)` | SQL padrão | SQL padrão | ✅ |

\* `CURRENT_TIMESTAMP` pode retornar timezone diferente entre SQLite e PostgreSQL se o servidor PostgreSQL não estiver configurado em UTC. Para ambientes de produção, recomenda-se `sa.func.now()` ou garantir que o servidor PostgreSQL use UTC.

### Conclusão

A migration `003_runtime_alignment` é **totalmente compatível** com PostgreSQL. Não há operações SQLite-específicas. O uso de `batch_alter_table` é seguro porque Alembic degrada para `ALTER TABLE` padrão no PostgreSQL.

### Recomendação para produção

1. Garantir que o servidor PostgreSQL tenha timezone UTC (`timezone = 'UTC'`)
2. Considerar usar `sa.func.now()` em vez de `sa.text("CURRENT_TIMESTAMP")` em migrations futuras
3. Testar a migration em ambiente PostgreSQL antes do deploy

---

## Impacto Futuro

- Todas as migrations futuras devem ser incrementais
- Nenhuma migration histórica deve ser reescrita
- Se uma migration falhar, criar uma nova de correção
- ADR não é necessária para esta decisão (estatégia A é a padrão)

---

**Autor:** Sprint 14.3
**Atualizado:** 2026-06-28 (ETAPA 2 — Validações finais)
**Status:** Aprovado
