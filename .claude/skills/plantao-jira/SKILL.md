---
name: plantao-jira
description: Automação do fluxo de dev do plantao360 integrado ao Jira (projeto PLANTAOPA) — cria, discute, move e acompanha cards do backlog até o merge em produção. Use quando o usuário pedir para criar card de melhoria/manutenção, mover item de fase, tirar dúvida de regra de negócio, validar ou abrir PR/merge ligado a uma issue PLANTAOPA.
---

# Plantao360 Jira — fluxo automatizado

Skill que EU (Claude Code) opero via comandos Jira (MCP Atlassian) para tocar o ciclo de vida de uma
melhoria/manutenção do projeto plantao360, do backlog até produção. O usuário não mexe no Jira manualmente —
eu crio os cards e movo os status conforme o combinado abaixo. Mesmo processo do `crm-jira` (CRM Lab),
adaptado para os IDs reais do board PLANTAOPA (que não são idênticos — ver mapa abaixo).

## Constantes

- `cloudId`: `18534185-6f51-4d22-88aa-ad4cd6f3ac6a` (site brodbeckmichelatlassian.atlassian.net)
- `projectKey`: `PLANTAOPA`
- Tipo de issue padrão: `Tarefa` (usar `Bug` se for correção de defeito, `História` se for feature maior)

## Mapa de status → transitionId

**Atenção:** os IDs `2` e `3` estão invertidos em relação ao board do CRM Lab — não reutilizar de cabeça.

| Fase | Status Jira | transition id (a partir de qualquer status, são globais) |
|---|---|---|
| 1. Ideia registrada | A fazer (Backlog) | 11 |
| 2. Discutindo escopo/regras | Discução | 21 |
| 3. Escopo fechado, pode implementar | Aprovado para o Dev | 31 |
| 4. Dúvida de regra de negócio durante o dev | Duvida / Regra negocios | 2 |
| 5. Codando | Em Desenvolvimento | 3 |
| 6. Código pronto, aguardando o usuário testar | Pronto p/ Validar | 4 |
| 7. Usuário validou | Aprovado | 5 |
| 8. PR aberto / mergeado | PR aberto / Merge | 6 |
| 9. Em produção (deploy confirmado pelo usuário) | Finalizado | 7 |

Use `transitionJiraIssue` com `cloudId`, `issueIdOrKey` e `transition: {"id": "<id>"}`.
Antes de mover, adicione um comentário curto (`addCommentToJiraIssue`) explicando a mudança — isso vira o
histórico de decisão do card, já que não há board físico sendo olhado em tempo real.

## Comandos (subcomandos do skill)

Args esperados após `/plantao-jira`: `<subcomando> [CHAVE] [texto livre]`.

### `backlog "<ideia>"`
1. Cria issue em `PLANTAOPA` com `createJiraIssue` (fica automaticamente em "A fazer").
2. Resumo (`summary`) curto e objetivo; descrição com o contexto que o usuário deu.
3. Responda ao usuário com a chave (ex: PLANTAOPA-7) e o link, e pergunte se quer discutir escopo agora.

### `discutir <CHAVE>`
1. Transição 21 (Discução).
2. NÃO mova sozinho para "Aprovado para o Dev" — só o usuário decide isso explicitamente
   ("pode implementar", "aprovado", "manda pra dev").

### `aprovar-dev <CHAVE>`
1. Transição 31 (Aprovado para o Dev).
2. Confirme resumo do escopo acordado no comentário antes de mover.

### `iniciar-dev <CHAVE>`
1. Transição 3 (Em Desenvolvimento).
2. Crie branch git a partir de `main`, seguindo a convenção Unimed (`feature/<descricao-curta>` —
   ver `.claude/CLAUDE.md` da Unimed): `feature/PLANTAOPA-<n>-slug-curto`.
3. Comece a implementação normalmente (seguindo as práticas de código do projeto).
4. **Se durante a implementação surgir qualquer dúvida de regra de negócio ou ambiguidade de escopo**:
   pare, rode o subcomando `duvida` (abaixo) e aguarde resposta do usuário antes de continuar codando.
   Não adivinhe regra de negócio.

### `duvida <CHAVE> "<pergunta>"`
1. Comenta a pergunta específica na issue.
2. Transição 2 (Duvida / Regra negocios).
3. Avise o usuário na conversa que o card está travado aguardando resposta.
4. Quando o usuário responder, comente a resposta na issue e volte para transição 3
   (Em Desenvolvimento) automaticamente para continuar o trabalho.

### `pronto-validacao <CHAVE>`
1. Rode a suíte de testes/lint do projeto se existir; só prossiga se passar (ou avise se não passou).
2. Comente um resumo do que foi feito (arquivos alterados, o que testar).
3. Transição 4 (Pronto p/ Validar).
4. Avise o usuário que está pronto para ele validar.

### `aprovar <CHAVE>`
Só executar quando o usuário disser explicitamente que validou/aprovou.
1. Transição 5 (Aprovado).

### `abrir-pr <CHAVE>`
1. Confirme que o card está em "Aprovado" — se não estiver, pergunte antes de prosseguir.
2. Push da branch e `gh pr create` com título referenciando a chave (`PLANTAOPA-<n>: <resumo>`) e corpo
   linkando a issue. Alvo do PR é `main`, conforme a norma Unimed — sem push direto.
3. Comente o link do PR na issue e transição 6 (PR aberto / Merge).
4. **NUNCA faça merge para a branch de produção automaticamente.** Depois do PR aberto, peça o resumo em
   português do que mudou e por quê (norma Unimed de aprovação) e só rode `gh pr merge` após confirmação
   explícita nesta conversa — mesmo que o card já esteja "Aprovado". Merge em prod é sempre manual/confirmado.

## Regras gerais

- Nunca pule etapas silenciosamente (ex: ir direto de Backlog para Em Desenvolvimento) — sempre siga a
  sequência, a menos que o usuário peça explicitamente para pular uma fase.
- Toda transição de status vem acompanhada de um comentário explicando o porquê.
- Se o usuário pedir para "criar um card", assuma `backlog` por padrão, a não ser que ele já diga que quer
  pular direto para dev.
- Merge para produção é a única ação que exige confirmação explícita a cada vez, independente do status do
  card — e segue o ciclo completo descrito no `CLAUDE.md` da Unimed (PR → main → homolog → tag → produção).
