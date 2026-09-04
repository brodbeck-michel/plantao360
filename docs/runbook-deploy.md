# Runbook — Deploy e operação do Plantão 360

O servidor **nunca compila nada**. Toda mudança — código, migrations, nginx,
frontend — viaja dentro das imagens publicadas no GHCR pelo GitHub Actions.

## O que existe na pasta do servidor (`/apps/plantao360`)

Só três arquivos:

| Arquivo              | Para quê                                                        |
| -------------------- | --------------------------------------------------------------- |
| `docker-compose.yml` | a stack (db + backend + frontend/nginx)                          |
| `.env`               | **toda** a configuração, inclusive `APP_VERSION`                 |
| `logo.png`           | logo exibido na aplicação — troque o arquivo e reinicie o front  |

Nada mais. Sem `scripts/`, sem `docs/`, sem código-fonte.

## Instalação (uma vez)

```bash
mkdir -p /apps/plantao360 && cd /apps/plantao360
# copie docker-compose.yml, .env (a partir de .env.example) e logo.png
docker login ghcr.io          # só se as imagens forem privadas
docker compose up -d
```

Preencha no `.env`: `APP_VERSION`, `POSTGRES_PASSWORD`, `SECRET_KEY`,
`ADMIN_PASSWORD`. O backend **aborta o startup** se `SECRET_KEY` ou
`ADMIN_PASSWORD` estiverem com valor padrão/fraco.

Acesso: `http://<servidor>:3001` (porta ajustável por `FRONTEND_PORT`).
A API não é publicada no host — o nginx do frontend faz proxy de `/api`.

## Atualizar para uma nova versão

1. Edite `APP_VERSION=` no `.env` com a tag publicada (ex.: `1.6.0`).
2. ```bash
   docker compose down
   docker compose pull
   docker compose up -d
   ```

As migrations rodam sozinhas no startup do backend (`app/core/lifespan.py`).

**Rollback:** volte `APP_VERSION` para a versão anterior e repita o passo 2.
(Se a nova versão tiver migration destrutiva, restaure o backup antes.)

## Publicar uma nova versão

```bash
git tag v1.6.0 && git push origin v1.6.0
```

O workflow `release-images.yml` publica
`ghcr.io/brodbeck-michel/plantao360-{backend,frontend}:1.6.0` (sem o `v`).

## Backup do banco

```bash
docker exec plantao360_db pg_dump -U plantao360 -d plantao360 > plantao360_$(date +%F).sql
```

No cron (diário às 2h):

```
0 2 * * * docker exec plantao360_db pg_dump -U plantao360 -d plantao360 > /var/backups/plantao360_$(date +\%F).sql
```

Restaurar em banco limpo:

```bash
docker exec -i plantao360_db psql -U plantao360 -d plantao360 < arquivo.sql
```

## Diagnóstico

```bash
docker compose ps
docker compose logs -f backend
curl -s localhost:3001/api/v1/health
```

| Sintoma                                   | Causa provável                                          |
| ----------------------------------------- | -------------------------------------------------------- |
| `manifest unknown` no `pull`              | `APP_VERSION` não existe no GHCR (ou falta `docker login`) |
| backend reiniciando                       | `SECRET_KEY`/`ADMIN_PASSWORD` padrão, ou senha do Postgres divergente |
| logo não muda                             | falta `logo.png` na pasta — `docker compose restart frontend` |
