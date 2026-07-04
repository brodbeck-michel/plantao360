# Casos de Borda — Payroll & Competência Financeira

**Sprint:** 9
**Data:** 2026-06-26

---

## CB-P01 — Remuneração alterada após fechamento

**Cenário:** Uma regra de remuneração é alterada após a competência ter sido fechada.

**Comportamento esperado:**
- A competência não é afetada automaticamente
- A regra antiga permanece registrada no PayrollSeal
- Se a alteração deve ser aplicada, requer reabertura com nova versão
- A versão anterior permanece no histórico

**Ação:** Reabrir competência → criar nova versão → recalcular com regras atualizadas.

---

## CB-P02 — Extra aprovado posteriormente

**Cenário:** Um extra é aprovado depois que a competência já foi calculada.

**Comportamento esperado:**
- A competência em `calculated` ou `reviewed` pode ser recalculada
- A competência em `approved` requer reabertura
- O novo extra é incluído no recálculo

**Ação:** Se competência não está aprovada → recalcular. Se aprovada → reabrir.

---

## CB-P03 — Reabertura

**Cenário:** Administrador Financeiro precisa corrigir erro em competência aprovada.

**Comportamento esperado:**
- Requer justificativa obrigatória
- Gera nova versão (nunca sobrescreve)
- A versão anterior permanece no histórico
- Invalida aprovações e exportações anteriores

**Ação:** Reabrir → justificativa → nova versão → recalcular → revisar → aprovar.

---

## CB-P04 — Duas versões

**Cenário:** Existem duas versões da mesma competência.

**Comportamento esperado:**
- Apenas a versão mais recente está ativa
- Versões anteriores são históricas
- Cada versão é imutável
- Consultas mostram a versão ativa por padrão

**Ação:** Consultar versão ativa. Histórico disponível para auditoria.

---

## CB-P05 — Competência vazia

**Cenário:** Uma competência é criada sem dados (nenhum plantão, nenhum extra).

**Comportamento esperado:**
- Cálculo produz resultado com total zero
- Competência pode ser criada e aprovada normalmente
- PayrollSeal contém snapshot vazio
- Validação: pelo menos um médico deve ter sido calculado (regra de negócio)

**Ação:** Se regra permite competência vazia → OK. Se não permite → bloquear com erro.

---

## CB-P06 — Médico removido

**Cenário:** Um médico é desativado após a competência ter sido calculada.

**Comportamento esperado:**
- A competência mantém os dados do médico no snapshot
- Reabertura não remove dados históricos
- Médico permanece no PayrollSeal com todos os dados

**Ação:** Nenhuma ação necessária. Snapshot preserva dados.

---

## CB-P07 — Inconsistências

**Cenário:** O Coverage Engine detecta inconsistências durante consolidação.

**Comportamento esperado:**
- Inconsistências são registradas no CoverageSnapshot
- Competência pode ser calculada mesmo com inconsistências
- Inconsistências são visíveis na revisão
- Revisor decide se aceita ou corrige

**Ação:** Registrar inconsistências → incluir no relatório → revisor decide.

---

## CB-P08 — Rollback

**Cenário:** Erro detectado após início de cálculo.

**Comportamento esperado:**
- Cálculo é atômico: ou completa ou não persiste nada
- Se erro durante cálculo, competência permanece em `draft`
- Se erro durante revisão, competência permanece em `calculated`

**Ação:** Tratar erro → corrigir → reiniciar operação.

---

## CB-P09 — Cancelamento

**Cenário:** Competência é cancelada antes de aprovação.

**Comportamento esperado:**
- Apenas competências em `draft` ou `calculated` podem ser canceladas
- Cancelamento é diferente de reabertura (não gera nova versão)
- Dados são preservados mas competência fica inativa

**Ação:** Cancelar competência → registrar motivo → dados preservados.

---

## CB-P10 — Estorno

**Cenário:** Pagamento precisa ser estornado após marcação como pago.

**Comportamento esperado:**
- Requer reabertura da competência
- Gera nova versão com estorno
- Estorno é registrado como transação financeira
- Competência retorna a estado anterior ao pago

**Ação:** Reabrir → gerar estorno → recalcular → aprovar novamente.
