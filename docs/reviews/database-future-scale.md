# Database Future Scale Review

**Data:** 2026-06-24

## Cenários de Escala

### 10 Médicos

| Aspecto | Impacto | Nota |
|---------|---------|------|
| Tamanho tabela doctors | ~1 KB | Irrelevante |
| Tabela shifts | ~500 rows/mês | Irrelevante |
| Tabela shift_parts | ~500 rows/mês | Irrelevante |
| Índices | Mínimos | Nenhum ajuste necessário |

### 100 Médicos

| Aspecto | Impacto | Nota |
|---------|---------|------|
| Tamanho tabela doctors | ~10 KB | Irrelevante |
| Tabela shifts | ~5.000 rows/mês | Ainda pequeno |
| Tabela shift_parts | ~5.000 rows/mês | Ainda pequeno |
| Queries por médico | ~50 rows/mês | Índice (doctor_id, shift_id) suficiente |

### 1.000 Médicos

| Aspecto | Impacto | Nota |
|---------|---------|------|
| Tamanho tabela doctors | ~100 KB | Irrelevante |
| Tabela shifts | ~50.000 rows/mês | Moderado |
| Tabela shift_parts | ~50.000 rows/mês | Moderado |
| Tabela shift_extras | ~5.000 rows/mês | Moderado |
| **Atenção** | Consultas por período | Índice (period_id, shift_date) importante |

## Análise de Índices

| Índice | Justificativa | Manter |
|--------|---------------|--------|
| ix_doctors_crm | Lookup por CRM | ✅ |
| ix_doctors_active | Filtro por ativos | ✅ |
| ix_periods_status | Filtro por status | ✅ |
| ix_shifts_period_id | Join com periods | ✅ |
| ix_shifts_shift_date | Filtro por data | ✅ |
| ix_shifts_period_date | Query relatório mensal | ✅ |
| ix_shift_parts_shift_id | Join com shifts | ✅ |
| ix_shift_parts_doctor_id | Query por médico | ✅ |
| ix_shift_parts_doctor_date | Relatório médico | ✅ |
| ix_shift_extras_shift_id | Join com shifts | ✅ |
| ix_shift_extras_doctor_id | Query por médico | ✅ |

## Consultas Críticas

1. **Relatório mensal por período:** (period_id, shift_date) — otimizado
2. **Plantões de um médico:** (doctor_id, shift_id) — otimizado
3. **Médicos ativos:** (active) — otimizado
4. **Períodos por status:** (status) — otimizado

## Remuneração (hour_rate)

| Médicos | Registros/mês | Tamanho |
|---------|---------------|---------|
| 10 | 500 | ~40 KB |
| 100 | 5.000 | ~400 KB |
| 1.000 | 50.000 | ~4 MB |

**Conclusão:** Até 1.000 médicos, nenhum ajuste de escala necessário. Os índices atuais são suficientes.

## Recomendações Futuras (quando necessário)

1. **Particionamento:** Se ultrapassar 1M de registros em shift_parts
2. **Read replica:** Se READ exceder capacidade de um nó
3. **Materialized views:** Se relatórios mensais ficarem lentos
4. **Connection pooling:** Configurar pool_size e max_overflow

## Conclusão

A modelagem atual suporta confortavelmente até 1.000 médicos com operações mensais. Não é necessário otimizar prematuramente.
