# Casos de Borda — Governança Administrativa da Competência

**Sprint:** 9.5 — Competência Administrativa & Governança Financeira
**Data:** 2026-06-27

---

## CB-G01 — Reabertura após aprovação

**Cenário:** Administrador Financeiro precisa corrigir erro em competência aprovada.

**Comportamento esperado:**
- Requer justificativa obrigatória (mínimo 10 caracteres)
- Gera nova versão (nunca sobrescreve)
- A versão anterior permanece no histórico
- Invalida aprovação e selo anteriores
- AdministrativeLock é removido
- ApprovalSnapshot anterior permanece como registro histórico

**Ação:** Reabrir → justificativa → nova versão → recalcular → revisar → aprovar novamente.

---

## CB-G02 — Reabertura após exportação

**Cenário:** Erro detectado após competência ter sido exportada para sistema externo.

**Comportamento esperado:**
- Requer justificativa detalhada
- Gera nova versão
- Exportação anterior é invalidada
- Sistema externo deve ser notificado (decisão adiada)
- Competência retorna ao estado `draft`

**Ação:** Reabrir → justificativa → nova versão → recalcular → revisar → aprovar → re-exportar.

---

## CB-G03 — Duas aprovações simultâneas

**Cenário:** Dois usuários tentam aprovar a mesma competência ao mesmo tempo.

**Comportamento esperado:**
- Apenas a primeira aprovação é aceita
- A segunda aprovação é rejeitada com erro de concorrência
- Competência fica no estado anterior à aprovação
- Usuário deve retry após verificar estado atual

**Ação:** Sistema detecta conflito → rejeita segunda aprovação → usuário verifica estado → retry.

---

## CB-G04 — Aprovação sem checklist completo

**Cenário:** Usuário tenta aprovar competência sem ter preenchido todo o checklist.

**Comportamento esperado:**
- Sistema rejeita aprovação
- Retorna lista de itens pendentes
- Usuário deve completar checklist antes de aprovar
- Nenhuma exceção é permitida

**Ação:** Sistema valida checklist → rejeita aprovação → retorna pendências → usuário completa checklist → retry.

---

## CB-G05 — Alteração após bloqueio

**Cenário:** Usuário tenta alterar dados de competência bloqueada.

**Comportamento esperado:**
- Sistema rejeita alteração
- Retorna mensagem de erro indicando bloqueio
- Usuário deve solicitar desbloqueio ao Diretor
- Desbloqueio requer justificativa

**Ação:** Sistema detecta bloqueio → rejeita alteração → usuário solicita desbloqueio → Diretor desbloqueia → alteração permitida.

---

## CB-G06 — Perda de evidências

**Cenário:** Evidência essencial (snapshot, seal, checklist) é corrompida ou perdida.

**Comportamento esperado:**
- Sistema detecta evidência faltante durante validação
- Competência não pode ser aprovada
- Requer reconstituição da evidência
- Se reconstituição não é possível, competência deve ser recalculada

**Ação:** Sistema detecta evidência faltante → bloqueia aprovação → usuário reconstitui ou recalcula.

---

## CB-G07 — Aprovação por usuário sem permissão

**Cenário:** Usuário sem papel autorizado tenta aprovar competência.

**Comportamento esperado:**
- Sistema rejeita aprovação
- Retorna erro de permissão
- Usuário não recebe informação sobre o estado da competência (segurança)
- Apenas papel autorizado pode aprovar

**Ação:** Sistema valida permissão → rejeita aprovação → retorna erro de permissão.

---

## CB-G08 — Reabertura de competência arquivada

**Cenário:** Administrador tenta reabrir competência em estado `archived`.

**Comportamento esperado:**
- Sistema rejeita reabertura
- Competências arquivadas são terminais
- Nenhuma ação administrativa é permitida
- Exceção: ordem judicial (decisão adiada)

**Ação:** Sistema rejeita reabertura → retorna erro → competência permanece arquivada.

---

## CB-G09 — Checklist com itens dispensados

**Cenário:** Responsável dispensa itens do checklist com justificativa.

**Comportamento esperado:**
- Itens dispensados devem ter justificativa
- Justificativa deve ter mínimo de 10 caracteres
- Checklist é considerado completo se todos os itens obrigatórios estiverem atendidos
- Itens dispensados são registrados como evidência

**Ação:** Responsável marca item como `waived` → registra justificativa → sistema valida → checklist completo.

---

## CB-G10 — Competência com múltiplas versões

**Cenário:** Competência possui múltiplas versões devido a reaberturas.

**Comportamento esperado:**
- Apenas a versão mais recente está ativa
- Versões anteriores são históricas
- Cada versão é imutável
- ApprovalSnapshot referencia versão específica
- Consultas mostram versão ativa por padrão

**Ação:** Sistema gerencia versões → mantém ativa apenas mais recente → histórico disponível para auditoria.

---

## CB-G11 — Aprovação com segregação de funções violada

**Cenário:** Mesmo usuário que executou cálculo tenta aprovar.

**Comportamento esperado:**
- Sistema rejeita aprovação
- Retorna erro de segregação de funções
- Usuário deve solicitar aprovação a outro usuário
- Nenhuma exceção é permitida

**Ação:** Sistema valida segregação → rejeita aprovação → retorna erro → usuário solicita a outro.

---

## CB-G12 — Desbloqueio sem autorização

**Cenário:** Usuário sem papel superior tenta desbloquear competência.

**Comportamento esperado:**
- Sistema rejeita desbloqueio
- Retorna erro de permissão
- Apenas Diretor pode desbloquear
- Desbloqueio requer justificativa

**Ação:** Sistema valida permissão → rejeita desbloqueio → retorna erro → Diretor desbloqueia.

---

## CB-G13 — Competência com dados inconsistentes após reabertura

**Cenário:** Após reabertura, dados da competência estão inconsistentes.

**Comportamento esperado:**
- PayrollReadiness detecta inconsistências
- Competência não pode ser aprovada
- Requer correção antes de aprovação
- Checklist reflete inconsistências

**Ação:** Readiness detecta → bloqueia aprovação → usuário corrige → revalida → aprova.

---

## CB-G14 — Aprovação parcial (múltiplos departamentos)

**Cenário:** Competência envolve múltiplos departamentos que precisam aprovar.

**Comportamento esperado:**
- Decisão adiada: workflow configurável
- Por enquanto: apenas uma aprovação é necessária
- Departamentos são notificados (decisão adiada)
- Aprovação é registrada por departamento

**Ação:** Por enquanto: aprovação única. Futuro: workflow multi-departamento.

---

## CB-G15 — Timeout de aprovação

**Cenário:** Solicitação de aprovação expira sem resposta.

**Comportamento esperado:**
- Decisão adiada: timeout configurável
- Por enquanto: sem timeout
- Solicitação permanece ativa até aprovação ou rejeição
- Notificação automática (decisão adiada)

**Ação:** Por enquanto: sem timeout. Futuro: timeout configurável.
