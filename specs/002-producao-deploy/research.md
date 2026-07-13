# Research — Fase 0: Produção Confiável & Deploy Simples

Decisões técnicas que ancoram o plano. Formato: Decisão / Justificativa / Alternativas
descartadas. Todas guiadas pelo Princípio I (simplicidade).

## D1 — Registry de imagens: GHCR

**Decisão**: publicar as imagens no **GitHub Container Registry** (`ghcr.io/brodbeck-michel/
plantao360-backend` e `-frontend`), autenticando no CI com o `GITHUB_TOKEN` (permissão
`packages: write`).

**Justificativa**: já usamos GitHub; GHCR é gratuito para o repositório, não exige conta/segredo
extra, e integra com `docker/login-action` usando o token nativo. É o caminho de menor atrito
("deploy pelo GitHub", como pedido).

**Alternativas descartadas**: Docker Hub (mais um cadastro/segredo, limites de pull); registry
self-hosted (complexidade desnecessária); ACR/ECR (nuvem paga, fora de escopo interno).

## D2 — Gatilho do build e tags

**Decisão**: workflow `release-images.yml` dispara em **push de tag `v*`** (ex.: `v1.2.0`) e por
**`workflow_dispatch`** (botão manual). Cada imagem recebe duas tags: a versão (`v1.2.0`) e
`latest`. O servidor faz deploy por versão via variável `TAG`.

**Justificativa**: tag = versão explícita e imutável → rollback trivial (apontar `TAG` para a
anterior). `workflow_dispatch` dá um gatilho manual sem precisar criar tag. Evita rebuild a cada
push em `master` (mais barato e previsível).

**Alternativas descartadas**: build a cada push em `master` (imagens demais, sem semântica de
versão); build no merge de PR (o projeto opera direto em `master`, sem fluxo de PR consolidado).

## D3 — Driver PostgreSQL: `psycopg2-binary`

**Decisão**: adicionar `psycopg2-binary` às `requirements.txt`. Manter a URL
`postgresql+psycopg2://...` já esperada em `settings/production.py`.

**Justificativa**: o código de produção **já** referencia `postgresql+psycopg2`; usar o driver
correspondente é a mudança mínima (uma linha). `-binary` dispensa toolchain de compilação na
imagem.

**Alternativas descartadas**: `psycopg` (v3) exigiria trocar a URL para `postgresql+psycopg` e
revalidar; sem ganho para este porte. `asyncpg` exigiria SQLAlchemy async — reescrita grande,
viola simplicidade.

## D4 — PostgreSQL como serviço no Compose

**Decisão**: adicionar serviço `db` (`postgres:16-alpine`) ao `docker-compose.prod.yml`, com
volume dedicado, `healthcheck` via `pg_isready` e variáveis `POSTGRES_USER/PASSWORD/DB`. O
backend usa `depends_on: db: condition: service_healthy`.

**Justificativa**: Postgres suporta escrita concorrente (resolve o "database is locked" do
SQLite). `16-alpine` é enxuto e estável. Tudo no mesmo compose mantém a operação em um lugar.

**Alternativas descartadas**: Postgres gerenciado em nuvem (custo/complexidade, app é interno);
manter SQLite (não aguenta concorrência — é a causa do risco).

## D5 — Espera do banco e migrations no boot

**Decisão**: manter `alembic upgrade head` no `start.sh` (antes de servir), **precedido de uma
espera ativa** pelo banco (`pg_isready`/tentativa de conexão em loop com timeout). O `depends_on
service_healthy` cobre o caso normal; a espera no script é o cinto de segurança. `set -e`
mantém: se a migração falhar, o boot aborta de forma visível.

**Justificativa**: startup determinístico (Princípio IV) sem introduzir orquestração externa.
Migrations no boot são simples e suficientes para um servidor único; a espera evita o loop de
restart quando o Postgres ainda está subindo.

**Alternativas descartadas**: job de migração separado (mais peças para um deploy de um servidor);
init containers/entrypoints elaborados (complexidade desnecessária).

## D6 — Seed nunca em produção

**Decisão**: o `start.sh` já só semeia em `ENVIRONMENT=development` + `DEMO_MODE=true`. Reforçar:
`DEMO_MODE=false` no `.env.production` e documentar o seed como **comando manual**
(`python -m app.seed.seed_data ...`). Nenhuma mudança de lógica de boot além disso.

**Justificativa**: elimina a classe de erro que derrubava o container (seed no boot). Mantém a
possibilidade de semear sob demanda em ambientes de teste.

**Alternativas descartadas**: remover o seed do código (ainda é útil em dev/demo); manter
`DEMO_MODE=true` em produção (confuso e arriscado).

## D7 — Segredos fora da imagem

**Decisão**: segredos (`SECRET_KEY`, `ADMIN_PASSWORD`, `POSTGRES_PASSWORD`) permanecem no
`.env.production` **no servidor** (já fora do git via `.gitignore`), carregados por `env_file` em
runtime. Versionar um `.env.production.example` sem valores. Validar `backend/.dockerignore` para
que nenhum `.env`/`*.db` local entre na imagem.

**Justificativa**: imagem publicada não pode conter segredo (Princípio IV / segurança). `env_file`
em runtime é o mecanismo mais simples do Compose.

**Alternativas descartadas**: Docker secrets/Swarm (orquestração desnecessária); baked na imagem
(inseguro); gestor de segredos externo (fora de escopo para app interno).

## D8 — Backup por `pg_dump`

**Decisão**: `scripts/backup.sh` roda `pg_dump` dentro do container `db`, gerando um arquivo
datado; restauração documentada no `quickstart.md`. Agendamento (cron do servidor) fica como
recomendação operacional.

**Justificativa**: `pg_dump` é a forma padrão, simples e restaurável de backup lógico —
suficiente para o volume e criticidade (folha) desta aplicação.

**Alternativas descartadas**: replicação/PITR (complexidade muito além da necessidade);
ferramentas de backup dedicadas (custo/peso).

## D9 — Versionamento do deploy e rollback

**Decisão**: `docker-compose.prod.yml` referencia `image: ...:${TAG:-latest}`. `scripts/deploy.sh`
recebe `TAG`, faz `docker compose -f docker-compose.prod.yml pull` e `up -d`. Rollback = rodar o
mesmo script com a `TAG` anterior.

**Justificativa**: um único comando, versão explícita, rollback sem rebuild — atende SC-002 e
SC-003 com o mínimo de mecanismo.

**Alternativas descartadas**: scripts de deploy complexos/CD que faz SSH e aplica sozinho (mais
superfície de falha; o operador prefere um comando controlado no servidor nesta fase).

## Riscos e observações

- **Gates de CI existentes** (`architecture.yml`, `release-readiness.yml`) podem reprovar mudanças
  por regras dos ADRs de "freeze". Como a constituição supera os ADRs, se um gate bloquear
  indevidamente, ajustamos/relaxamos o gate (registrar em `tasks.md`). Não é bloqueador do plano.
- **Primeira migração em Postgres**: as migrations foram escritas/rodadas em SQLite. Há risco de
  incompatibilidade de tipos (ex.: `String` sem length, `Boolean`, defaults). Validar migração do
  zero em Postgres é uma tarefa explícita (parte de FR-005/006) antes de considerar a Fase 0 pronta.
- **`app.main:app` vs `app.api.app:app`**: `start.sh` usa `app.main:app`; confirmar o entrypoint
  real ao validar o boot (não alterar sem necessidade).
