> ⚠️ **ADR HISTÓRICO — SUPERADO.** Registro mantido para rastreabilidade. A
> [Constituição](../../.specify/memory/constitution.md) (v1.1.0) supera os 31 ADRs onde houver
> conflito — em especial os de *freeze* e a arquitetura DDD/CQRS/event-sourcing, desmontada nas
> specs 003–006 (a `domain/` foi de 118 → ~13 arquivos; payroll/cobertura removidos). Índice e
> contexto em [docs/adr/README.md](README.md).

# ADR-001: Monolito Modular

## Status

Aceito

## Data

2026-06-24

## Contexto

O Plantão 360 precisa de uma arquitetura que permita evolução incremental sem complexidade prematura de microsserviços.

## Problema

Escolher entre monolito, microsserviços ou monolito modular para o sistema de gestão de plantões médicos.

## Decisão

Adotar **monolito modular** com separação estrita de responsabilidades por camadas (Clean Architecture).

## Consequências

### Positivas
- Deploy simplificado (um único container)
- Desenvolvimento mais rápido no início
- Testes integrados mais fáceis
- Refatoração incremental possível

### Negativas
- Acoplamento acidental entre módulos se não houver disciplina
- Escala horizontal limitada ao monolito
- Necessidade de rigor na separação de módulos

## Alternativas Descartadas

1. **Microsserviços**: Complexidade operacional excessiva para a fase atual
2. **Monolito tradicional**: Sem separação clara, levaria a código spaghetti

## Notas

Se o sistema crescer significativamente, módulos podem ser extraídos como serviços独立.
