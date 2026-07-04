# Casos de Borda — Extras de Plantão

**Data:** 2026-06-26
**Sprint:** 6

---

## Casos de Borda Documentados

### CB01 — Extra iniciado antes do plantão

**Cenário:** Médico começa a trabalhar antes do horário previsto na Alocação.

**Decisão:** O Extra é registrado com a duração real trabalhada. O sistema não valida se o início é anterior ao plantão — apenas valida a duração total.

**Impacto:** Nenhum. O Extra é tratado como qualquer outro.

---

### CB02 — Extra encerrado depois da meia-noite

**Cenário:** Plantão termina às 23h, médico trabalha até 01h do dia seguinte.

**Decisão:** O Extra é registrado no Plantão da data original. A duração é calculada em minutos absolutos (120 minutos).

**Impacto:** Nenhum. A data do Plantão é a referência, não a data do término do Extra.

---

### CB03 — Dois Extras consecutivos

**Cenário:** Médico tem um Extra de 30min, depois outro de 30min no mesmo Plantão.

**Decisão:** Cada Extra é uma entidade separada. Ambos são válidos e somados para remuneração.

**Impacto:** Nenhum. O sistema aceita múltiplos Extras por Plantão.

---

### CB04 — Extra durante troca de médico

**Cenário:** Plantão tem troca de médico no meio. O médico que saiu tem um Extra.

**Decisão:** O Extra é vinculado ao médico que efetivamente trabalhou. A Alocação original é referência.

**Impacto:** Nenhum. O vínculo é com o médico, não com a Alocação específica.

---

### CB05 — Extra lançado retroativamente

**Cenário:** Extra de semana passada é registrado agora.

**Decisão:** Permitido se o Período ainda estiver em draft. O sistema registra com timestamp atual.

**Impacto:** Nenhum. O sistema permite registros retroativos dentro do período aberto.

---

### CB06 — Extra removido após fechamento

**Cenário:** Coordenador quer remover um Extra após fechar o período.

**Decisão:** **BLOQUEADO.** O sistema não permite remoção após fechamento.

**Ação necessária:** Reabrir o período, remover o Extra, fechar novamente.

**Impacto:** Processo manual exigido.

---

### CB07 — Extra importado do legado

**Cenário:** Dados de extras de sistema legado precisam ser importados.

**Decisão:** Será necessário processo de importação que:
1. Cria o Período (se não existir)
2. Cria o Plantão (se não existir)
3. Cria a Alocação (se não existir)
4. Cria o Extra com dados do legado

**Impacto:** Módulo de Import (Sprint 9).

---

### CB08 — Extra duplicado

**Cenário:** Mesmo médico, mesmo Plantão, mesma duração, registrados duas vezes.

**Decisão:** O sistema **NÃO** impede duplicação. Cada Extra é uma entidade independente.

**Justificativa:** Podem existir dois Extras legítimos com mesma duração (ex: extensão + emergência).

**Impacto:** A coordenação deve validar manualmente.

---

### CB09 — Extra sem justificativa

**Cenário:** Tentativa de criar Extra sem preencher justificativa.

**Decisão:** **BLOQUEADO.** A justificativa é obrigatória (I04).

**Impacto:** Validação no momento da criação.

---

### CB10 — Extra de duração zero

**Cenário:** Tentativa de criar Extra com duração = 0 minutos.

**Decisão:** **BLOQUEADO.** A duração deve ser maior que zero (I03).

**Impacto:** CheckConstraint no banco de dados.

---

### CB11 — Extra com duração muito longa

**Cenário:** Extra com 48 horas (impossível na prática).

**Decisão:** O sistema aceita. Validar regra de negócio: duração máxima = 24 horas.

**Impacto:** Validação de regra de negócio no Service.

---

### CB12 — Extra para Plantão cancelado

**Cenário:** Tentativa de criar Extra para Plantão com status cancelled.

**Decisão:** **BLOQUEADO.** Plantão cancelado não aceita Extras (I15).

**Impacto:** Validação no momento da criação.

---

### CB13 — Extra para período pago

**Cenário:** Tentativa de criar Extra para Período com status paid.

**Decisão:** **BLOQUEADO.** Período pago não aceita novos Extras (I07).

**Impacto:** Validação no momento da criação.

---

### CB14 — Extra com médico inativo

**Cenário:** Tentativa de criar Extra para Médico com status inactive.

**Decisão:** **BLOQUEADO.** Foreign key RESTRICT impede referência a médico inativo.

**Impacto:** Integridade referencial no banco.

---

## Resumo

| Caso | Decisão | Bloqueado? |
|------|---------|------------|
| CB01 | Permitido | Não |
| CB02 | Permitido | Não |
| CB03 | Permitido | Não |
| CB04 | Permitido | Não |
| CB05 | Permitido | Não |
| CB06 | Bloqueado | SIM |
| CB07 | Futuro (Sprint 9) | N/A |
| CB08 | Permitido | Não |
| CB09 | Bloqueado | SIM |
| CB10 | Bloqueado | SIM |
| CB11 | Validação | SIM |
| CB12 | Bloqueado | SIM |
| CB13 | Bloqueado | SIM |
| CB14 | Bloqueado | SIM |
