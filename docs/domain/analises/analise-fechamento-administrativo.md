# Análise do Fechamento Administrativo da Competência

**Sprint:** 9.5 — Competência Administrativa & Governança Financeira
**Data:** 2026-06-27
**Pergunta Fundamental:**

> "Como garantir que uma competência financeira só possa ser encerrada quando todos os requisitos administrativos, operacionais e de auditoria estiverem satisfeitos, preservando rastreabilidade completa para futuras inspeções?"

---

## Resposta

A resposta é: **através de uma cadeia de validação obrigatória e progressiva, onde cada transição administrativa requer conclusão verificável de todos os pré-requisitos, com registro imutável de responsabilidades e evidências.**

O encerramento institucional de uma competência financeira não é meramente uma transição de estado — é um **ato administrativo formal** que exige:

1. **PayrollReadiness** — Validação automatizada de que todos os pré-requisitos estão satisfeitos
2. **ApprovalChecklist** — Checklist completo e verificável de todos os critérios obrigatórios
3. **AdministrativeApproval** — Registro formal do ato de aprovação com responsável, justificativa e versão
4. **AdministrativeLock** — Congelamento administrativo que impede qualquer alteração posterior
5. **ApprovalSnapshot** — Fotografia do estado completo no momento da aprovação

Cada etapa gera **eventos imutáveis** e **snapshots de auditoria** que preservam rastreabilidade completa para futuras inspeções.

---

## Perguntas de Negócio — Respostas

### 1. O que caracteriza uma competência pronta para aprovação?

Uma competência está pronta para aprovação quando **todos** os seguintes pré-requisitos estão satisfeitos:

- **Competência calculada:** A competência deve estar no estado `calculated` ou `reviewed`
- **Snapshot financeiro íntegro:** O FinancialSnapshot deve conter todos os fatos consolidados
- **Remunerações válidas:** Todas as remunerações devem ter sido calculadas com regras válidas
- **Sem inconsistências críticas:** Nenhuma inconsistência do tipo `critical` pode estar pendente
- **Sem extras pendentes:** Todos os extras devem ter sido processados
- **Sem remunerações órfãs:** Toda remuneração deve estar vinculada a um fato financeiro válido
- **Auditoria consistente:** O trail de auditoria deve estar completo e consistente

A validação é executada pelo **PayrollReadiness**, que retorna um resultado binário (ready/not ready) com a lista de pendências.

### 2. Quem pode aprovar?

A aprovação é um ato de responsabilidade que requer papel autorizado:

- **Administrador Financeiro** — Pode aprovar competências dentro de sua área de responsabilidade
- **Diretor** — Pode aprovar qualquer competência, incluindo aquelas de alto valor

**Restrições:**
- O aprovador **não pode ser o mesmo** que executou o cálculo (separação de funções)
- O aprovador deve possuir papel ativo no sistema
- A aprovação é registrada com identificação completa do responsável

### 3. Quem pode reabrir?

Reabertura é uma operação restrita que invalida aprovações anteriores:

- **Administrador Financeiro** — Pode reabrir competências dentro de sua área
- **Diretor** — Pode reabrir qualquer competência
- **Auditor** — Pode solicitar reabertura para fins de auditoria

**Restrições:**
- Reabertura requer **justificativa obrigatória** documentada
- Reabertura gera **nova versão** (nunca sobrescreve)
- Reabertura **invalida** a aprovação e o selo anterior
- Competências em estado `archived` **não podem** ser reabertas

### 4. Quem pode bloquear?

Bloqueio é uma operação administrativa que impede alterações:

- **Administrador Financeiro** — Pode bloquear competências em qualquer estado exceto `archived`
- **Diretor** — Pode bloquear qualquer competência
- **Sistema** — Bloqueio automático após aprovação

**Restrições:**
- Bloqueio é **irreversível** exceto por autorização superior
- Competência bloqueada **não pode** ser exportada, paga ou alterada
- Bloqueio registra responsável e justificativa

### 5. O que impede o fechamento?

Os impedimentos de fechamento são categorizados em:

**Impedimentos Críticos (bloqueiam fechamento):**
- Snapshot financeiro incompleto ou corrompido
- Remunerações com cálculos inválidos
- Inconsistências críticas não resolvidas
- Extras pendentes de processamento
- Regras de remuneração inválidas ou expiradas
- Competência com mais de uma versão ativa sem resolução

**Impedimentos Administrativos (requerem ação):**
- Checklist de fechamento incompleto
- Responsável pela aprovação não identificado
- Justificativa não documentada
- Evidências incompletas

**Impedimentos de Auditoria (requerem verificação):**
- Trail de auditoria incompleto
- Transições de estado inconsistentes
- Snapshots de versão anteriores corrompidos

### 6. Como registrar justificativas?

Justificativas são registradas como parte integrante do processo administrativo:

- **Tipo:** Reabertura, rejeição, exceção, observação
- **Conteúdo:** Texto livre explicativo (mínimo 10 caracteres)
- **Responsável:** Usuário que registrou a justificativa
- **Timestamp:** Data e hora do registro
- **Vinculação:** Vinculada a uma versão específica da competência

**Formato de registro:**
```
Justificativa {
    tipo: str          # "reabertura" | "rejeicao" | "excecao" | "observacao"
    conteudo: str      # Texto explicativo (mínimo 10 caracteres)
    registrado_por: str # Identificação do responsável
    registrado_em: datetime
    versao: int        # Versão da competência
}
```

### 7. Quais evidências devem permanecer armazenadas?

Todas as evidências são preservadas indefinidamente:

- **FinancialSnapshot:** Fotografia dos fatos financeiros no momento do cálculo
- **RemunerationResult:** Resultado completo dos cálculos de remuneração
- **RemunerationRule:** Regras aplicadas no momento (snapshots)
- **PayrollSeal:** Selo imutável criado na aprovação
- **ApprovalChecklist:** Checklist completo com status de cada item
- **AdministrativeApproval:** Registro formal da aprovação
- **AdministrativeLock:** Registro do bloqueio administrativo
- **ApprovalSnapshot:** Fotografia do estado completo na aprovação
- **AuditTrail:** Trilha completa de auditoria com timestamps

**Formato de preservação:**
- Dados são snapshotados (copiados) no momento da aprovação
- Referências a dados vivos são substituídas por cópias imutáveis
- Histórico completo é mantido para auditoria

### 8. Como tratar correções posteriores?

Correções posteriores seguem o processo de reabertura:

1. **Identificação do erro:** Auditor ou administrador detecta inconsistência
2. **Justificativa:** Registro formal do motivo da correção
3. **Reabertura:** Competência retorna ao estado `draft`
4. **Nova versão:** Sistema cria nova versão com dados atualizados
5. **Recálculo:** Competência é recalculada com dados corrigidos
6. **Nova aprovação:** Processo de aprovação é repetido
7. **Preservação:** Versão anterior permanece no histórico

**Restrições:**
- Competências em `archived` não podem ser corrigidas
- Cada correção gera nova versão (nunca sobrescreve)
- Todas as versões são preservadas para auditoria

### 9. Quais riscos administrativos existem?

**Risco de Fraude:**
- Aprovação por usuário não autorizado
- Mitigação: Validação de papel e segregação de funções

**Risco de Erro:**
- Aprovação com dados inconsistentes
- Mitigação: Checklist obrigatório e PayrollReadiness

**Risco de Perda:**
- Perda de evidências ou snapshots
- Mitigação: Snapshot imutável e preservação indefinida

**Risco de Retraabalho:**
- Reabertura excessiva por erros evitáveis
- Mitigação: Checklist rigoroso e validação pré-aprovação

**Risco de Auditoria:**
- Trilha de auditoria incompleta
- Mitigação: Registro automático de todas as transições

**Risco de Conformidade:**
- Não atender requisitos legais de preservação
- Mitigação: Preservação de dados por prazo legal mínimo (5 anos)

---

## Fluxo Administrativo Completo

```
Competência Calculada
        ↓
PayrollReadiness (validação automatizada)
        ↓
ApprovalChecklist (checklist completo)
        ↓
AdministrativeApproval (ato formal)
        ↓
AdministrativeLock (congelamento)
        ↓
ApprovalSnapshot (fotografia final)
        ↓
Competência Oficialmente Encerrada
```

---

## Pergunta Fundamental — Resposta Completa

**"Como garantir que uma competência financeira só possa ser encerrada quando todos os requisitos administrativos, operacionais e de auditoria estiverem satisfeitos, preservando rastreabilidade completa para futuras inspeções?"**

### Solução: Cadeia de Validação Obrigatória e Progressiva

1. **PayrollReadiness** valida automaticamente todos os pré-requisitos técnicos
2. **ApprovalChecklist** documenta formalmente a conclusão de cada critério
3. **AdministrativeApproval** registra o ato administrativo com responsável e justificativa
4. **AdministrativeLock** congela o estado impedindo alterações posteriores
5. **ApprovalSnapshot** preserva fotografia completa do momento da aprovação
6. **Eventos imutáveis** registram cada transição para auditoria futura

**Nenhuma competência pode ser encerrada sem que TODOS os passos anteriores estejam completos e documentados.**

---

## Decisões Deliberadamente Adiadas

1. Assinatura digital ICP-Brasil
2. Workflow configurável por tipo de competência
3. Aprovação paralela (múltiplos aprovadores)
4. Integração com Active Directory
5. Aprovação por certificado digital
6. Integração com ERP
7. Integração bancária

---

## Referências

- docs/domain/glossario-governanca.md
- docs/domain/matriz-aprovacao.md
- docs/domain/checklist-fechamento.md
- docs/domain/invariantes-governanca.md
- docs/domain/casos-borda-governanca.md
