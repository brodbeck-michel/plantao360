# Glossário Financeiro

**Sprint:** 7
**Data:** 2026-06-26

---

## Termos

### Cobertura
Representação quantitativa de quanto de um plantão foi efetivamente trabalhado por médicos. Expressa em minutos ou horas. Medida por Assignment (período efetivo) e por Extra (horas adicionais aprovadas).

### Fato Operacional
Evento que ocorre no domínio de operações do hospital. Exemplos: criação de plantão, atribuição de médico, cancelamento, conclusão. Fatos operacionais são registrados mas não geram valores financeiros por si só.

### Fato Financeiro
Consolidação de um fato operacional que produz um direito financeiro. Exemplo: Assignment completado gera um FatoFinanceiro do tipo `assignment_completion`. Um mesmo fato operacional pode gerar zero ou um fato financeiro.

### Direito Financeiro
Reconhecimento formal de que um médico possui direito a remuneração por um período específico de trabalho. Representado pelo FinancialSnapshot. O direito existe independentemente de pagamento efetivo.

### Competência
Período mensal (ano-mês) ao qual os fatos financeiros são vinculados. Definido pelo Period. Cada competência possui status: draft → closed → paid.

### Fechamento
Ato de finalizar uma competência para consolidação financeira. Ao fechar, o Coverage Engine executa e gera snapshots. Fechamento não é pagamento.

### Remuneração
Valor monetário devido a um médico por seus direitos financeiros. **Não é calculado nesta sprint.** Apenas os fatos que geram remuneração são consolidados.

### Elegibilidade
Condição que qualifica um fato operacional para gerar direito financeiro. Um Assignment `completed` é elegível. Um Assignment `cancelled` não é.

### Estorno
Revogação de um direito financeiro anteriormente concedido. Ocorre quando: competência é reaberta, Assignment é cancelado após consolidação, Extra é rejeitado após aprovação. Representado pelo evento `financial.fact.revoked.v1`.

### Consolidação
Processo pelo qual o Coverage Engine transforma fatos operacionais em fatos financeiros. Envolve: coleta de dados, validação, detecção de inconsistências, geração de CoverageSnapshot, geração de FinancialSnapshot.

### Snapshot Financeiro (FinancialSnapshot)
Representação definitiva de todos os direitos financeiros de uma competência. Contém lista de fatos financeiros consolidados. Consumido pelo Payroll (Sprint 8).

### Coverage Snapshot (CoverageSnapshot)
Fotografia operacional do plantão. Registra: médicos participantes, intervalos trabalhados, extras válidos, substituições, inconsistências detectadas. Base para o FinancialSnapshot.

### Coverage Engine
Componente de domínio responsável por consolidar cobertura. Não calcula valores. Apenas identifica, valida e registra fatos operacionais elegíveis.

### Financial Fact (FatoFinanceiro)
Registro de um direito financeiro individual. Contém: tipo (assignment/extra), médico, competência, duração, status. Não contém valores monetários.

---

## Diagrama de Relacionamento

```
Fato Operacional
    │
    ▼
Coverage Engine
    │
    ├──→ CoverageSnapshot (fotografia operacional)
    │
    └──→ FinancialSnapshot (consolidação de direitos)
              │
              └──→ FinancialFact (fatos individuais)
                        │
                        └──→ Payroll (Sprint 8)
```
