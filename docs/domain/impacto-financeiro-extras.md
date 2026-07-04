# Impacto Financeiro — Extras de Plantão

**Data:** 2026-06-26
**Sprint:** 6

---

## 1. O Extra altera remuneração?

**Sim.** O Extra aumenta diretamente a remuneração do Médico.

**Mecanismo:**
- Cada Extra aprovado gera um crédito ao Médico
- O crédito é calculado: `duração × valor_hora × multiplicador`
- O total de Extras é somado à remuneração do período

**Exemplo:**
```
Plantão T1: R$ 500,00
Extra 1: 60min × R$ 50/hora × 1.0 = R$ 50,00
Extra 2: 30min × R$ 50/hora × 1.5 (noturno) = R$ 37,50
Total: R$ 587,50
```

---

## 2. O Extra influencia relatórios?

**Sim.** O Extra alimenta:

| Relatório | Dados utilizados |
|-----------|------------------|
| Relatório de Extras por Médico | Contagem, duração, valores |
| Relatório de Custos por Período | Total de Extras, média |
| Relatório de Aprovações | Pendentes, aprovados, rejeitados |
| Relatório de Padrões | Horários mais comuns, tendências |

---

## 3. O Extra altera fechamento?

**Sim.** O fechamento do período deve considerar:

| Regra | Descrição |
|-------|-----------|
| Extras pendentes | Devem ser resolvidos antes do fechamento |
| Extras aprovados | Entram no cálculo de pagamento |
| Extras rejeitados | Não entram no cálculo |
| Extras cancelados | Não entram no cálculo |

**Fluxo de fechamento:**
1. Verificar se há Extras pendentes
2. Notificar coordenação para aprovação
3. Aguardar resolução de todos os Extras
4. Processar pagamentos
5. Fechar período

---

## 4. O Extra influencia auditoria?

**Sim.** O Extra gera trilha de auditoria:

| Dado | Descrição |
|------|-----------|
| Timestamp de criação | Quando foi registrado |
| Quem registrou | Médico ou coordenação |
| Timestamp de aprovação | Quando foi autorizado |
| Quem aprovou | Qual coordenação |
| Alterações | Histórico de edições |
| Justificativa | Motivo do Extra |

**Importância:** Essencial para auditorias médicas e financeiras.

---

## 5. O Extra gera passivo financeiro?

**Sim.** Cada Extra aprovado gera uma obrigação financeira:

| Status | Passivo |
|--------|---------|
| pending | Potencial (não confirmado) |
| approved | Confirmado (deve ser pago) |
| rejected | Zero (não será pago) |
| cancelled | Zero (não será pago) |

**Gestão do passivo:**
- Dashboard deve mostrar passivo acumulado
- Alertas quando passivo excede orçamento
- Projeções para meses futuros

---

## 6. Preparação para Payroll

O módulo de Payroll (Sprint 8) precisará:

### Dados do Extra

| Campo | Descrição | Uso no Payroll |
|-------|-----------|----------------|
| duration_minutes | Duração em minutos | Cálculo de valor |
| doctor_id | Médico responsável | Identificação do pagável |
| shift_date | Data do Plantão | Competência |
| status | Estado do Extra | Filtrar aprovados |
| justification | Motivo | Auditoria |

### Regras de Negócio

| Regra | Descrição |
|-------|-----------|
| Multiplicador por tipo | Diferentes tipos têm multiplicadores diferentes |
| Limite diário | Máximo de horas extras por dia |
| Limite mensal | Máximo de horas extras por mês |
| Tabela por especialidade | Médicos diferentes podem ter valores diferentes |

### Integração

```
Extras Aprovados → Payroll → Cálculo → Pagamento
```

---

## 7. Resumo Financeiro

| Aspecto | Status | Notas |
|---------|--------|-------|
| Altera remuneração | SIM | Diretamente proporcional |
| Influencia relatórios | SIM | Dados para análise |
| Altera fechamento | SIM | Extras devem estar resolvidos |
| Influencia auditoria | SIM | Trilha completa |
| Gera passivo | SIM | Extras aprovados = obrigação |
| Preparado para Payroll | PARCIAL | Estrutura existe, regras adiadas |
