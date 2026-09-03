# Runbook — Deploy do Plantão 360 em produção

Passo a passo autossuficiente para publicar a aplicação no servidor de produção. **O GitHub
constrói as imagens; o servidor apenas baixa e sobe — nunca se compila (`--build`) no servidor.**

> Versão de referência deste guia: **1.5.1**. Para versões futuras, troque `1.5.1` pela versão
> desejada (sem `v`) em todos os comandos — é o mesmo valor de `APP_VERSION`.
>
> **Acesso:** só a porta **3001** (frontend) fica pública. A API do backend **não** é exposta ao
> host — o nginx do frontend faz proxy de `/api` para o backend pela rede interna do Docker.

---

## Pré-requisitos no servidor

- Linux com **Docker** e **Docker Compose v2**.
- Acesso à internet (para baixar as imagens do GHCR).
- Uma conta GitHub com acesso de leitura aos pacotes: um **Personal Access Token (PAT)** com
  escopo `read:packages` — só necessário se as imagens forem privadas (hoje são públicas).

---

## Passo 1 — Colocar o código no servidor

```bash
sudo mkdir -p /apps && cd /apps
git clone --branch v1.5.1 https://github.com/brodbeck-michel/plantao360.git
cd plantao360
```

> Em atualizações futuras (repo já clonado): `cd /apps/plantao360 && git fetch --tags && git checkout v1.5.1`.
>
> ⚠️ **Não compile as imagens no servidor.** O `docker-compose.prod.yml` usa imagens já
> publicadas no GHCR (sem `build:`) de propósito — compilar no servidor foi a causa de loops de
> restart no passado. O deploy só faz `pull` + `up`.

## Passo 2 — Criar o `.env` da raiz (controla versão e qual compose usar)

```bash
cat > .env <<'EOF'
COMPOSE_FILE=docker-compose.prod.yml
APP_VERSION=1.5.1
EOF
```

Com isso, os comandos `docker compose ...` sem `-f` já usam `docker-compose.prod.yml`
automaticamente, e a versão das imagens (e a versão exibida no rodapé da tela) vêm de
`APP_VERSION`. **Para atualizar uma versão futura, é só editar essa linha e repetir o Passo 4.**

## Passo 3 — Criar o `.env.production` ⚠️ (passo mais crítico)

```bash
cp .env.production.example .env.production
nano .env.production
```

Preencha **obrigatoriamente** com valores **seguros** (um `.env.production` incompleto/fraco faz o
backend **abortar o startup de propósito** — é a causa mais comum de falha no deploy):

```env
ENVIRONMENT=production
DEMO_MODE=false

POSTGRES_USER=plantao360
POSTGRES_PASSWORD=<uma senha forte>
POSTGRES_DB=plantao360
DATABASE_URL=postgresql+psycopg2://plantao360:<A MESMA senha acima>@db:5432/plantao360

SECRET_KEY=<cole o resultado do comando abaixo — precisa ter >= 32 caracteres>
ADMIN_EMAIL=gestao.dados@unimedtubarao.com.br
ADMIN_PASSWORD=<senha do admin, >= 8 caracteres, NAO pode ser "admin123">
```

Gere o `SECRET_KEY` no próprio servidor:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(48))"
```

**Regras que o app valida no startup (senão aborta com mensagem clara):**
- `SECRET_KEY` ≥ 32 caracteres e diferente do valor de exemplo.
- `ADMIN_PASSWORD` ≥ 8 caracteres e diferente dos valores padrão (`admin123` etc.).

> O `.env.production` (com os segredos) e o `.env` (com `APP_VERSION`) **nunca** vão para o git —
> ficam só no servidor. Ajuste também `ALLOWED_ORIGINS` e as portas (`BACKEND_PORT`/`FRONTEND_PORT`)
> conforme o ambiente, se necessário (os demais campos podem ficar com os padrões do
> `.env.production.example`).

## Passo 4 — Subir a aplicação

```bash
docker compose pull
docker compose up -d
```

(equivalente a `./scripts/deploy.sh`, que faz o mesmo `pull` + `up` com algumas checagens extras).

O `pull` baixa as imagens da versão definida em `APP_VERSION` (`.env`) no GHCR, e o `up -d` sobe os
serviços na ordem `db → backend → frontend`. O backend espera o Postgres ficar saudável, aplica as
migrations e só então passa a servir.

> **Backup:** no **primeiro** deploy não é necessário (não há dados a preservar). Em atualizações
> de uma produção **já em uso**, rode `./scripts/backup.sh` **antes** do deploy.

## Passo 5 — Verificar

```bash
docker compose ps
# os 3 serviços (db, backend, frontend) devem ficar "healthy"

# health da API pelo proxy do frontend (porta 8000 NÃO é exposta ao host):
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3001/api/v1/health
# deve retornar 200
```

Depois, abrir a aplicação no navegador na **porta 3001** do servidor e fazer login com o
`ADMIN_EMAIL` / `ADMIN_PASSWORD` definidos no `.env.production`. A versão exibida no rodapé do
menu lateral deve bater com o `APP_VERSION` definido no `.env`.

---

## Atualizar para uma nova versão

```bash
cd /apps/plantao360
git fetch --tags && git checkout v1.6.0   # se o compose/scripts também mudaram nessa versão
sed -i 's/^APP_VERSION=.*/APP_VERSION=1.6.0/' .env
docker compose pull
docker compose up -d
```

## Solução de problemas

Primeiro, sempre olhar o log do backend:

```bash
docker compose logs backend
```

| Sintoma no log / comportamento | Causa | O que fazer |
|---|---|---|
| Backend reinicia em loop; log diz **"Configuração de produção insegura"** | `SECRET_KEY` ou `ADMIN_PASSWORD` fraco/ausente no `.env.production` | Ajustar o Passo 3 e rodar o Passo 4 de novo |
| `pull` falha com **"unauthorized"** | Não autenticado no GHCR / token sem escopo (só se as imagens forem privadas) | Rodar `docker login ghcr.io` com PAT `read:packages` |
| `pull` falha com **"manifest unknown"** | `APP_VERSION` no `.env` não corresponde a nenhuma versão publicada | Conferir a versão em https://github.com/brodbeck-michel/plantao360/tags (sem o `v`) |
| Backend reinicia dizendo que **não conecta ao banco** | `DATABASE_URL` errada ou Postgres ainda subindo | Conferir `DATABASE_URL` e `POSTGRES_*` no `.env.production` (a senha na URL tem que ser idêntica à `POSTGRES_PASSWORD`) |
| `docker compose` reclama que não encontra o compose file | `.env` da raiz sem `COMPOSE_FILE=docker-compose.prod.yml` | Recriar o `.env` conforme o Passo 2 |
| Erro **"database is locked"** | `DATABASE_URL` apontando para SQLite | Confirmar que começa com `postgresql+psycopg2://...` |

## Rollback (voltar para a versão anterior, sem rebuild)

```bash
sed -i 's/^APP_VERSION=.*/APP_VERSION=1.5.0/' .env
docker compose pull
docker compose up -d
```

---

**Resumo em uma linha:** clonar o repo em `/apps/plantao360`, criar `.env` com `COMPOSE_FILE` e
`APP_VERSION`, criar `.env.production` com `SECRET_KEY`/`ADMIN_PASSWORD` seguros, e rodar
`docker compose pull && docker compose up -d`.
