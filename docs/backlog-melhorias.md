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

## B-05 · Cache do `index.html` após novo deploy (footgun de deploy) — ✅ RESOLVIDO (2026-07-15)

- Descoberto ao testar o B-01: após rebuild do frontend, o navegador continuava servindo o
  `index.html` antigo (com hashes de JS antigos) até um reload forçado com cache-buster.
- **Risco**: depois de um deploy novo, usuários podem ver a versão antiga até dar hard refresh.
- **Correção aplicada**: `location = /index.html { expires -1; }` em `docker/nginx/nginx.conf` —
  gera `Cache-Control: no-cache` **sem** `add_header` (que descartaria os security headers
  herdados do bloco `server`, pela regra de herança do Nginx). Assets com hash seguem `immutable`.
- **Validado** com nginx:alpine real + curl: `/`, `/index.html` e rota SPA (`/dashboard`) retornam
  `Cache-Control: no-cache` com os 4 security headers presentes; `.js` segue
  `max-age=31536000, public, immutable`. Vale para dev e prod (mesmo conf na imagem).
- **Nota**: o efeito começa no **próximo** deploy; a transição para essa versão ainda pode exigir
  um último hard refresh (o `index.html` já cacheado não sabe do no-cache).

## B-06 · ~~Cálculo/relatório de folha~~ — ✅ NÃO É GAP (esclarecido pelo stakeholder 2026-07-14)

> **ESCOPO CORRETO:** esta aplicação é de **GESTÃO** de plantões. A **folha oficial** (com
> honorários, impostos etc.) é feita em **outro ERP** — **não** é papel desta app calcular isso.
> O que a app precisa fazer para o pagamento **já existe e está em uso**: a **aba de Relatórios**
> gera um relatório com **valores e horas por médico** em **PDF/Excel**, que é enviado ao financeiro
> para realizar o pagamento e os demais honorários.

- **Conclusão**: **não há gap funcional.** O antigo B-06 ("implementar cálculo de folha") nasceu de
  uma leitura errada da spec 001 — **descartado**. Os "valores" no relatório são apresentação
  (horas × valor-hora), não a folha oficial.
- **Por isso** `domain/remuneration` (motor `duração × hour_rate`) estava morto e foi removido sem
  perda — a app nunca precisou calcular folha.
- **Nice-to-have futuro (opcional, baixa prioridade)**: se algum dado do relatório ainda for montado
  manualmente, dá para acrescentar; mas o fluxo principal (PDF/Excel → financeiro) funciona.

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
