> ⚠️ **ADR HISTÓRICO — SUPERADO.** Registro mantido para rastreabilidade. A
> [Constituição](../../.specify/memory/constitution.md) (v1.1.0) supera os 31 ADRs onde houver
> conflito — em especial os de *freeze* e a arquitetura DDD/CQRS/event-sourcing, desmontada nas
> specs 003–006 (a `domain/` foi de 118 → ~13 arquivos; payroll/cobertura removidos). Índice e
> contexto em [docs/adr/README.md](README.md).

# ADR-002: Clean Architecture

## Status

Aceito

## Data

2026-06-24

## Contexto

O sistema precisa de separação clara entre lógica de negócio, infraestrutura e apresentação.

## Problema

Garantir que regras de negócio não vazem para o frontend e que infraestrutura possa ser trocada sem impacto no domínio.

## Decisão

Adotar **Clean Architecture** com as seguintes camadas:

- **Domain**: Entidades, Value Objects, Exceptions de negócio
- **Application**: Services, Schemas (DTOs)
- **Infrastructure**: Database, Repositories, External APIs
- **Presentation**: Routes, Middlewares, Exception Handlers

## Consequências

### Positivas
- Regras de negócio isoladas e testáveis
- Infraestrutura substituível (SQLite → PostgreSQL)
- Frontend independente do backend
- Testes unitários rápidos para lógica de negócio

### Negativas
- Mais arquivos e pastas inicialmente
- Curva de aprendizado para a equipe
- Overhead de abstração em casos simples

## Alternativas Descartadas

1. **MVC tradicional**: Acoplamento entre camadas, lógica de negócio em controllers
2. **Hexagonal Architecture**: Similar, mas Clean Architecture é mais consolidada na comunidade Python/FastAPI
