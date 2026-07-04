# Glossário — Governança Administrativa da Competência

**Sprint:** 9.5 — Competência Administrativa & Governança Financeira
**Data:** 2026-06-27

---

| Termo | Definição |
|---|---|
| **Aprovação** | Ato administrativo formal que confirma a correção dos dados de uma competência e autoriza seu encerramento. Registrado com responsável, data, justificativa e versão. Irreversível sem reabertura. |
| **Conferência** | Revisão manual dos totais e detalhes antes de aprovar. Responsável valida: totais por médico, regras aplicadas, explicações, consistência dos dados. |
| **Validação** | Verificação automatizada de que todos os pré-requisitos técnicos estão satisfeitos antes da aprovação. Executada pelo PayrollReadiness. |
| **Fechamento** | Processo administrativo completo que inclui: validação, checklist, aprovação e bloqueio. Transforma competência calculada em documento oficial aprovado. |
| **Reabertura** | Operação restrita que retorna uma competência ao estado de cálculo. Gera nova versão. Requer justificativa. Invalida aprovações anteriores. |
| **Bloqueio** | Congelamento administrativo da competência. Após criado, nenhuma alteração administrativa poderá ocorrer. Irreversível exceto por autorização superior. |
| **Justificativa** | Documento formal que explica o motivo de uma ação administrativa (reabertura, rejeição, exceção). Obrigatória para reaberturas. |
| **Evidência** | Documento ou dado que comprova a ocorrência de um evento ou a correção de um cálculo. Preservado indefinidamente para auditoria. |
| **Pendência** | Item do checklist que ainda não foi atendido. Impede o fechamento até ser resolvido. |
| **Checklist** | Lista completa de critérios obrigatórios que devem ser atendidos antes da aprovação. Cada item possui status (pendente/atendido) e justificativa. |
| **Governança** | Conjunto de regras, processos e controles que garantem a integridade, transparência e conformidade do processo de fechamento da competência. |
| **Competência Administrativa** | Representação formal de uma competência financeira que inclui: validação, checklist, aprovação, bloqueio e snapshot de aprovação. Transforma cálculo em documento oficial. |
| **PayrollReadiness** | Componente responsável por validar se uma competência está apta para fechamento. Retorna resultado binário (ready/not ready) com lista de pendências. Não altera estado. |
| **ApprovalChecklist** | Lista completa de critérios exigidos antes da aprovação. Cada item possui: identificador, descrição, status, justificativa e responsável. |
| **AdministrativeApproval** | Registro formal do ato de aprovação. Contém: responsável, data, justificativa, versão, observações. É um ato irreversível sem reabertura. |
| **AdministrativeLock** | Congelamento administrativo da competência. Após criado, impede qualquer alteração administrativa. Registrado com responsável e timestamp. |
| **ApprovalSnapshot** | Fotografia do estado completo no momento da aprovação. Congela: versão, usuário, timestamp, justificativa, checklist utilizado. Imutável após criação. |
| **Segregação de Funções** | Princípio de governança que impede que o mesmo usuário execute cálculo e aprovação. Reduz risco de fraude e erro. |
| **Rastreabilidade** | Capacidade de rastrear cada ação administrativa até seu responsável, momento e motivo. Garantida por eventos imutáveis e snapshots de auditoria. |
| **Snapshot Administrativo** | Fotografia imutável do estado da competência no momento de uma ação administrativa. Preservada para auditoria futura. |
