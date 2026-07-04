# Governance Alignment — Divergence Analysis

**Date:** Sprint 5.1
**Author:** Architecture Team

---

## 1. Por que o Validator marcou apenas 68%?

O Architecture Validator utiliza `to_snake_case(module_name)` para derivar caminhos de arquivos. Quando chamado com `Assignment`, ele procura por:
- `models/assignment.py`
- `repositories/assignment_repository.py`
- `services/assignment_service.py`

Mas os arquivos reais são:
- `models/shift_part.py`
- `repositories/shift_part_repository.py`
- `services/assignment_service.py` (este sim existe)

**Causa raiz:** O validator assume que nome de domínio = nome de arquivo.

---

## 2. Por que o Golden Guard caiu para 72%?

O Golden Guard compara a estrutura de arquivos do módulo Against o Golden Module (Doctor). Ele utiliza a mesma conversão `to_snake_case` e verifica existência de arquivos.

Quando chamado com `Assignment`:
- Espera `models/assignment.py` → encontra `models/shift_part.py` → FAIL
- Espera `repositories/assignment_repository.py` → encontra `repositories/shift_part_repository.py` → FAIL
- Espera `services/assignment_service.py` → encontra → PASS

**Causa raiz:** O Golden Guard compara nomes de arquivos, não responsabilidades.

---

## 3. Quais verificações assumem nomes como verdade absoluta?

| Verificação | Assume Nome? | Deveria Verificar |
|-------------|--------------|-------------------|
| Model exists | ✅ Sim | Existência + herança |
| Repository exists | ✅ Sim | Existência + interface |
| Service exists | ✅ Sim | Existência + padrão |
| Mapper exists | ✅ Sim | Existência + herança |
| Validator exists | ✅ Sim | Existência + padrão |
| DTOs exist | ✅ Sim | Existência + estrutura |
| Error Codes exist | ✅ Sim | Existência + StrEnum |
| Router exists | ✅ Sim | Existência + ApiResponse |
| Tests exist | ✅ Sim | Existência + cobertura |

---

## 4. Quais verificações realmente avaliam responsabilidades?

| Verificação | Avalia Responsabilidade? |
|-------------|-------------------------|
| Service uses UnitOfWork | ✅ Sim |
| Service uses Result pattern | ✅ Sim |
| Service uses ErrorCode | ✅ Sim |
| Service uses EventDispatcher | ✅ Sim |
| Mapper inherits BaseMapper | ✅ Sim |
| Router uses ApiResponse | ✅ Sim |
| Router has pagination headers | ✅ Sim |
| Router does not import SQLAlchemy | ✅ Sim |

---

## 5. Quais verificações precisam evoluir?

Todas as verificações de **existência de arquivo** precisam evoluir para:
1. Consultar o Domain Alias Registry
2. Verificar múltiplos nomes possíveis
3. Validar responsabilidade (herança, interface) além de existência
4. Compreender Aggregate Owner

---

## Plano de Ação

1. Criar Domain Alias Registry (fonte única da verdade)
2. Evoluir Architecture Validator para consultar registry
3. Evoluir Golden Guard para consultar registry
4. Criar Governance Metadata
5. Criar Validator Profiles
6. Criar Architecture Exceptions
7. Implementar ADR Traceability
