# Feature Manifest Guide — Plantão 360

**Sprint:** 12 — Frontend Architecture, Enterprise Foundation & Golden Frontend Platform
**Data:** 2026-06-27

---

## O que é um Feature Manifest?

Um Feature Manifest é um arquivo JSON que documenta completamente uma feature do frontend:
- Rotas e permissões
- Componentes e hooks
- Services e types
- Endpoints consumidos
- Testes planejados

---

## Estrutura

```json
{
  "name": "feature-name",
  "version": "1.0.0",
  "description": "Descrição da feature",
  "type": "feature",
  "golden_module": false,
  "routes": {
    "routeName": {
      "path": "/app/feature",
      "component": "FeatureScreen",
      "personas": ["coordenador", "admin"],
      "endpoints": ["GET /api/v1/feature"],
      "query_objects": ["FeatureQuery"],
      "read_models": ["FeatureSummary"],
      "mutations": ["CreateFeature", "UpdateFeature"]
    }
  },
  "components": ["Component1", "Component2"],
  "hooks": ["useFeatureList", "useFeatureDetail"],
  "services": ["featureQueries", "featureMutations"],
  "types": ["Feature", "FeatureSummary", "FeatureFilters"],
  "tests": {
    "unit": ["component.test.tsx"],
    "hooks": ["use-feature.test.ts"],
    "integration": ["feature-api.test.ts"]
  }
}
```

---

## Campos

### name
Nome da feature (kebab-case).

### version
Versão semântica.

### description
Descrição curta.

### type
Tipo do módulo (`feature`, `shared`, `layout`).

### golden_module
Se `true`, é o módulo de referência.

### routes
Mapa de rotas da feature.

#### routeName
Nome da rota (ex: `list`, `detail`, `form`).

#### path
Caminho da rota (pode ser string ou array).

#### component
Nome do componente que renderiza a rota.

### personas
Personas que podem acessar a rota.

### endpoints
Endpoints consumidos pela rota.

### query_objects
Query Objects do backend consumidos.

### read_models
Read Models do backend consumidos.

### mutations
Mutations do backend consumidos.

### components
Lista de componentes da feature.

### hooks
Lista de hooks da feature.

### services
Lista de services da feature.

### types
Lista de types da feature.

### tests
Mapa de testes planejados.

---

## Validação

O Frontend Validator (`src/shared/utils/feature-validator.ts`) valida:
1. Estrutura de diretórios
2. Imports proibidos
3. Estrutura do manifest
4. Formato dos endpoints
5. Naming

### Uso
```bash
# Validar uma feature
npx ts-node src/shared/utils/feature-validator.ts doctor

# Validar todas as features
npx ts-node src/shared/utils/feature-validator.ts
```

---

## Manifests Existentes

| Feature | Golden | Status |
|---|---|---|
| doctor | ✅ | ✅ Criado |
| period | ❌ | ✅ Criado |
| shift | ❌ | ✅ Criado |
| assignment | ❌ | ✅ Criado |
| extra | ❌ | ✅ Criado |
| coverage | ❌ | ✅ Criado |
| payroll | ❌ | ✅ Criado |
| dashboard | ❌ | ✅ Criado |
| analytics | ❌ | ✅ Criado |
| readiness | ❌ | ✅ Criado |

---

## Referências

- `frontend/manifests/doctor.json`
- `frontend/src/shared/utils/feature-validator.ts`
