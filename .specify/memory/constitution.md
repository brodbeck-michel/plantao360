<!--
SYNC IMPACT REPORT
Versão: 1.0.0 → 1.1.0
Tipo de mudança: emenda MINOR — Princípio IV expandido com pipeline de deploy via CI
  (GitHub Actions constrói imagem, servidor apenas baixa e sobe; sem build no servidor).
Histórico:
  (inicial) → 1.0.0: ratificação inicial (MAJOR — primeira versão formal)
Princípios definidos:
  I.   Simplicidade Deliberada (NÃO-NEGOCIÁVEL)
  II.  Regra de Negócio no Backend
  III. Testes do que Importa
  IV.  Deploy Confiável
  V.   Foco no Usuário Real
Seções adicionadas:
  - Restrições Técnicas (stack e estrutura-alvo)
  - Fluxo de Desenvolvimento (Spec-Driven + simplificação incremental)
  - Governança
Templates verificados:
  ✅ plan-template.md — Constitution Check compatível (genérico)
  ✅ spec-template.md — sem conflito
  ✅ tasks-template.md — sem conflito
Follow-up:
  - [FEITO na Fase 3, 2026-07-15] Os 31 ADRs em docs/adr foram marcados como
    histórico (banner em cada + docs/adr/README.md índice). Superados por esta
    constituição onde houver conflito. Mantidos como rastro, não removidos.
-->

# Plantão 360 — Constituição

Aplicação interna de gestão de plantões médicos da Unimed Tubarão. Uso em intranet,
poucas dezenas de usuários (médicos e gestão). Esta constituição existe para manter o
sistema **simples de manter por uma pessoa, e bem feito onde importa**. Ela supera
qualquer prática, ADR ou documento anterior em caso de conflito.

## Princípios Fundamentais

### I. Simplicidade Deliberada (NÃO-NEGOCIÁVEL)

A complexidade é dívida. Cada camada, abstração ou padrão precisa ser justificada por
uma necessidade **concreta e presente** — nunca por antecipação ("pode ser útil") ou por
seguir um padrão de livro.

Regras não-negociáveis:
- **Abstração de consumidor único é proibida.** Se algo é usado em um só lugar, ele mora
  nesse lugar (inline), não em um módulo próprio.
- **Profundidade máxima de camada:** `rota → service → model`. Repositório só entra quando
  a query é genuinamente complexa ou reutilizada.
- **Proibido sem necessidade comprovada:** CQRS, event sourcing, aggregate roots, máquinas
  de estado formais, projeções, read models separados, "engines"/"policies" para cálculos
  que cabem em uma função. Cálculo de negócio é **função testada**, não uma hierarquia.
- **YAGNI.** Não se constrói para requisitos que ninguém pediu.

Rationale: o custo real do projeto hoje não é bug — é peso. Toda camada extra multiplica o
tempo de cada mudança. Menos código é menos superfície para errar.

### II. Regra de Negócio no Backend

Nenhuma regra de negócio, cálculo ou validação de domínio vive no frontend. O frontend
apresenta, coleta e exibe; o backend decide. Toda validação (sobreposição de plantão,
remuneração, competência de folha, transições de status) ocorre exclusivamente no backend
e é a fonte única de verdade.

Rationale: garante consistência independente do cliente e concentra o que é crítico (e
auditável, por envolver pagamento) em um só lugar.

### III. Testes do que Importa

Teste dá confiança para simplificar. A disciplina é pragmática, não dogmática:
- **Obrigatório testar:** regras de negócio de risco (sobreposição de plantão, cálculo de
  remuneração, competência/fechamento de folha) e contratos de API (status, formato).
- **Test-first para regra nova** de negócio: escreva o teste da regra antes de implementá-la.
- **Não perseguir cobertura de código trivial** (getters, mapeamentos, CRUD sem lógica).
- Toda simplificação (inline-and-delete) só é concluída com a suíte relevante **verde**.

Rationale: os testes existem para proteger o que erra caro, não para inflar métrica.

### IV. Deploy Confiável

O que o médico usa tem que ficar de pé. Requisitos inegociáveis de operação:
- **Postgres em produção** (SQLite apenas em desenvolvimento/teste).
- **Migrations versionadas no git** — o histórico de schema é código, não artefato local.
- **Imagem construída no CI, não no servidor.** O GitHub Actions builda as imagens
  (backend e frontend) e publica em registry (GHCR). O servidor de produção **apenas baixa
  a imagem pronta e sobe** (`docker compose pull && up -d`) — nunca `--build`. Deploy é
  reproduzível e cabe em um comando.
- **Startup determinístico:** boot da aplicação não depende de seed; migrations aplicam
  antes do serviço aceitar tráfego; seed é passo manual e explícito, jamais roda
  automaticamente em produção.
- **Backup de banco** rotineiro e restaurável (dado de folha não se perde).

Rationale: a maior fragilidade atual é operacional, não arquitetural. Build no servidor foi
a origem dos loops de restart; mover o build para o CI torna o deploy previsível e simples.
Simplicidade não vale nada sobre um deploy que reinicia em loop.

### V. Foco no Usuário Real

Cada tela, endpoint e tabela existe porque uma pessoa real (médico ou gestão) a usa numa
jornada concreta. Funcionalidade especulativa é candidata a remoção. Antes de construir,
pergunta-se: "qual usuário faz isso, e quando?". Sem resposta clara, não entra.

Rationale: o escopo mínimo que resolve o problema do médico é o alvo — não um sistema
"completo" no papel que ninguém percorre inteiro.

## Restrições Técnicas

**Stack (mantida):**
- Backend: Python 3.12+, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic.
- Frontend: React 18 + TypeScript, MUI, React Query, Vite, react-hook-form.
- Banco: Postgres (produção), SQLite (dev/test). Deploy: Docker Compose.

**Estrutura-alvo do backend (enxuta):**
```
backend/app/
  api/routes/   # endpoints finos
  services/     # regra de negócio (inclui cálculos, como funções)
  models/       # SQLAlchemy
  schemas/      # Pydantic (entrada/saída)
  core/         # config, segurança, logging
  common/       # utilitários genuinamente compartilhados
```
A pasta `domain/` no formato atual (DDD tático/CQRS) é alvo de colapso incremental. Novos
conceitos entram na estrutura acima, não em novas camadas.

## Fluxo de Desenvolvimento

- **Spec-Driven (Spec Kit):** mudanças relevantes passam por `specify → plan → tasks →
  implement`. A spec descreve o *quê* e o *porquê* antes do *como*.
- **Simplificação incremental (inline-and-delete):** remoção de camada é feita módulo a
  módulo — inline no consumidor, suíte verde, deleta. Nunca big-bang.
- **Checkpoint git** antes de cada bloco de mudança estrutural, para retorno limpo.
- **Ponto de partida operacional:** correções de produção (Princípio IV) têm prioridade
  sobre refactor de arquitetura.

## Governança

- Esta constituição supera práticas, ADRs e documentos anteriores onde houver conflito —
  incluindo os ADRs de "freeze". Eles passam a ser registro histórico, não regra vigente.
- **Toda complexidade nova deve ser justificada por escrito** contra o Princípio I. O ônus
  da prova é de quem adiciona camada, não de quem simplifica.
- Revisões (PR/commit) verificam conformidade com os princípios acima.
- **Emendas:** exigem versionamento semântico desta constituição (MAJOR: remoção/redefinição
  de princípio; MINOR: novo princípio/seção; PATCH: ajuste de texto) e uma linha de
  justificativa no Sync Impact Report.

**Version**: 1.1.0 | **Ratified**: 2026-07-13 | **Last Amended**: 2026-07-13
