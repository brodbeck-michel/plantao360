> ⚠️ **ADR HISTÓRICO — SUPERADO.** Registro mantido para rastreabilidade. A
> [Constituição](../../.specify/memory/constitution.md) (v1.1.0) supera os 31 ADRs onde houver
> conflito — em especial os de *freeze* e a arquitetura DDD/CQRS/event-sourcing, desmontada nas
> specs 003–006 (a `domain/` foi de 118 → ~13 arquivos; payroll/cobertura removidos). Índice e
> contexto em [docs/adr/README.md](README.md).

# ADR-010: Enterprise Application Patterns

## Status

Aceito

## Data

2026-06-24

## Contexto

O Plantão 360 precisa de padrões reutilizáveis para evitar duplicação e garantir consistência entre módulos.

## Problema

Sem padrões definidos:
- Cada módulo implementaria Repository/Service de forma diferente
- Lógica de transação duplicada
- Retornos inconsistentes entre endpoints
- SQLAlchemy exposto nos Routers
- Testes difíceis de mockar

## Decisão

Criar padrões enterprise **antes** dos módulos funcionais:
- BaseRepository genérico
- BaseService genérico
- UnitOfWork para transações
- Result Pattern para retornos
- Mapper Pattern para Model ↔ DTO
- Query Objects para parâmetros
- Event Dispatcher para eventos
- API Response padrão

## Consequências

### Positivas
- Zero duplicação entre módulos
- Consistência total
- Testabilidade facilitada
- Refatoração centralizada
- Onboarding rápido

### Negativas
- Mais arquivos inicialmente
- Curva de aprendizado
- Pode parecer over-engineering

## Alternativas Descartadas

1. **Implementar por módulo**: Duplicação inevitável
2. **Usar Active Record (SQLAlchemy mixins)**: Acoplamento com ORM
3. **Não criar padrões**: Caos na escala
