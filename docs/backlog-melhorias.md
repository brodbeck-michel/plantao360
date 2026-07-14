# Backlog de Melhorias (achados de uso)

Itens levantados navegando o app dev. Todos são **frontend** — não conflitam com a Fase 2
(que é o colapso do `domain/` no **backend**), então podem andar em paralelo, sem risco de
retrabalho.

## B-01 · Criar usuário não funciona (bug de frontend) — ✅ RESOLVIDO (2026-07-13, commit ba5601c)

- **Sintoma**: na aba Usuários, não era possível criar um novo usuário.
- **Causa raiz**: o backend está OK (`POST /users` → 201). Na tela, senha curta (<6) ou dados
  inválidos geravam `422`, mas o erro aparecia como **"Erro ao salvar usuario"** genérico num
  `Alert` no topo da página, **escondido atrás do modal aberto** — parecia que "não dava".
- **Correção**: validação no cliente (nome/email obrigatórios, senha ≥6) com mensagem
  específica; erro exibido **dentro** do dialog; usa a mensagem real do `apiClient`; campos
  `required` + dica "Mínimo 6 caracteres". **Validado no navegador** (senha curta bloqueia com
  mensagem clara; dados válidos criam e atualizam a lista).

## B-02 · Aba Turno: layout sem separação clara entre dia/turno — prioridade MÉDIA

- **Sintoma**: difícil identificar qual dia e qual turno; falta uma linha/separador entre eles.
- **Tipo**: UI/UX (frontend), baixo risco.
- **Escopo**: `frontend/src/features/shift` / grade operacional.

## B-03 · Dashboard: permitir escolher a competência (período) — prioridade MÉDIA

- **Sintoma**: o dashboard puxa a competência automaticamente; não há como trocar o
  período/mês manualmente.
- **Tipo**: pequena melhoria de usabilidade (frontend; o backend de dashboard provavelmente já
  aceita um parâmetro de período — a confirmar).
- **Escopo**: `frontend/src/features/dashboard` (+ verificar se o endpoint aceita período).

## B-04 · Mesmo padrão de erro escondido no dialog "Alterar senha" — prioridade BAIXA

- Descoberto ao corrigir o B-01: `handlePasswordChange` também usa o `Alert` de página (atrás
  do modal). Vale aplicar a mesma correção (erro dentro do dialog) por consistência.
- **Escopo**: `frontend/src/pages/UserListPage.tsx`.

## B-05 · Cache do `index.html` após novo deploy (footgun de deploy) — prioridade MÉDIA

- Descoberto ao testar o B-01: após rebuild do frontend, o navegador continuava servindo o
  `index.html` antigo (com hashes de JS antigos) até um reload forçado com cache-buster.
- **Risco**: depois de um deploy novo, usuários podem ver a versão antiga até dar hard refresh.
- **Correção**: no Nginx, servir `index.html` com `Cache-Control: no-cache` (os assets com hash
  podem ser `immutable`). **Escopo**: `docker/nginx/nginx.conf`. Relevante à Fase 0 (deploy).

## B-06 · Cálculo de remuneração/folha NÃO está implementado (gap funcional) — prioridade ALTA

- Descoberto no levantamento da `domain/` (ver [levantamento-domain.md](levantamento-domain.md)).
- **Fato**: o sistema consolida *quantas horas* cada médico fez (`financial_fact`/`financial_snapshot`
  guardam duração), mas **nunca converte em R$**. `Payroll` não tem campo de valor; o
  `payroll_service` só faz o ciclo de vida (draft→review→approve→export) sem calcular nada. O
  único `hour_rate × duração` está no motor `domain/remuneration`, que **nunca é chamado**.
- **Impacto**: a capacidade "calcular valores a pagar + exportar para o financeiro" (spec 001,
  US5) **não existe de verdade** hoje.
- **Ação (feature, não simplificação)**: implementar de forma simples — função
  `duração × hour_rate` (com a tabela de valores por médico/tipo, conforme decidido), campos de
  valor no `Payroll`/snapshot, e a exportação. Fazer DEPOIS do colapso da `domain/` (para
  construir sobre a base já enxuta), reaproveitando o que for útil do motor antigo antes de
  deletá-lo.
- **Backend, requer decisão de produto** sobre a tabela de valores (já esboçada na spec 001).

### Fórmula útil resgatada do motor morto (antes de deletar, spec 004 T013)

O motor `domain/remuneration/remuneration_calculator.py` (prod=0, nunca chamado) foi removido no
colapso da `domain/`. A fórmula que ele aplicava, resgatada aqui para reaproveitar em B-06:

```
duration_hours     = duration_minutes / 60.0
value_before_mult  = hour_rate × duration_hours
final_value        = value_before_mult × rule.multiplier
```

Onde: `duration_minutes` vem do `financial_fact`/snapshot; `hour_rate` é o valor-hora do médico
(tabela de valores por médico/tipo — decisão de produto da spec 001); `rule.multiplier` é o
multiplicador da regra aplicável (ex.: plantão noturno). A explicação passo-a-passo do cálculo
(minutos→horas, ×valor-hora, ×multiplicador, valor final) também estava embutida ali — útil para
uma futura tela de "como este valor foi calculado".

---

## Nota de timing (recomendação do arquiteto)

- Estes itens são **frontend**; a Fase 2 é **backend** (`domain/`). Não colidem → sem retrabalho.
- **B-01** é bloqueador e isolado → vale corrigir logo.
- **B-02/B-03** são polimento/pequena melhoria → podem ir num lote curto de frontend, sem
  precisar de spec formal (seriam cerimônia demais para o tamanho — Princípio I).
- Nada disso remove funcionalidade; são correções/paridade. Ficam registrados aqui até serem
  feitos.
