# Docker & Infrastructure Review — Plantao 360

**Data:** 2026-06-28
**Escopo:** Auditoria completa da infraestrutura Docker e configurações de deploy
**Objetivo:** Verificar conformidade com boas práticas de produção

---

## Visão Geral

A infraestrutura Docker do Plantão 360 é composta por:
- **2 Dockerfiles** (backend Python, frontend Node/Nginx)
- **3 docker-compose files** (base, dev, prod)
- **1 configuração Nginx**
- **1 script de inicialização** (start.sh)
- **5 arquivos de ambiente** (.env, .env.development, .env.production, .env.example, .env.test)

---

## 1. Backend Dockerfile

**Arquivo:** `backend/Dockerfile` (26 linhas)

### Análise

| Critério | Status | Detalhe |
|----------|--------|---------|
| Multi-stage build | ❌ Ausente | Usa stage único `python:3.12-slim` |
| Usuário não-root | ✅ Presente | `appuser` (uid 1000) criado e utilizado |
| Health check | ✅ Presente | `python -c "import urllib.request; urllib.request.urlopen(...)"` |
| Otimização de layers | ✅ Presente | `COPY requirements.txt` antes de `COPY .` |
| Sem secrets na imagem | ✅ OK | Nenhuma variável sensível exposta |
| CMD/ENTRYPOINT | ✅ OK | `CMD ["sh", "start.sh"]` |
| .dockerignore | ❌ Ausente | Arquivo não existe |

**Status: COM RESSALVAS**

### Issues

1. **Ausência de multi-stage build** — A imagem final contém pip, cache de build e dependências de compilação. Uma segunda etapa com `python:3.12-slim` como base reduziria o tamanho da imagem em ~30-40%.

2. **Ausência de .dockerignore** — Sem `.dockerignore`, o build copia desnecessariamente `.git`, `__pycache__`, `.pytest_cache`, `htmlcov/`, `test.db`, etc. para o contexto do Docker, aumentando tempo de build e risco de expor dados.

---

## 2. Frontend Dockerfile

**Arquivo:** `frontend/Dockerfile` (21 linhas)

### Análise

| Critério | Status | Detalhe |
|----------|--------|---------|
| Multi-stage build | ✅ Presente | `node:20-alpine` (builder) → `nginx:alpine` |
| Usuário não-root | ⚠️ Não aplicável | Nginx alpine roda como root por padrão (comum para reverse proxies) |
| Health check | ✅ Presente | `wget -q --spider http://localhost/nginx-health` |
| Otimização de layers | ✅ Presente | `COPY package.json` antes de `COPY .` |
| Sem secrets na imagem | ✅ OK | Nenhum |
| CMD/ENTRYPOINT | ✅ OK | `nginx -g "daemon off;"` |

**Status: APROVADO**

### Issues

Nenhum issue crítico. O multi-stage build é bem implementado.

---

## 3. docker-compose.yml (Base)

**Arquivo:** `docker-compose.yml` (46 linhas)

### Análise

| Critério | Status | Detalhe |
|----------|--------|---------|
| Health checks | ✅ Presente | Backend e frontend |
| Restart policies | ❌ Ausente | Nenhum serviço tem `restart` |
| Startup order | ✅ Presente | `depends_on` com `condition: service_healthy` |
| Gerenciamento de env | ✅ OK | `env_file` apontando para `.env.development` |
| Estratégia de volumes | ✅ OK | Named volume `plantao360_data` para dados |
| Resource limits | ❌ Ausente | Sem limites de CPU/memória |
| Isolamento de rede | ✅ Presente | Bridge network `plantao360` |
| Logging config | ❌ Ausente | Sem configuração de logging |

**Status: COM RESSALVAS**

### Issues

1. **Ausência de restart policies** — Para uso em desenvolvimento local, `restart: unless-stopped` seria recomendado para auto-recovery.

2. **Sem resource limits** — Em desenvolvimento local aceitável; para qualquer ambiente partilhado seria necessário definir limites.

3. **Sem logging config** — Logs do Docker seguirão o padrão (json-file sem rotação); em produção causa crescimento indefinido do `/var/lib/docker/containers`.

---

## 4. docker-compose.dev.yml

**Arquivo:** `docker-compose.dev.yml` (45 linhas)

### Análise

| Critério | Status | Detalhe |
|----------|--------|---------|
| Health check backend | ✅ Presente | Mesmo do base |
| Health check frontend | ❌ Ausente | P22 identificado no audit |
| Restart policies | ❌ Ausente | Nenhum |
| Startup order | ✅ Presente | `depends_on` com `condition: service_healthy` |
| Bind mounts | ✅ Presente | `./backend:/app` e `./frontend:/app` para hot reload |
| Resource limits | ❌ Ausente | Nenhum |
| Network isolamento | ✅ Presente | Rede separada `plantao360_dev` |

**Status: COM RESSALVAS**

### Issues

1. **Frontend sem healthcheck** (P22) — O serviço frontend usa `node:20-alpine` com `npm run dev -- --host`, mas não define healthcheck. O `depends_on` do backend não pode usar `condition: service_healthy` para o frontend. Atualmente funciona porque o frontend não depende do backend de forma declarativa via health.

2. **Bind mount pode sobrescrever dependências instaladas** — O mount `./backend:/app` sobrepõe todo o diretório `/app`, incluindo `requirements.txt` e `start.sh` já instalados na imagem. Se o `requirements.txt` local mudar, o container não refletirá a mudança automaticamente (precisa rebuild). Não é um bug, mas é uma limitação do bind mount que pode confundir desenvolvedores.

3. **Ausência de `npm install` no dev** — O container frontend dev usa `npm run dev` diretamente sem executar `npm install` previamente. Se as dependências não estiverem no `./frontend/node_modules` (mount local), o comando falhará. Assume-se que o desenvolvedor execute `npm install` na máquina host antes.

---

## 5. docker-compose.prod.yml

**Arquivo:** `docker-compose.prod.yml` (53 linhas)

### Análise

| Critério | Status | Detalhe |
|----------|--------|---------|
| Health checks | ✅ Presente | Backend e frontend |
| Restart policies | ✅ Presente | `restart: always` em ambos |
| Startup order | ✅ Presente | `depends_on` com `condition: service_healthy` |
| Resource limits | ✅ Parcial | Backend: 1 CPU, 512M RAM. Frontend: ausente |
| Volume strategy | ✅ Presente | Named volume `plantao360_prod_data` |
| Network isolamento | ✅ Presente | Rede `plantao360_prod` |
| Logging config | ❌ Ausente | Sem rotação de logs |

**Status: COM RESSALVAS**

### Issues

1. **P14 — Healthcheck frontend usa `localhost` (line 42)** — `wget -q --spider http://localhost/nginx-health` pode resolver para IPv6 em alguns ambientes. O `docker-compose.yml` base já usa `127.0.0.1` (line 35) — a versão prod deve seguir o mesmo padrão.

2. **Resource limits ausentes no frontend** — O backend tem limites definidos (1 CPU, 512M), mas o frontend não. Em produção, o frontend Nginx pode consumir memória indefinidamente sob carga.

3. **Sem logging config** — Produção deve definir `logging` com `json-file` driver e `max-size`/`max-file` para rotação.

4. **Produção ainda usa SQLite** — `.env.production` define `DATABASE_URL=postgresql+psycopg2://user:pass@localhost:5432/plantao360` com credenciais placeholder. Se o PostgreSQL não estiver disponível, o container falhará na migration.

5. **SECRET_KEY placeholder** — `.env.production` tem `SECRET_KEY=change-this-to-a-real-secret-in-production`. Em produção, isso deve ser substituído por um valor seguro via variável de ambiente ou secret management.

---

## 6. Nginx Configuration

**Arquivo:** `docker/nginx/nginx.conf` (47 linhas)

### Análise

| Critério | Status | Detalhe |
|----------|--------|---------|
| Gzip compression | ✅ Presente | Nível 6, tipos amplamente cobertos |
| Security headers | ✅ Presente | X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy |
| Static asset caching | ✅ Presente | `expires 1y` com `Cache-Control: public, immutable` |
| SPA routing | ✅ Presente | `try_files $uri $uri/ /index.html` |
| API proxy | ✅ Presente | `proxy_pass http://backend:8000` com headers corretos |
| Health endpoint | ✅ Presente | `/nginx-health` retorna 200 |

**Status: APROVADO**

### Issues

Nenhum issue crítico. Configuração sólida para SPA com backend proxy.

**Observações menores:**
- `X-Frame-Options` poderia ser substituído por `Content-Security-Policy: frame-ancestors 'self'` (mais moderno).
- `X-XSS-Protection` é descontinuado em navegadores modernos; `Content-Security-Policy` é a alternativa recomendada.
- Não há `server_tokens off` para esconder versão do Nginx.

---

## 7. Start Script

**Arquivo:** `backend/start.sh` (55 linhas)

### Análise

| Critério | Status | Detalhe |
|----------|--------|---------|
| Mode-aware startup | ✅ Presente | DEMO, DEVELOPMENT, PRODUCTION, TEST |
| Error handling | ✅ Presente | `set -e` no início |
| Signal handling | ✅ Presente | `exec uvicorn` substitui o shell, recebendo sinais diretamente |
| Migrations | ✅ Presente | `alembic upgrade head` (exceto test mode) |
| Seed data | ✅ Presente | Apenas em DEMO_MODE=true |

**Status: APROVADO**

### Issues

Nenhum issue crítico. Script bem estruturado.

**Observação:** O modo "demo" não é tratado explicitamente no case (linhas 38-54) — cai no padrão `development|demo` (linha 43) mas o case não tem `demo)` isolado. Funciona corretamente porque o shell faz fallthrough, mas poderia ser mais explícito.

---

## 8. Environment Files

**Arquivos:** `.env`, `.env.development`, `.env.production`, `.env.example`, `.env.test`

### Análise

| Arquivo | Status | Detalhe |
|---------|--------|---------|
| `.env` | ⚠️ | Local dev; `SECRET_KEY` é placeholder; `DEMO_MODE=true` |
| `.env.development` | ⚠️ | Mesmo do `.env`; `SECRET_KEY` não seguro |
| `.env.production` | ⚠️ | Credenciais PostgreSQL placeholder; `SECRET_KEY` placeholder |
| `.env.example` | ✅ | Template correto com placeholders |
| `.env.test` | ✅ | Configuração de teste apropriada |

**Status: COM RESSALVAS**

### Issues

1. **P17 — `.env.production` incompleto** — `SECRET_KEY` e `DATABASE_URL` contêm valores placeholder. Em produção real, devem ser injetados via variáveis de ambiente ou secret management (não commitados no repositório).

2. **`.env` e `.env.development` são idênticos** — Redundância; poderiam ser o mesmo arquivo.

3. **`.gitignore` não ignora `.env.*`** — Verificar se os arquivos `.env.*` estão no `.gitignore` para evitar commit de secrets.

4. **`ALLOWED_ORIGINS` em `.env.development`** — Inclui `http://localhost:3000,http://localhost:5173` — correto para dev.

---

## Resumo

| Componente | Status | Issues |
|------------|--------|--------|
| Backend Dockerfile | COM RESSALVAS | Sem multi-stage build, sem .dockerignore |
| Frontend Dockerfile | APROVADO | Nenhum |
| docker-compose.yml (Base) | COM RESSALVAS | Sem restart, sem resource limits, sem logging |
| docker-compose.dev.yml | COM RESSALVAS | P22: frontend sem healthcheck; bind mount overwrite |
| docker-compose.prod.yml | COM RESSALVAS | P14: localhost no healthcheck; sem resource limits frontend; sem logging |
| Nginx | APROVADO | Observações menores (headers modernos) |
| Start Script | APROVADO | Nenhum |
| Environment Files | COM RESSALVAS | P17: production com placeholders; redundância |

---

## Verificação de Issues do Production Readiness Audit

### P05 — Dockerfile usando create_all

**Status: ✅ CORRIGIDO**

O Dockerfile atual usa `CMD ["sh", "start.sh"]`, que executa `alembic upgrade head` (não `create_all()`). A correção foi aplicada corretamente.

### P12 — docker-compose.dev.yml assume Alembic funcional

**Status: ⚠️ PENDENTE**

O `docker-compose.dev.yml` herda `start.sh` via bind mount, que executa `alembic upgrade head`. Se as migrations continuarem quebradas (ETAPA 2), o container falhará na inicialização. A dependência da ETAPA 2 precisa ser resolvida primeiro.

### P14 — Healthcheck usando localhost vs 127.0.0.1

**Status: ⚠️ PARCIALMENTE CORRIGIDO**

- `docker-compose.yml` (base, line 35): Usa `127.0.0.1` ✅
- `docker-compose.prod.yml` (line 42): Ainda usa `localhost` ❌
- `docker-compose.dev.yml` (line 17): Usa `localhost` no healthcheck do backend ❌

### P16 — Production missing volume strategy

**Status: ✅ CORRIGIDO**

`docker-compose.prod.yml` define `plantao360_prod_data` como named volume (line 49). A estratégia de volume está implementada.

### P22 — Frontend sem healthcheck no dev

**Status: ⚠️ CONFIRMADO**

`docker-compose.dev.yml` não define healthcheck para o serviço frontend. O frontend dev não tem `condition: service_healthy` disponível.

### P13 — Caminho incorreto `app.api.app:app`

**Status: ✅ CORRIGIDO**

O `docker-compose.dev.yml` atual não sobrescreve o CMD — usa o `start.sh` do Dockerfile via bind mount. O path `app.main:app` é used internamente pelo uvicorn via start.sh.

---

## Pendências

### Críticas (devem ser resolvidas antes de produção)

| # | Issue | Componente | Ação |
|---|-------|------------|------|
| 1 | P14: Healthcheck `localhost` em prod | docker-compose.prod.yml:42 | Trocar para `127.0.0.1` |
| 2 | Production SECRET_KEY placeholder | .env.production | Definir via secret management |
| 3 | Production DATABASE_URL placeholder | .env.production | Configurar PostgreSQL real |

### Altas (devem ser resolvidas para robustez)

| # | Issue | Componente | Ação |
|---|-------|------------|------|
| 4 | Ausência de .dockerignore | backend/ | Criar `.dockerignore` |
| 5 | Ausência de .dockerignore | frontend/ | Criar `.dockerignore` |
| 6 | Frontend sem resource limits | docker-compose.prod.yml | Adicionar `deploy.resources.limits` |
| 7 | Sem logging config | docker-compose.prod.yml | Adicionar `logging` com rotação |
| 8 | P22: Frontend sem healthcheck | docker-compose.dev.yml | Adicionar healthcheck ou usar `service_started` |

### Médias (melhorias recomendadas)

| # | Issue | Componente | Ação |
|---|-------|------------|------|
| 9 | Multi-stage build ausente | backend/Dockerfile | Adicionar stage de build separado |
| 10 | Nginx: server_tokens off | nginx.conf | Adicionar `server_tokens off;` |
| 11 | Nginx: headers modernos | nginx.conf | Avaliar substituição de X-XSS-Protection |
| 12 | .env redundância | .env, .env.development | Consolidar ou remover duplicatas |
| 13 | Restart policies ausentes | docker-compose.yml | Adicionar `restart: unless-stopped` |

---

**Próximo passo:** ETAPA 7 (Frontend Review)
