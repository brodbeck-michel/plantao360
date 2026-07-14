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

## B-06 · Relatório para pagamento (NÃO é cálculo de folha) — prioridade a confirmar

> **⚠️ CORREÇÃO DE ESCOPO (2026-07-14, direto do stakeholder):** esta aplicação **NÃO calcula a
> folha**. O cálculo/pagamento é feito em **outro ERP**. Aqui o papel é **gestão** dos plantões e,
> para o pagamento, **gerar um relatório** (horas/plantões consolidados por médico na competência)
> que o financeiro/ERP consome. **NÃO implementar motor de cálculo `duração × hour_rate` aqui** —
> seria construir o que o produto não quer (foi por isso que `domain/remuneration` estava morto).

- **Fato**: o sistema já consolida *quantas horas* cada médico fez (`financial_fact`/
  `financial_snapshot` guardam duração). O `payroll_service.export` hoje é só uma **transição de
  status** (`→EXPORTED` + evento), não gera arquivo.
- **A verificar com o produto**: como o relatório para pagamento sai hoje? Se as telas de gestão já
  permitem ver/imprimir/exportar as horas por médico da competência, **não há gap** (B-06 vira só um
  "nice-to-have": botão de exportar CSV/XLSX). Se hoje é manual/inexistente, o item real é **gerar
  esse relatório** (consolidado que já existe → CSV/XLSX/PDF), **não** um cálculo de valores.
- **Backend/leve**, sem regra de negócio nova de cálculo.

*(Nota: a antiga fórmula `duração × hour_rate × multiplier` do motor morto foi removida deste item —
não se aplica: quem calcula valor é o ERP, não esta aplicação.)*

## B-07 · Cluster payroll ainda em `domain/` (dívida de simplificação) — prioridade MÉDIA

- Descoberto ao fechar a spec 005 (colapso final da `domain/`). A meta de tamanho da Fase 2 foi
  atingida (`domain/` 118→32; meta 30–40), mas **restou um cluster acoplado** em `domain/`:
  `payroll_competency.py` (agregado DDD de **717 linhas**: versões, selo imutável, auditoria,
  governança/checklist), `governance.py` (287), `payroll_state_machine.py`, `coverage`, `financial`,
  as data classes de `remuneration` e `base` (AggregateRoot).
- **Por que ficou**: diferente do resto (data classes/regras pequenas), é **comportamento real**.
  Colapsar mecanicamente só relocaria ~1000 linhas para `payroll_service` (~1500 linhas) — relocaliza,
  não **reduz** (o oposto do Princípio I). A simplificação de verdade exige **analisar o fluxo real
  de folha** (o que a API/usuário usa) e remover a cerimônia morta — como fizemos com
  `use_cases/assignments`, read models e os motores mortos — **antes** de mover.
- **Ação (feature própria)**: mapear o uso real do agregado payroll; remover selo/versão/governança/
  auditoria que não forem usados; então colapsar o núcleo restante em `coverage_service`/
  `payroll_service` sem inversão, com `base` por último. **Reforço (correção de escopo B-06):** boa
  parte dessa cerimônia (selo imutável, versionamento, resultado de remuneração) foi construída para
  um cenário de "calcular e lacrar a folha oficial" que **não é o papel deste sistema** (o ERP faz a
  folha). Isso torna o enxugamento ainda mais justificável — muito provavelmente é possível remover,
  não só relocar. Casa com B-06 (o relatório para pagamento), já que mexem no mesmo fluxo.
- **Escopo**: `domain/{payroll,coverage,financial,remuneration,base,state_machines}` + services.
  Paridade garantida pela suíte (632) + testes de API (93).

---

## Nota de timing (recomendação do arquiteto)

- Estes itens são **frontend**; a Fase 2 é **backend** (`domain/`). Não colidem → sem retrabalho.
- **B-01** é bloqueador e isolado → vale corrigir logo.
- **B-02/B-03** são polimento/pequena melhoria → podem ir num lote curto de frontend, sem
  precisar de spec formal (seriam cerimônia demais para o tamanho — Princípio I).
- Nada disso remove funcionalidade; são correções/paridade. Ficam registrados aqui até serem
  feitos.
