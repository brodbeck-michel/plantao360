# Revisão Crítica — Extras de Plantão

**Data:** 2026-06-26
**Sprint:** 6

---

## Perguntas de Revisão

### 1. Existem inconsistências?

**Não.** Todas as regras documentadas são consistentes entre si.

Verificação:
- Invariantes compatíveis com casos de borda ✓
- Impacto financeiro compatível com eventos ✓
- Decisões adiadas não conflitam com implementação atual ✓

---

### 2. Existem conflitos entre regras?

**Não.** As regras são complementares.

Exemplos verificados:
- R05 (período draft) compatível com I06, I07 ✓
- R09 (timestamp) compatível com I08 ✓
- R10 (status) compatível com eventos ✓

---

### 3. Existe risco financeiro?

**Baixo.** O sistema atual apenas registra. O cálculo é posterior.

Riscos identificados:
- Extra com duração incorreta → Validação de duração mitiga
- Extra duplicado → Coordenação valida manualmente
- Extra sem aprovação → Status pending exclui do pagamento

---

### 4. Existe risco jurídico?

**Baixo.** O sistema registra o que a instituição já faz manualmente.

Mitigações:
- Trilha de auditoria completa
- Justificativa obrigatória
- Aprovação documentada

---

### 5. Existe regra não documentada?

**Não.** Todas as regras conhecidas estão documentadas.

Ressalva: Regras de negócio específicas (limites, multiplicadores) serão definidas pela instituição em sprints futuras.

---

### 6. Existe dependência com Payroll?

**Sim, mas não bloqueante.**

Dependências:
- Payroll consumirá dados dos Extras aprovados
- Payroll precisará de tabela de valores
- Payroll precisará de regras de multiplicadores

Mitigação: Estrutura do Extra já fornece todos os dados necessários. Payroll é consumidor, não produtor.

---

## Conclusão

**APROVADO para implementação.**

- Sem inconsistências
- Sem conflitos
- Risco financeiro baixo
- Risco jurídico baixo
- Todas as regras documentadas
- Dependência com Payroll não bloqueante

**Recomendação:** Prosseguir com implementação do módulo.
