# Plantão 360

Sistema de gestão de plantões médicos para intranet da Unimed.

> **Deploy:** o servidor nunca compila. Toda atualização vem dentro da imagem —
> basta trocar `APP_VERSION` no `.env` e rodar `down; pull; up -d`.
> Guia completo em **[docs/runbook-deploy.md](docs/runbook-deploy.md)**.

## Pré-requisitos

- Docker e Docker Compose
- Python 3.12+ e Node.js 20+ (desenvolvimento local)

## Como Subir

```bash
cp .env.example .env     # preencha POSTGRES_PASSWORD, SECRET_KEY, ADMIN_PASSWORD
docker compose pull
docker compose up -d
```

O `docker-compose.yml` é o **único** arquivo de stack e sempre usa as imagens
publicadas no GHCR (`APP_VERSION` do `.env`). Para desenvolver com hot reload,
rode backend e frontend nativamente (ver "Desenvolvimento Local" abaixo).

## URLs de Acesso

| Serviço | URL |
|---------|-----|
| Aplicação (frontend + proxy /api) | http://localhost:3001 |
| Health Check | http://localhost:3001/api/v1/health |
| Swagger (dev local) | http://localhost:8000/api/v1/docs |

## Comandos Úteis

```bash
# Subir serviços
make up

# Derrubar serviços
make down

# Executar lint
make lint

# Executar testes
make test

# Formatar código
make format
```

## Desenvolvimento Local (sem Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn app.api.app:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Gerar Migrations

```bash
cd backend
alembic revision --autogenerate -m "descrição"
alembic upgrade head
```

## Estrutura do Projeto

```
plantao360/
├── backend/
│   ├── app/
│   │   ├── api/          # Rotas, middlewares, exception handlers
│   │   ├── core/         # Config, logging, security, constants
│   │   ├── database/     # SQLAlchemy base e session
│   │   ├── domain/       # Entidades, value objects, exceptions
│   │   ├── models/       # Modelos SQLAlchemy
│   │   ├── repositories/ # Repositórios
│   │   ├── schemas/      # Schemas Pydantic
│   │   ├── services/     # Serviços de negócio
│   │   └── tests/        # Testes
│   ├── alembic/          # Migrações
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── api/          # Cliente Axios e chamadas API
│   │   ├── components/   # Componentes React
│   │   ├── contexts/     # Contexts React
│   │   ├── hooks/        # Hooks customizados
│   │   ├── layouts/      # Layouts
│   │   ├── pages/        # Páginas
│   │   ├── routes/       # Rotas
│   │   ├── types/        # Tipos TypeScript
│   │   └── utils/        # Utilitários
│   ├── Dockerfile
│   └── package.json
├── docker/
│   └── nginx/            # Configuração Nginx
├── scripts/              # lint / test / format (uso local)
├── docs/                 # Documentação
├── backups/              # Backups
├── docker-compose.yml    # única stack (imagens do GHCR)
├── Makefile
├── .env.example
└── README.md
```

## Arquitetura

- **Clean Architecture** com separação de responsabilidades
- **Repository Pattern** para acesso a dados
- **Service Layer** para lógica de negócio
- **SOLID** como princípio de design

## Regra de Negócio

> Nenhuma regra de negócio deve existir no frontend.
> Todo cálculo e validação de negócio deve ocorrer exclusivamente no backend.
