# Como Executar — Plantao 360

Guia completo para executar o sistema localmente.

---

## Pre-requisitos

### Docker (Recomendado)

- Docker Desktop 4.x+ ou Docker Engine 24.x+
- Docker Compose v2.x+

### Desenvolvimento Local

- Python 3.12+
- Node.js 20+ (ou 18+)
- pip
- npm

---

## Opcao 1: Docker (Recomendado)

### Clone e Execute

```bash
cd "Plantoes PS Unimed/plantao360"

# Copiar variaveis de ambiente
cp .env.example .env

# Subir todo o sistema
docker compose up --build
```

Ou, em segundo plano:

```bash
docker compose up --build -d
```

### Acessar

| Servico | URL |
|---|---|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:8000 |
| **Swagger** | http://localhost:8000/api/v1/docs |
| **Health** | http://localhost:8000/api/v1/health |

### Parar

```bash
docker compose down
```

---

## Opcao 2: Desenvolvimento Local

### Backend

```bash
cd plantao360/backend

# Criar ambiente virtual
python -m venv .venv

# Ativar (Linux/Mac)
source .venv/bin/activate

# Ativar (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Executar migrations
alembic upgrade head

# Carregar dados de demonstracao
python -m app.seed.seed_data --dataset demo --clear

# Iniciar servidor
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend (em outro terminal)

```bash
cd plantao360/frontend

# Instalar dependencias
npm install

# Iniciar servidor de desenvolvimento
npm run dev
```

### Acessar

| Servico | URL |
|---|---|
| **Frontend** | http://localhost:5173 |
| **Backend API** | http://localhost:8000 |
| **Swagger** | http://localhost:8000/api/v1/docs |

> **Nota:** O frontend em modo dev faz proxy automatico das chamadas `/api` para `http://localhost:8000`.

---

## Dados de Demonstracao

O sistema ja inicia com dados de demonstracao carregados automaticamente (Docker) ou sob demanda (local).

### Datasets Disponiveis

| Dataset | Descricao | Comando |
|---|---|---|
| `demo` | 35 medicos, ~180 plantoes | `python -m app.seed.seed_data --dataset demo --clear` |
| `edge_cases` | Casos extremos para teste | `python -m app.seed.seed_data --dataset edge_cases --clear` |
| `showcase` | Dados minimos para demo | `python -m app.seed.seed_data --dataset showcase --clear` |

### Conteudo do Demo

- **35 Medicos** com nomes, CRMs e valores por hora
- **6 Competencias** (Janeiro a Junho 2026)
- **~180 Plantoes** com tipos T1/T2/T3
- **Shift Parts** (atribuicoes de medicos)
- Periodos em status draft, closed e paid

---

## Endpoints da API

### Health & Readiness

```bash
# Health check
curl http://localhost:8000/api/v1/health

# Readiness check
curl http://localhost:8000/api/v1/readiness
```

### CRUD Medicos

```bash
# Listar medicos
curl http://localhost:8000/api/v1/doctors

# Obter medico por ID
curl http://localhost:8000/api/v1/doctors/1
```

### Competencias

```bash
# Listar periodos
curl http://localhost:8000/api/v1/periods

# Criar periodo
curl -X POST http://localhost:8000/api/v1/periods \
  -H "Content-Type: application/json" \
  -d '{"year": 2026, "month": 7}'
```

### Plantoes

```bash
# Listar plantoes
curl http://localhost:8000/api/v1/shifts

# Filtrar por periodo
curl "http://localhost:8000/api/v1/shifts?period_id=1"
```

### Dashboard

```bash
# Dashboard operacional
curl http://localhost:8000/api/v1/query/dashboard
```

---

## Troubleshooting

### Backend nao inicia

1. Verifique se Python 3.12+ esta instalado: `python --version`
2. Verifique se todas as dependencias estao instaladas: `pip install -r requirements.txt`
3. Verifique se o banco foi criado: `alembic upgrade head`

### Frontend nao conecta ao Backend

1. Verifique se o backend esta rodando na porta 8000
2. No modo dev, o Vite faz proxy automatico para `/api`
3. Verifique o console do navegador para erros de rede

### Docker nao sobe

1. Verifique se o Docker esta rodando: `docker info`
2. Limpe containers antigos: `docker compose down -v`
3. Reconstrua: `docker compose up --build`

### Erro de migracao

1. Verifique as migrations: `cd backend && alembic history`
2. Reverta se necessario: `cd backend && alembic downgrade -1`
3. Reaplique: `cd backend && alembic upgrade head`
