# Runbook — Deploy do Plantão 360 em produção

Passo a passo autossuficiente para publicar a aplicação no servidor de produção. **O GitHub
constrói as imagens; o servidor apenas baixa e sobe — nunca se compila (`--build`) no servidor.**

> Versão de referência deste guia: **v1.2.1** (primeiro go-live). Para versões futuras, troque
> `v1.2.1` pela tag desejada em todos os comandos.
>
> **Acesso:** só a porta **3001** (frontend) fica pública. A API do backend **não** é exposta ao
> host — o nginx do frontend faz proxy de `/api` para o backend pela rede interna do Docker.

---

## Pré-requisitos no servidor

- Linux com **Docker** e **Docker Compose v2**.
- Acesso à internet (para baixar as imagens do GHCR).
- Uma conta GitHub com acesso de leitura aos pacotes: um **Personal Access Token (PAT)** com
  escopo `read:packages`.

---

## Passo 1 — Colocar o código no servidor

```bash
sudo mkdir -p /apps && cd /apps
git clone --branch v1.2.1 https://github.com/brodbeck-michel/plantao360.git
cd plantao360
```

> Em atualizações futuras (repo já clonado): `cd /apps/plantao360 && git fetch --tags && git checkout v1.2.1`.
>
> ⚠️ **Não compile as imagens no servidor.** O `docker-compose.prod.yml` usa imagens já
> publicadas no GHCR (sem `build:`) de propósito — compilar no servidor foi a causa de loops de
> restart no passado. O deploy só faz `pull` + `up`.

## Passo 2 — Autenticar no GHCR (uma vez por servidor)

```bash
docker login ghcr.io -u <SEU_USUARIO_GITHUB>
# senha = o Personal Access Token com escopo read:packages
```

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

> O `.env.production` **nunca** vai para o git — fica só no servidor. Ajuste também
> `ALLOWED_ORIGINS` e as portas (`BACKEND_PORT`/`FRONTEND_PORT`) conforme o ambiente, se necessário
> (os demais campos podem ficar com os padrões do `.env.production.example`).

## Passo 4 — Subir a aplicação

```bash
TAG=v1.2.1 ./scripts/deploy.sh
```

O script baixa as imagens da tag no GHCR e sobe os serviços na ordem `db → backend → frontend`. O
backend espera o Postgres ficar saudável, aplica as migrations e só então passa a servir.

> **Backup:** no **primeiro** deploy não é necessário (não há dados a preservar). Em atualizações
> de uma produção **já em uso**, rode `./scripts/backup.sh` **antes** do deploy.

## Passo 5 — Verificar

```bash
docker compose -f docker-compose.prod.yml ps
# os 3 serviços (db, backend, frontend) devem ficar "healthy"

# health da API pelo proxy do frontend (porta 8000 NÃO é mais exposta ao host):
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:3001/api/v1/health
# deve retornar 200
```

Depois, abrir a aplicação no navegador na **porta 3001** do servidor e fazer login com o
`ADMIN_EMAIL` / `ADMIN_PASSWORD` definidos no `.env.production`.

---

## Solução de problemas

Primeiro, sempre olhar o log do backend:

```bash
docker compose -f docker-compose.prod.yml logs backend
```

| Sintoma no log / comportamento | Causa | O que fazer |
|---|---|---|
| Backend reinicia em loop; log diz **"Configuração de produção insegura"** | `SECRET_KEY` ou `ADMIN_PASSWORD` fraco/ausente no `.env.production` | Ajustar o Passo 3 e rodar o Passo 4 de novo |
| `pull` falha com **"unauthorized"** | Não autenticado no GHCR / token sem escopo | Refazer `docker login ghcr.io` com PAT `read:packages` (Passo 2) |
| Backend reinicia dizendo que **não conecta ao banco** | `DATABASE_URL` errada ou Postgres ainda subindo | Conferir `DATABASE_URL` e `POSTGRES_*` no `.env.production` (a senha na URL tem que ser idêntica à `POSTGRES_PASSWORD`) |
| Deploy sobe a **versão errada** | `TAG` não informado | Rodar com `TAG=v1.2.0 ./scripts/deploy.sh` |
| Erro **"database is locked"** | `DATABASE_URL` apontando para SQLite | Confirmar que começa com `postgresql+psycopg2://...` |

## Rollback (voltar para a versão anterior, sem rebuild)

```bash
TAG=v1.1.0 ./scripts/deploy.sh
```

---

**Resumo em uma linha:** clonar o repo na tag `v1.2.0` em `/apps/plantao360`, `docker login ghcr.io`,
criar o `.env.production` com `SECRET_KEY` e `ADMIN_PASSWORD` seguros, e rodar
`TAG=v1.2.0 ./scripts/deploy.sh`.
