# Análise de Negócio — Extras de Plantão

**Versão:** 1.0
**Data:** 2026-06-26
**Sprint:** 6
**Status:** APROVADA

---

## 1. O que é um Extra?

Um **Extra de Plantão** é uma ocorrência de trabalho adicional, fora do horário previsto na Alocação (Assignment), que ocorre durante a execução de um Plantão (Shift).

O Extra representa situações como:
- Médico permaneceu após o término programado do plantão
- Médico iniciou atividade antes do horário previsto
- Necessidade de cobertura temporária durante o plantão
- Situação de emergência que demandou extensão de jornada

**Definição formal:** Um Extra é uma registro de duração (em minutos), vinculado a um Plantão e a um Médico, que representa trabalho adicional ao que foi previsto na Alocação original.

---

## 2. Quando um Extra pode existir?

Um Extra pode existir quando:

| Condição | Obrigatória |
|----------|-------------|
| Existe um Plantão (Shift) válido | SIM |
| Existe um Médico (Doctor) válido | SIM |
| O Plantão está em execução ou foi concluído | SIM |
| O período associado ao Plantão está aberto (draft) | SIM |
| A duração é maior que zero | SIM |
| Existe justificativa documentada | SIM |

**Quando NÃO pode existir:**
- Plantão cancelado
- Período fechado ou pago
- Duração igual ou menor que zero
- Sem justificativa

---

## 3. Quem autoriza um Extra?

| Papel | Responsabilidade |
|-------|------------------|
| **Médico** | Solicita/informa o Extra |
| **Coordenação** | Autoriza/rejeita o Extra |
| **Sistema** | Registra e controla |

**Fluxo de autorização:**
1. Médico informa necessidade de Extra (durante ou após o plantão)
2. Coordenação evalua justificativa
3. Coordenação autoriza ou rejeita
4. Sistema registra decisão

**Nota:** Na fase atual, o sistema apenas registra. A aprovação eletrônica será implementada futuramente.

---

## 4. Quem solicita?

O **Médico** é quem vivencia a situação que gera o Extra. Ele pode:
- Informar diretamente à coordenação
- Registrar no sistema após o plantão
- Solicitar durante a execução do plantão

A coordenação também pode:
- Identificar a necessidade de Extra
- Solicitar registro ao médico
- Registrar em nome do médico (situações especiais)

---

## 5. Quem paga?

A **Instituição (Unimed)** é quem paga os Extras.

O pagamento é processado através do módulo de **Payroll** (Remuneração), que:
1. Coleta todos os Extras aprovados do período
2. Calcula o valor baseado na tabela de remuneração
3. Gera o passivo financeiro
4. Processa o pagamento

**Impacto financeiro:** O Extra aumenta a remuneração do Médico proporcionalmente à duração.

---

## 6. Como é calculado?

O cálculo do valor de um Extra é baseado em:

| Fator | Descrição |
|-------|-----------|
| **Duração** | Tempo em minutos do Extra |
| **Valor hora** | Tabela de remuneração por hora do Médico |
| **Tipo de plantão** | Pode haver multiplicadores (noturno, feriado) |
| **Competência** | Período de referência do pagamento |

**Fórmula básica:**
```
Valor Extra = (Duração em minutos / 60) × Valor Hora × Multiplicador
```

**Nota:** O cálculo completo com multiplicadores será implementado no módulo Payroll (Sprint 8).

---

## 7. O Extra altera o valor do plantão?

**Sim.** O Extra aumenta o valor total da remuneração do Médico para aquele período.

O Extra **NÃO** altera o valor base do Plantão. Ele é um acréscimo independente.

**Relação:**
- Plantão = valor fixo previsto na Alocação
- Extra = valor adicional sobre o que foi trabalhado além do previsto
- Total = Plantão + Extras

---

## 8. O Extra pode existir sem Assignment?

**Não.** Todo Extra está vinculado a um Plantão, e todo Plantão deve ter pelo menos uma Alocação para que haja trabalho.

**Hierarquia:**
```
Período → Plantão → Alocação → Extra
```

O Extra é sempre posterior à Alocação. Ele representa trabalho adicional ao que foi alocado.

**Exceção futura:** Em situações de cobertura de emergência, pode ser necessário criar uma Alocação temporária e depois um Extra. Isso será tratado no módulo de Coverage.

---

## 9. O Extra pode existir após fechamento do período?

**Não.** O fechamento do período congela todos os dados para processamento de pagamento.

**Regra:** Extras devem ser registrados e aprovados antes do fechamento do período.

**Consequência:** Se um Extra for identificado após o fechamento, o processo deve ser:
1. Reabrir o período (se permitido)
2. Registrar o Extra
3. Aprovar o Extra
4. Fechar o período novamente

---

## 10. O Extra pode ser removido?

**Sim, mas com restrições:**

| Estado do Período | Pode remover? |
|-------------------|---------------|
| draft | SIM |
| closed | NÃO |
| paid | NÃO |

**Regras de remoção:**
- Período em draft: remoção permitida
- Período fechado: remoção bloqueada
- Período pago: remoção bloqueada

---

## 11. O Extra pode ser editado?

**Sim, mas com restrições:**

| Campo | Pode editar? | Condição |
|-------|-------------|----------|
| duração_minutes | SIM | Período em draft |
| justification | SIM | Período em draft |
| shift_id | NÃO | Jamais |
| doctor_id | NÃO | Jamais |

**Regra:** Dados que afetam cálculo financeiro não podem ser alterados após fechamento.

---

## 12. Existe limite de quantidade?

**Não há limite técnico no sistema.** Porém, regras de negócio podem limitar:

| Regra | Descrição |
|-------|-----------|
| Limite diário | Médico pode ter no máximo X extras por dia |
| Limite mensal | Médico pode ter no máximo Y extras por mês |
| Limite financeiro | Total de extras não pode exceder Z% do salário |

**Nota:** Essas regras serão implementadas quando o negócio definir os limites específicos.

---

## 13. Existe limite financeiro?

**Sim, potencialmente.** A definição de limites financeiros depende de:

- Política da instituição
- Convenção coletiva
- Regulamentação do conselho médico
- Orçamento disponível

**Nota:** Limites financeiros serão implementados no módulo Payroll.

---

## 14. Existem tipos diferentes de Extra?

**Sim.** Os tipos de Extra podem incluir:

| Tipo | Descrição | Multiplicador |
|------|-----------|---------------|
| **Extensão** | Permanência após término do plantão | 1.0x |
| **Antecipação** | Início antes do horário previsto | 1.0x |
| **Cobertura** | Substituição temporária durante plantão | 1.0x |
| **Emergência** | Situação de urgência | 1.5x |
| **Noturno** | Horário noturno (22h-06h) | 1.5x |
| **Feriado** | Dia feriado | 2.0x |

**Nota:** Os tipos e multiplicadores serão implementados no módulo Payroll.

---

## 15. Resumo das Regras

| Regra | Descrição |
|-------|-----------|
| R01 | Extra pertence a exatamente um Plantão |
| R02 | Extra pertence a exatamente um Médico |
| R03 | Duração deve ser maior que zero |
| R04 | Justificativa é obrigatória |
| R05 | Período deve estar em draft |
| R06 | Extra cancelado não participa da remuneração |
| R07 | Extra removido não participa da remuneração |
| R08 | Dados financeiros não são editáveis após fechamento |
| R09 | Extra é registrado com timestamp |
| R10 | Extra pode ter status (pending, approved, rejected, cancelled) |
