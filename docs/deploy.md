# Guia de Deploy — Plantão 360 (Produção)

Como publicar e operar o Plantão 360 em produção. O princípio é simples:

> **O GitHub constrói as imagens. O servidor apenas baixa e sobe.**
> Nunca se compila (`--build`) no servidor.

Fluxo geral:

```
git tag vX.Y.Z  ─►  GitHub Actions builda  ─►  imagens no GHCR  ─►  servidor: deploy.sh (pull + up)
```

---

## 1. Pré-requisitos do servidor

- Linux com **Docker** e **Docker Compose v2**.
- Acesso à internet para baixar imagens do GHCR.
- Uma cópia do repositório (ou ao menos: `docker-compose.prod.yml`, `scripts/` e o `.env.production`).

## 2. Setup inicial (uma vez)

1. **Autenticar no GHCR** (as imagens podem ser privadas):
   ```bash
   docker login ghcr.io -u <seu-usuario-github>
   # senha = um Personal Access Token com escopo read:packages
   ```

2. **Criar o `.env.production`** a partir do modelo e preencher:
   ```bash
   cp .env.production.example .env.production
   ```
   Defina obrigatoriamente:
   - `POSTGRES_USER`, `POSTGRES_DB`
   - `POSTGRES_PASSWORD` — senha forte, **a mesma** que aparece na `DATABASE_URL`
   - `DATABASE_URL=postgresql+psycopg2://<user>:<senha>@db:5432/<db>`
   - `SECRET_KEY` — gere com:
     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(48))"
     ```
   - `ADMIN_EMAIL`, `ADMIN_PASSWORD` (>= 8 caracteres, não pode ser padrão)

   > O `.env.production` **nunca** vai para o git — ele fica só no servidor.

## 3. Publicar uma nova versão (no GitHub)

Criar e enviar uma tag de versão:

```bash
git tag v1.2.0
git push origin v1.2.0
```

O workflow **Release Images** constrói e publica no GHCR:
- `ghcr.io/brodbeck-michel/plantao360-backend:v1.2.0` (e `:latest`)
- `ghcr.io/brodbeck-michel/plantao360-frontend:v1.2.0` (e `:latest`)

Alternativa manual: aba **Actions → Release Images → Run workflow** (publica `:latest`).

## 4. Deploy no servidor (um comando)

```bash
cd /apps/plantao360
TAG=v1.2.0 ./scripts/deploy.sh
```

O script baixa as imagens da tag e sobe os serviços na ordem `db → backend → frontend`.
O backend espera o Postgres ficar saudável, aplica as migrations e só então serve.

## 5. Rollback

```bash
TAG=v1.1.0 ./scripts/deploy.sh    # volta para a versão anterior, sem rebuild
```

## 6. Seed de dados (manual — nunca automático em produção)

Em produção **nenhum seed roda no boot** (`DEMO_MODE=false`, `ENVIRONMENT=production`). Para
popular dados de exemplo sob demanda (normalmente só em ambiente de teste):

```bash
docker exec plantao360_backend_prod python -m app.seed.seed_data --dataset demo --clear
```

## 7. Backup e restauração

**Backup** (gera arquivo datado em `backups/`):
```bash
./scripts/backup.sh
```

**Restauração** em um banco limpo:
```bash
docker exec -i plantao360_db psql -U <POSTGRES_USER> -d <POSTGRES_DB> < backups/plantao360_<data>.sql
```

Recomendado agendar o backup no cron (ex.: diário às 2h):
```cron
0 2 * * *  cd /apps/plantao360 && ./scripts/backup.sh >> /var/log/plantao360-backup.log 2>&1
```

## 8. Solução de problemas

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| Backend reinicia dizendo que não conecta ao banco | Postgres ainda subindo ou `DATABASE_URL` errada | O `start.sh` espera o banco; se persistir, confira `DATABASE_URL` e `POSTGRES_*` no `.env.production` |
| `pull` falha com "unauthorized" | Não autenticado no GHCR ou imagem privada | Refazer `docker login ghcr.io` com token `read:packages` |
| Deploy sobe versão errada | `TAG` não informado | Rode com `TAG=vX.Y.Z ./scripts/deploy.sh` |
| Startup aborta em migração | Migration incompatível com Postgres | Ver seção 9; corrigir a migration e republicar |
| Erro "database is locked" | Ainda usando SQLite | Confirme que `DATABASE_URL` aponta para `postgresql+psycopg2://...` |

## 9. Validação da migração em Postgres (importante)

As migrations nasceram em SQLite. **Antes do primeiro go-live**, valide a migração do zero em
Postgres (idealmente igual ao de produção):

```bash
cd backend
ENVIRONMENT=test DATABASE_URL="postgresql+psycopg2://USER:SENHA@HOST:5432/DB" alembic upgrade head
```

Se algum tipo/constraint for incompatível, corrija a migration correspondente em
`backend/alembic/versions/` e republique. (Rastreado como T013/T014 em
`specs/002-producao-deploy/tasks.md`.)
