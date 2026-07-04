# ADR-018: Extras de Plantão

**Data:** 2026-06-26
**Status:** Accepted
**Decisor:** Arquiteto de Domínio

## Contexto

O sistema Plantão 360 precisa registrar horas extras para plantões. Atualmente, o médico trabalha beyond its shift but there's no formal tracking of extra hours.

## Decisão

Criar o módulo Extras de Plantão com ciclo de vida:
- **pending** → approved/rejected/cancelled
- Extra pertence ao Shift (não ao Assignment)
- Período deve estar draft para criar extras
- Justificativa obrigatória
- Duração > 0 minutos

## Consequências

### Positivas
- Rastreabilidade formal de horas extras
- Fluxo de aprovação documentado
- Dados para cálculo financeiro futuro

### Negativas
- Mais uma entidade para gerenciar
- Coordenação manual necessária para evitar duplicatas

## Alternativas Consideradas

1. **Não registrar extras** — Rejeitado: sem rastreabilidade
2. **Registrar sem aprovação** — Rejeitado: sem controle
3. **Aprovação automática** — Rejeitado: muito arriscado

## Referências

- docs/domain/analises/analise-negocio-extras-v1.md
- docs/domain/invariantes-extras.md
- docs/domain/casos-borda-extras.md
