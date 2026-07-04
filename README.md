# Plantão 360

Sistema de gestão de plantões médicos para intranet da Unimed.

## Pré-requisitos

- Docker e Docker Compose
- Python 3.12+ (desenvolvimento local)
- Node.js 20+ (desenvolvimento local)

## Como Subir

```bash
# Copiar variáveis de ambiente
cp .env.example .env

# Subir com Docker
docker compose up -d

# Ou usar Make
make setup
```

## URLs de Acesso

| Serviço | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| API | http://localhost:8000 |
| Swagger | http://localhost:8000/api/v1/docs |
| ReDoc | http://localhost:8000/api/v1/redoc |
| Health Check | http://localhost:8000/api/v1/health |

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
├── scripts/              # Scripts auxiliares
├── docs/                 # Documentação
├── backups/              # Backups
├── docker-compose.yml
├── docker-compose.dev.yml
├── docker-compose.prod.yml
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
