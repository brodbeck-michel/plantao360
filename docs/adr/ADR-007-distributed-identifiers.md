# ADR-007: Distributed Identifiers

## Status

Aceito

## Data

2026-06-24

## Contexto

O sistema requer rastreabilidade distribuída para logs, auditoria, integrações e observabilidade. Identificadores únicos são fundamentais para correlacionar eventos entre componentes.

## Problema

UUIDs podem ser gerados aleatoriamente em qualquer lugar do sistema, criando:
- Inconsistência na formatação
- Dificuldade de rastreabilidade
- Acoplamento implícito com biblioteca `uuid`
- Impossibilidade de centralizar geração e validação

## Decisão

Centralizar geração e manipulação de identificadores em `common/identifiers.py` com funções:
- `generate_uuid()` → UUID
- `generate_uuid_str()` → str
- `parse_uuid(value)` → UUID
- `is_valid_uuid(value)` → bool

Tipos alias em `common/types.py`:
- `UUIDStr`, `RequestID`, `CorrelationID`, `AuditID`, `EventID`

Context variables em `common/context.py`:
- `set_request_id()` / `get_request_id()`
- `set_correlation_id()` / `get_correlation_id()`

## Consequências

### Positivas
- Ponto único de geração de UUIDs
- Rastreabilidade distribuída facilitada
- Logs estruturados com request_id e correlation_id automáticos
- Preparação para OpenTelemetry e Event Sourcing
- Facilita integrações com sistemas externos

### Negativas
- Necessidade de garantir que nenhum `uuid.uuid4()` direto seja usado
- Overhead mínimo de uma camada de abstração

## Alternativas Descartadas

1. **Usar `uuid.uuid4()` diretamente onde necessário**: Gera inconsistência e dificulta manutenção
2. **Usar ULID**: Mais complexo, UUID já é padrão consolidado
3. **Usar KSUID**: Biblioteca menos madura que uuid
