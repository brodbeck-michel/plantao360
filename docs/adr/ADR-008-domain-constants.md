> ⚠️ **ADR HISTÓRICO — SUPERADO.** Registro mantido para rastreabilidade. A
> [Constituição](../../.specify/memory/constitution.md) (v1.1.0) supera os 31 ADRs onde houver
> conflito — em especial os de *freeze* e a arquitetura DDD/CQRS/event-sourcing, desmontada nas
> specs 003–006 (a `domain/` foi de 118 → ~13 arquivos; payroll/cobertura removidos). Índice e
> contexto em [docs/adr/README.md](README.md).

# ADR-008: Domain Constants

## Status

Aceito

## Data

2026-06-24

## Contexto

O domínio do Plantão 360 possui conceitos que se repetem em múltiplas camadas: models, schemas, services, repositories, frontend, exportações.

## Problema

Strings mágicas e enums duplicados geram:
- Inconsistência entre camadas
- Dificuldade de manutenção
- Erros de digitação
- Impossibilidade de refatoração centralizada

## Decisão

Centralizar conceitos do domínio em:
- `domain/constants/` — Enums compartilhados (ShiftType, PeriodStatus)
- `domain/rules/` — Códigos de regras de negócio (BusinessRuleCode)
- `domain/errors/` — Catálogo de mensagens de erro
- `domain/events/` — Catálogo de nomes de eventos

## Consequências

### Positivas
- Strings mágicas eliminadas
- Enums reutilizáveis em todas as camadas
- Testabilidade dos enums
- Preparação para SQLAlchemy, Pydantic, Frontend
- Facilita internacionalização futura

### Negativas
- Mais arquivos para manter
- Necessidade de importar de módulos específicos

## Alternativas Descartadas

1. **Enums nos models**: Acoplamento com SQLAlchemy
2. **Strings fixas nos services**: Duplicação e inconsistência
3. **Constantes no frontend**: Gera divergência backend/frontend
