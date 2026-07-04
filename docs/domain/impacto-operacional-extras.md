# Impacto Operacional — Extras de Plantão

**Data:** 2026-06-26
**Sprint:** 6

---

## 1. Quem utiliza essa funcionalidade?

| Usuário | Uso |
|---------|-----|
| **Médico** | Registra Extras que sofreu durante o Plantão |
| **Coordenação** | Autoriza/rejeita Extras, visualiza relatórios |
| **Gestão** | Aprova Extras de alto valor, visualiza métricas |
| **Financeiro** | Utiliza dados para processamento de pagamento |

---

## 2. Qual fluxo operacional será alterado?

### Fluxo Atual (sem sistema)

1. Médico trabalha além do horário
2. Médico informa coordenação (verbal/telefone)
3. Coordenação registra em planilha
4. No final do mês, planilha vai para financeiro
5. Financeiro calcula pagamento

### Fluxo Futuro (com sistema)

1. Médico trabalha além do horário
2. Médico registra Extra no sistema
3. Coordenação visualiza e autoriza
4. Sistema mantém registro centralizado
5. No final do período, dados vão para Payroll
6. Payroll calcula pagamento automaticamente

### Benefícios

- Eliminação de planilhas manuais
- Rastreabilidade completa
- Redução de erros
- Aceleração do processo de pagamento
- Visibilidade em tempo real

---

## 3. Quais setores serão impactados?

| Setor | Impacto | Tipo |
|-------|---------|------|
| **Coordenação Médica** | ALTO | Uso diário |
| **Financeiro** | MÉDIO | Dados para pagamento |
| **Gestão Hospitalar** | BAIXO | Relatórios |
| **TI** | BAIXO | Suporte ao sistema |

---

## 4. Quais riscos operacionais existem?

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| Médico não registra Extra | ALTO | Dados incompletos | Facilitar registro |
| Coordenação não autoriza | MÉDIO | Extras pendentes | Alertas automáticos |
| Erro de duração | MÉDIO | Pagamento incorreto | Validação de duração |
| Registro tardio | ALTO | Perda de dados | Deadline de registro |
| Dados duplicados | BAIXO | Pagamento em dobro | Validação de duplicatas |

---

## 5. O que acontece caso um Extra seja lançado incorretamente?

| Erro | Consequência | Correção |
|------|--------------|----------|
| Duração errada | Pagamento incorreto | Editar antes do fechamento |
| Médico errado | Pagamento para pessoa errada | Editar antes do fechamento |
| Sem justificativa | Dados incompletos | Adicionar justificativa |
| Extra fantasma | Pagamento indevido | Remover antes do fechamento |

**Regra:** Após fechamento, correções exigem reabertura do período.
