# Invariantes — Governança Administrativa da Competência

**Sprint:** 9.5 — Competência Administrativa & Governança Financeira
**Data:** 2026-06-27

---

## Invariantes Fundamentais

### G01 — Competência aprovada é imutável
Após transitar para `approved`, nenhum dado da competência pode ser alterado. Apenas reabertura (que gera nova versão) permite modificação.

### G02 — Toda reabertura exige justificativa
Ao reabrir uma competência, o campo `reopen_reason` deve ser obrigatoriamente preenchido com mínimo de 10 caracteres.

### G03 — Toda aprovação possui responsável
Toda `AdministrativeApproval` deve conter identificação completa do responsável pela aprovação.

### G04 — Nenhuma competência bloqueada pode ser exportada
Uma competência com `AdministrativeLock` ativo não pode transitar para `exported`.

### G05 — Nenhuma competência pode ser paga sem aprovação
Uma competência só pode transitar para `paid` se estiver no estado `approved` ou `exported`.

### G06 — Checklist completo é pré-requisito para aprovação
Nenhuma `AdministrativeApproval` pode ser criada sem que o `ApprovalChecklist` esteja completo (todos os itens obrigatórios atendidos).

### G07 — PayrollReadiness é pré-requisito para checklist
O `ApprovalChecklist` só pode ser preenchido se o `PayrollReadiness` retornar `ready`.

### G08 — Segregação de funções é obrigatória
O usuário que executou o cálculo não pode ser o mesmo que aprova a competência.

### G09 — ApprovalSnapshot é imutável
O `ApprovalSnapshot`, após criado, não pode ser alterado ou removido.

### G10 — AdministrativeApproval é irreversível sem reabertura
Uma aprovação registrada não pode ser desfeita. Apenas reabertura permite modificar a competência.

---

## Invariantes de Transição

### G11 — Transições administrativas seguem ordem definida
O fluxo administrativo segue: `PayrollReadiness → ApprovalChecklist → AdministrativeApproval → AdministrativeLock`. Nenhuma etapa pode ser pulada.

### G12 — Bloqueio requer aprovação prévia
Nenhuma `AdministrativeLock` pode ser criada sem que exista uma `AdministrativeApproval` válida.

### G13 — Desbloqueio requer autorização superior
Apenas usuário com papel superior ao bloqueador pode desbloquear uma competência.

### G14 — Reabertura invalida aprovação e bloqueio
Ao reabrir, tanto a `AdministrativeApproval` quanto o `AdministrativeLock` são invalidados.

### G15 — Estado administrativo é consistente com estado de cálculo
O estado administrativo (aprovado/bloqueado) deve ser consistente com o estado de cálculo da competência.

---

## Invariantes de Dados

### G16 — Justificativa é obrigatória para reabertura
Toda reabertura deve possuir justificativa com mínimo de 10 caracteres.

### G17 — Justificativa é obrigatória para dispensa de checklist
Todo item de checklist dispensado (`waived`) deve possuir justificativa.

### G18 — Responsável deve ser identificado em toda ação administrativa
Toda ação administrativa (aprovação, bloqueio, reabertura) deve conter identificação do responsável.

### G19 — Timestamp é obrigatório em toda ação administrativa
Toda ação administrativa deve conter timestamp de execução.

### G20 — Versão é obrigatória em toda aprovação
Toda `AdministrativeApproval` deve conter o número da versão aprovada.

---

## Invariantes de Auditoria

### G21 — Toda ação administrativa gera evento
Toda ação administrativa deve gerar um evento imutável correspondente.

### G22 — Toda ação administrativa gera registro de auditoria
Toda ação administrativa deve gerar uma entrada no `PayrollAuditSnapshot`.

### G23 — Eventos são imutáveis
Eventos de domínio, após emitidos, não podem ser alterados ou removidos.

### G24 — Snapshots são imutáveis
`ApprovalSnapshot`, `PayrollSeal` e `PayrollVersion`, após criados, não podem ser alterados.

### G25 — Histórico é preservado indefinidamente
Todas as versões, selos, snapshots e eventos devem ser preservados por prazo legal mínimo (5 anos).

---

## Invariantes de Consistência

### G26 — Readiness é consistente com dados
O `PayrollReadiness` deve refletir fielmente o estado dos dados da competência.

### G27 — Checklist é consistente com readiness
O `ApprovalChecklist` deve conter todos os itens verificados pelo `PayrollReadiness`.

### G28 — Aprovação é consistente com checklist
A `AdministrativeApproval` só pode ser criada se o `ApprovalChecklist` estiver completo.

### G29 — Bloqueio é consistente com aprovação
O `AdministrativeLock` só pode ser criado se existir uma `AdministrativeApproval` válida.

### G30 — Snapshot é consistente com aprovação
O `ApprovalSnapshot` deve conter o estado completo no momento da aprovação.

---

## Invariantes de Validação

### G31 — PayrollReadiness não altera estado
O `PayrollReadiness` é um componente de validação que não altera o estado da competência.

### G32 — Checklist não altera estado
O `ApprovalChecklist` é um componente de registro que não altera o estado da competência.

### G33 — Validação é determinística
Dada a mesma entrada, o `PayrollReadiness` sempre produz o mesmo resultado.

### G34 — Checklist é determinístico
Dada a mesma entrada, o `ApprovalChecklist` sempre produz os mesmos itens.

---

## Invariantes de Segurança

### G35 — Nenhuma competência pode ser aprovada sem segregação de funções
A separação entre calculador e aprovador é obrigatória e não pode ser contornada.

### G36 — Nenhuma competência pode ser desbloqueada sem autorização
Desbloqueio requer papel superior ao do bloqueador.

### G37 — Nenhuma competência pode ser alterada após bloqueio
`AdministrativeLock` impede qualquer alteração administrativa.

### G38 — Nenhuma competência pode ser exportada sem aprovação
Exportação requer estado `approved`.

### G39 — Nenhuma competência pode ser paga sem aprovação
Pagamento requer estado `approved` ou `exported`.

---

## Invariantes de Preservação

### G40 — Dados são snapshotados na aprovação
Todos os dados relevantes são copiados para o `ApprovalSnapshot` no momento da aprovação.

### G41 — Referências a dados vivos são substituídas
Após aprovação, referências a dados vivos são substituídas por cópias imutáveis.

### G42 — Preservação é indefinida
Dados preservados devem ser mantidos por prazo legal mínimo (5 anos).
