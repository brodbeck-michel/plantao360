# Documentação

## Sprint 0 - Fundação do Projeto

### Objetivo

Criar a fundação completa do projeto Plantão 360, preparado para evolução sem implementar entidades de negócio.

### Stack Tecnológica

#### Frontend
- React 18
- TypeScript 5
- Vite 5
- Material UI 5
- React Query 5

#### Backend
- Python 3.12
- FastAPI
- SQLAlchemy 2
- Alembic
- Pydantic V2

#### Infraestrutura
- Docker
- Docker Compose
- Nginx

### Padrões de Arquitetura

- Clean Architecture
- SOLID
- Repository Pattern
- Service Layer Pattern

### Endpoints Disponíveis

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /api/v1/health | Health check do sistema |

### Endpoints Futuros

Os endpoints de domínio serão implementados nas sprints seguintes.

### Configuração

Variáveis de ambiente configuradas via `.env`:

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| APP_NAME | Nome da aplicação | Plantao360 |
| APP_VERSION | Versão | 1.0.0 |
| ENVIRONMENT | Ambiente | development |
| DATABASE_URL | URL do banco | sqlite:///./plantao360.db |
| SECRET_KEY | Chave secreta | (ver .env.example) |
| LOG_LEVEL | Nível de log | INFO |
| ALLOWED_ORIGINS | Origins permitidas | http://localhost:3000 |

### Logging

Logs em formato JSON estruturado:

```json
{
  "event": "REQUEST",
  "method": "GET",
  "path": "/api/v1/health",
  "status": 200,
  "duration_ms": 12,
  "timestamp": "2026-01-01T00:00:00Z"
}
```

### Correlation ID

Toda requisição recebe header `X-Request-ID`. Se não existir, um UUID é gerado automaticamente.
