# ADR-003: FastAPI + React

## Status

Aceito

## Data

2026-06-24

## Contexto

Escolher stack tecnológica para frontend e backend do Plantão 360.

## Problema

Definir frameworks que suportem performance, tipagem, documentação automática e ecossistema maduro.

## Decisão

- **Backend**: FastAPI (Python 3.12)
- **Frontend**: React 18 + TypeScript 5 + Vite 5

## Consequências

### Positivas
- FastAPI: Auto-documentação OpenAPI, validação via Pydantic, async nativo
- React: Ecossistema vasto, MUI para UI, React Query para cache
- TypeScript: Type safety em todo o frontend
- Vite: Build rápido, HMR excelente

### Negativas
- FastAPI: Ecossistema menor que Django para admin
- React: Bundle size maior que alternativas leves

## Alternativas Descartadas

1. **Django REST**: Mais pesado, menos flexível para APIs REST puras
2. **Flask**: Sem auto-documentação, validação manual
3. **Vue.js**: Ecossistema menor que React no Brasil
4. **Angular**: Curva de aprendizado maior, mais verboso
