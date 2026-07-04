# ADR-005: Service Layer Pattern

## Status

Aceito

## Data

2026-06-24

## Contexto

Organizar lógica de negócio no backend.

## Problema

Onde colocar validações, regras de negócio e orquestração entre repositories e APIs.

## Decisão

Adotar **Service Layer Pattern** com camada de Services entre Routes e Repositories.

```
Routes → Services → Repositories → Database
```

## Consequências

### Positivas
- Services testáveis sem dependência de HTTP
- Repositórios genéricos e reutilizáveis
- Separação clara de responsabilidades
- Fácil de mockar em testes

### Negativas
- Mais uma camada de abstração
- Pode parecer over-engineering para operações CRUD simples

## Alternativas Descartadas

1. **Logic in Routes**: Acoplamento com HTTP, difícil de testar
2. **Active Record (Django-style)**: Lógica no modelo, acoplamento com ORM
