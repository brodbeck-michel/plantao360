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
