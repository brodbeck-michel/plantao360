# ShiftExtra Risk Assessment

**Data:** 2026-06-24

---

## Modelo Atual

```
shift_extras
├── id (PK)
├── shift_id (FK)
├── doctor_id (FK)
├── justification (TEXT)
├── created_at
└── updated_at
```

---

## Perguntas Críticas

### Como a remuneração será calculada?
O cálculo de remuneração de extras requer: `hour_rate × hours`.

**Problema:** Não existe campo de duração/horas no modelo atual.

### Onde a quantidade de horas extras será armazenada?
**NÃO SERÁ.** Não existe campo para isso.

### Existe perda de informação?
**SIM.** Ao registrar um extra, a duração é perdida. Só resta a justificativa.

### É possível reconstruir o valor financeiro apenas com os dados atuais?
**NÃO.** Impossível calcular `doctor.hour_rate × hours` sem o campo `hours`.

---

## Classificação de Risco

| Risco | Classificação | Justificativa |
|-------|---------------|---------------|
| Perda de dados financeiros | **ALTO** | Sem duração, remuneração é impossível |
| Importação de legado | **ALTO** | Dados históricos sem duração não importáveis |
| Relatórios de extras | **ALTO** | Sem horas, relatórios são inúteis |
| Auditoria | **MÉDIO** | Justificativa existe, mas valor não |

---

## Conclusão

**RISCO ALTO.**

O campo `duration_minutes` (ou `hours`) é **obrigatório** antes de iniciar módulos funcionais.

Sem ele:
- Impossível calcular remuneração
- Impossível importar dados legados
- Impossível gerar relatórios financeiros
- Impossível validar RN-04 (extra requer justificativa) com valor
