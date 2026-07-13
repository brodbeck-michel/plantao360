# Quickstart — Deploy e Validação (Fase 0)

Runbook para publicar e operar o Plantão 360 em produção após a Fase 0. Serve também como
roteiro de validação dos critérios de sucesso da [spec](./spec.md). Os arquivos citados
(`release-images.yml`, `docker-compose.prod.yml`, `scripts/*`) são produzidos na implementação
(`/speckit-tasks` → `/speckit-implement`).

## Pré-requisitos

- **Servidor**: Linux com Docker + Docker Compose v2, acesso à internet.
- **GitHub**: repositório `brodbeck-michel/plantao360` com GitHub Actions habilitado e
  permissão de `packages: write` (para publicar no GHCR).
- **Servidor autenticado no GHCR** (uma vez): `docker login ghcr.io` com um token de acesso
  pessoal com escopo `read:packages` (imagens podem ser privadas).
- **`.env.production` no servidor** (fora do git), a partir de `.env.production.example`, com
  `SECRET_KEY`, `ADMIN_PASSWORD`, `POSTGRES_PASSWORD`, `DATABASE_URL` e `TAG`.

## Fluxo 1 — Publicar uma nova versão (no GitHub)

1. Criar e enviar uma tag de versão:
   ```bash
   git tag v1.2.0 && git push origin v1.2.0
   ```
   (ou disparar o workflow manualmente pela aba Actions → *Release Images* → *Run workflow*.)
2. O workflow `release-images.yml` constrói e publica no GHCR:
   - `ghcr.io/brodbeck-michel/plantao360-backend:v1.2.0` (+ `latest`)
   - `ghcr.io/brodbeck-michel/plantao360-frontend:v1.2.0` (+ `latest`)

**Valida SC-001** (nenhuma compilação no servidor) e **FR-001/002**.

## Fluxo 2 — Deploy no servidor (um comando)

```bash
cd /apps/plantao360
TAG=v1.2.0 ./scripts/deploy.sh          # faz: docker compose -f docker-compose.prod.yml pull && up -d
```

O script baixa as imagens da `TAG` e sobe os serviços (db → backend → frontend). O backend
espera o Postgres ficar saudável, aplica as migrations e só então serve.

**Valida SC-002** (deploy em um comando, sem editar arquivo) e **FR-003/005/006**.

## Fluxo 3 — Rollback

```bash
TAG=v1.1.0 ./scripts/deploy.sh          # volta para a versão anterior, sem rebuild
```

**Valida SC-003** e **FR-003**.

## Validações de aceite (checklist de campo)

| Critério | Como verificar | Espera-se |
|---|---|---|
| **SC-004** (sem lock) | Dois usuários gravam escala/plantão ao mesmo tempo | Nenhum erro de banco; ambos salvam |
| **SC-005** (schema reproduzível) | Em ambiente limpo: subir só o `db` e rodar `alembic upgrade head` do zero | Schema completo, sem erro |
| **SC-006** (seed off) | `docker logs plantao360_backend_prod \| grep -i seed` | Nenhum seed executado em produção |
| **SC-007** (imagem sem segredo) | `docker history` / inspecionar camadas da imagem backend | Sem `SECRET_KEY`/senhas embutidas |
| **SC-008** (backup) | Rodar `scripts/backup.sh`, restaurar em banco limpo | Dados voltam íntegros |

## Fluxo 4 — Backup e restauração

```bash
# Backup (gera arquivo datado em ./backups)
./scripts/backup.sh                     # docker exec plantao360_db pg_dump ... > backups/plantao360_YYYY-MM-DD.sql

# Restauração em ambiente limpo
docker exec -i plantao360_db psql -U <user> -d plantao360 < backups/plantao360_YYYY-MM-DD.sql
```

Recomenda-se agendar `scripts/backup.sh` no cron do servidor (ex.: diário). **Valida FR-010.**

## Primeira migração para Postgres (atenção)

As migrations existentes nasceram em SQLite. **Antes de considerar a Fase 0 concluída**, validar
a migração do zero em Postgres (SC-005). Se algum tipo/atributo for incompatível (ex.: `String`
sem length, defaults, `Boolean`), corrigir a migration correspondente — é uma tarefa explícita do
plano, não um ajuste de última hora.

## Guia operacional completo

O passo a passo definitivo (instalação inicial do servidor, variáveis do `.env.production`,
solução de problemas) será consolidado no `README`/guia de deploy na etapa de implementação
(**FR-011**).
