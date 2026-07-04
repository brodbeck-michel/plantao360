# ADR-009: Shift Uniqueness

## Status

Aceito

## Data

2026-06-24

## Contexto

A tabela `shifts` possui constraint `UNIQUE(shift_date, shift_type)`.

## Problema

Compreender o impacto dessa restrição no modelo de negócio.

## Decisão

Manter `UNIQUE(shift_date, shift_type)` como restrição estrutural.

## Análise

### Por que existe?
Para garantir que existe **no máximo um plantão de cada tipo por dia**. Evita duplicação acidental.

### Quais cenários cobre?
- Impede dois T1 no mesmo dia
- Impede dois R2 no mesmo dia
- Garante unicidade por tipo/dia

### Quais cenários não cobre?
- **Não impede múltiplos médicos no mesmo plantão** — isso é feito via `shift_parts`
- **Não impede múltiplos setores** — campo `sector` não existe ainda

### O sistema admite múltiplos T1 no mesmo dia?
**NÃO.** A constraint impede. Se houver necessidade futura de múltiplos T1 (ex: diferentes setores), será necessário:
1. Adicionar campo `sector`
2. Mudar UNIQUE para `(shift_date, shift_type, sector)`

### O sistema admite múltiplos setores?
**NÃO.** Campo `sector` não existe. Quando implementado, a constraint deverá ser revisada.

## Consequências

### Positivas
- Impede duplicação acidental
- Facilita queries por (date, type)
- Garante consistência

### Negativas
- Não suporta múltiplos setores (futuro)
- Pode necessitar revisão quando `sector` for implementado

## Alternativas Descartadas

1. **UNIQUE apenas (shift_date)**: Muito restritivo — impede T1 e T2 no mesmo dia
2. **Sem UNIQUE**: Risco alto de duplicação
