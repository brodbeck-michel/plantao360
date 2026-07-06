# Deploy Produção — Plantão 360

## Pré-requisitos no Servidor

- Docker instalado
- Docker Compose instalado
- Acesso ao GitHub: `https://github.com/brodbeck-michel/plantao360`
- Portas abertas: `8000` (API) e `3000` (Frontend)

---

## Passo a Passo

### 1. Clonar o repositório

```bash
git clone https://github.com/brodbeck-michel/plantao360.git
cd plantao360
```

### 2. Verificar a tag

```bash
git checkout v1-operational-core
```

### 3. Criar o arquivo .env.production

O arquivo `.env.production` já existe no repositório. Ajustar o `SECRET_KEY`:

```bash
# Gerar uma chave aleatória
openssl rand -hex 32
```

Editar `.env.production` e substituir:
```
SECRET_KEY=<cole_a_chave_gerada_acima>
```

### 4. Construir e subir

```bash
docker compose -f docker-compose.prod.yml up --build -d
```

### 5. Verificar saúde

```bash
# Status dos containers
docker compose -f docker-compose.prod.yml ps

# Logs do backend
docker compose -f docker-compose.prod.yml logs backend --tail 20

# Testar API
curl http://localhost:8000/api/v1/health

# Testar Frontend
curl -I http://localhost:3000
```

### 6. Normalizar dados (primeira vez)

Após o primeiro build, o seed cria turnos apenas com T1/T2/T3. Para adicionar R1/R2:

```bash
docker cp backend/scripts/normalize_all_periods.py plantao360_backend_prod:/tmp/
docker exec plantao360_backend_prod python /tmp/normalize_all_periods.py
```

---

## Arquitetura

```
┌─────────────────────────────────────────────┐
│                  Servidor                   │
│                                             │
│  ┌──────────────┐    ┌──────────────┐      │
│  │   Frontend   │    │   Backend    │      │
│  │   (nginx)    │───▶│  (FastAPI)   │      │
│  │   :3000      │    │   :8000      │      │
│  └──────────────┘    └──────┬───────┘      │
│                             │               │
│                    ┌────────▼────────┐      │
│                    │   SQLite DB     │      │
│                    │  /app/data/     │      │
│                    │  plantao360.db  │      │
│                    └─────────────────┘      │
│                                             │
│              Volume Docker:                 │
│    plantao360_prod_data:/app/data           │
└─────────────────────────────────────────────┘
```

## Portas

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| Frontend | 3000 | Interface web |
| Backend | 8000 | API REST |

## Variáveis de Ambiente (.env.production)

| Variável | Valor Padrão | Descrição |
|----------|-------------|-----------|
| DATABASE_URL | sqlite:///./data/plantao360.db | Banco SQLite (volume) |
| SECRET_KEY | **ALTERAR** | Chave de segurança |
| DEMO_MODE | true | Modo demonstração |
| VITE_MVP_MODE | true | Sidebar reduzida |
| ENABLE_JWT | false | Autenticação desativada |
| LOG_LEVEL | INFO | Nível de log |

## Comandos Úteis

```bash
# Parar tudo
docker compose -f docker-compose.prod.yml down

# Rebuild completo
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up --build -d

# Logs em tempo real
docker compose -f docker-compose.prod.yml logs -f

# Acessar shell do backend
docker exec -it plantao360_backend_prod bash

# Verificar banco
docker exec plantao360_backend_prod python -c "
import sqlite3
conn = sqlite3.connect('/app/data/plantao360.db')
c = conn.cursor()
c.execute('SELECT COUNT(*) FROM shifts')
print('Shifts:', c.fetchone()[0])
c.execute('SELECT COUNT(*) FROM shift_parts')
print('Assignments:', c.fetchone()[0])
c.execute('SELECT COUNT(*) FROM doctors')
print('Doctors:', c.fetchone()[0])
conn.close()
"
```

## Troubleshooting

| Problema | Solução |
|----------|---------|
| Backend não sobe | Verificar logs: `docker compose logs backend` |
| DB não persiste | Verificar volume: `docker volume ls` |
| Porta em uso | Alterar porta no `docker-compose.prod.yml` |
| Frontend não acessível | Verificar se backend está healthy primeiro |
